import os
import time
from hashlib import md5 as _md5

from . import get_param, uid, gid, printerr, run, cp
from . import (
    POSTGRESCONF_ORIG, PG_HBA_ORIG, BACKUP_DIR, DATA_FILES_DIR,
    BACKUP_FILE_PREFIX, PGDATA, DATABASE_NAME, DATABASE_USER, DATABASE_HOST,
    DEBUG
)
from .prepare import prepare
from .secret import readsecret
from .gprun import gprun


DB_ENV = {
    'PGHOST': DATABASE_HOST,
    'PGSSLMODE': 'verify-ca',
    'PGSSLROOTCERT': '/run/secrets/PG_SERVER_SSL_CACERT',
    'PGSSLKEY': '/run/secrets/PG_CLIENT_SSL_KEY',
    'PGSSLCERT': '/run/secrets/PG_CLIENT_SSL_CERT',
}


def get_db_env(d=DATABASE_NAME, u=DATABASE_USER):
    ret = DB_ENV.copy()
    ret['PGUSER'] = u
    ret['PGDATABASE'] = d
    ret['PGPASSWORD'] = readsecret('DB_PASSWORD_%s' % u.upper(), decode=True)
    return ret


def md5(s):
    return _md5(s.encode()).hexdigest()


def ensure_db(db, user):
    """
    Initialize the database, set up users and passwords
    """
    os.makedirs(PGDATA, exist_ok=True)
    os.chmod(PGDATA, 0o700)
    u, g = uid('postgres'), gid('postgres')
    for root, dirs, files in os.walk(PGDATA):
        os.chown(root, u, g)

    PG_VERSION = os.path.join(PGDATA, 'PG_VERSION')
    if not os.path.isfile(PG_VERSION) or os.path.getsize(PG_VERSION) == 0:
        gprun(userspec='postgres', command=['initdb'], sys_exit=False)

    dest = os.path.join(PGDATA, 'pg_hba.conf')
    cp(PG_HBA_ORIG, dest, 'postgres', 'postgres', 0o600)

    dest = os.path.join(PGDATA, 'postgresql.conf')
    cp(POSTGRESCONF_ORIG, dest, 'postgres', 'postgres', 0o600)

    prepare('postgres')

    dbpass = readsecret('DB_PASSWORD_POSTGRES', decode=True)
    dbpass_postgres = "'md5%s'" % md5(dbpass + 'postgres')
    dbpass = readsecret('DB_PASSWORD_DJANGO', decode=True)
    dbpass_django = "'md5%s'" % md5(dbpass + user)
    dbpass = readsecret('DB_PASSWORD_EXPLORER', decode=True)
    dbpass_explorer = "'md5%s'" % md5(dbpass + 'explorer')

    # start postgres locally
    gprun(userspec='postgres', sys_exit=False, command=[
        'pg_ctl',
        '-o', "-c listen_addresses='127.0.0.1'",
        '-o', "-c log_statement=none",
        '-o', "-c log_connections=off",
        '-o', "-c log_disconnections=off",
        '-w', 'start'
    ])

    run([
        'psql', '-h', '127.0.0.1', '-U', 'postgres',
        '-c', 'ALTER ROLE postgres ENCRYPTED PASSWORD %s' % dbpass_postgres,
        '-c', 'CREATE ROLE %s' % user,
        '-c', 'ALTER ROLE %s '
              'ENCRYPTED PASSWORD %s LOGIN SUPERUSER' % (user, dbpass_django),
        '-c', 'CREATE ROLE explorer',
        '-c', 'ALTER ROLE explorer '
              'ENCRYPTED PASSWORD %s LOGIN' % dbpass_explorer,
        '-c', '\c postgres %s' % user,
        '-c', 'CREATE DATABASE %s' % db,
        '-c', '\c %s %s' % (db, user),
        '-c', 'REVOKE CREATE ON SCHEMA public FROM public',
        '-c', 'GRANT SELECT ON ALL TABLES IN SCHEMA public TO explorer',
        '-c', 'ALTER DEFAULT PRIVILEGES FOR USER django IN SCHEMA public '
              'GRANT SELECT ON TABLES TO explorer'
    ])

    # stop the internally started postgres
    gprun(userspec='postgres', sys_exit=False, command=[
        'pg_ctl', 'stop', '-s', '-w', '-m', 'fast'
    ])
    set_files_perms()


def set_backup_perms(backup_uid, backup_gid):
    os.makedirs(os.path.join(BACKUP_DIR, 'db'), exist_ok=True)
    os.makedirs(os.path.join(BACKUP_DIR, 'files'), exist_ok=True)

    for root, dirs, files in os.walk(BACKUP_DIR):
        os.chown(root, backup_uid, backup_gid)
        os.chmod(root, 0o700)
        for f in files:
            path = os.path.join(root, f)
            os.chown(path, backup_uid, backup_gid)
            os.chmod(path, 0o600)
    os.chmod(BACKUP_DIR, 0o755)


def set_files_perms():
    os.makedirs(DATA_FILES_DIR, exist_ok=True)
    u, g = uid('django'), gid('nginx')
    for root, dirs, files in os.walk(DATA_FILES_DIR):
        os.chown(root, u, g)
        os.chmod(root, 0o2750)
        for f in files:
            path = os.path.join(root, f)
            os.chown(path, u, g)
            os.chmod(path, 0o640)


def wait_for_db():
    while True:
        silent = not DEBUG
        env = get_db_env()
        try:
            run(['psql', '-c', 'select 1'], silent=silent, env=env)
        except Exception:
            printerr('db not ready yet')
            time.sleep(1)
        else:
            printerr('db ready')
            break


def backup(
    database_format=None, files=None,
    backup_uid=None, backup_gid=None
):
    default_uid = 0  # default is root to be on the safe side
    backup_uid = uid(get_param(backup_uid, 'BACKUP_UID', default_uid))
    backup_gid = gid(get_param(backup_gid, 'BACKUP_GID', backup_uid))
    set_backup_perms(backup_uid, backup_gid)

    if database_format:
        wait_for_db()
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())
        filename = '{prefix}-db-{timestamp}.backup'
        filename = filename.format(
            prefix=BACKUP_FILE_PREFIX, timestamp=timestamp
        )
        if database_format == 'plain':
            filename += '.sql'
        filename = os.path.join(BACKUP_DIR, 'db', filename)

        cmd = ['pg_dump', '-v', '-F', database_format, '-f', filename]
        run(cmd, env=get_db_env(), log_command=True)

    if files:
        cmd = [
            'rsync', '-v', '-a', '--delete', '--stats',
            DATA_FILES_DIR, os.path.join(BACKUP_DIR, 'files/')
        ]
        run(cmd, log_command=True)

    set_backup_perms(backup_uid, backup_gid)


def restore(
    db_backup_file=None, files=None,
    drop_db=DATABASE_NAME, create_db=DATABASE_NAME, owner=DATABASE_USER
):
    if db_backup_file:
        wait_for_db()
        db_backup_file = os.path.join(BACKUP_DIR, 'db', db_backup_file)
        if db_backup_file.endswith('.backup'):
            cmd = [
                'pg_restore', '-d', 'postgres', '--exit-on-error', '--verbose',
                '--clean', '--create', db_backup_file
            ]
            run(cmd, log_command=True, env=get_db_env())
        elif db_backup_file.endswith('.backup.sql'):
            drop_db = get_param(drop_db, 'DROP_DB', 'django')
            create_db = get_param(create_db, 'CREATE_DB', drop_db)
            owner = get_param(owner, 'OWNER', 'django')
            run([
                'psql', '-U', 'postgres', '-d', 'postgres',
                '-c', 'DROP DATABASE %s' % drop_db,
                '-c', 'CREATE DATABASE %s OWNER %s' % (create_db, owner)
            ], env=get_db_env(u='postgres', d='postgres'))
            run([
                'psql', '-v', 'ON_ERROR_STOP=1', '-U', owner, '-d', create_db,
                '-f', db_backup_file
            ], env=get_db_env(u=owner, d=create_db))

    if files:
        cmd = [
            'rsync', '-v', '-a', '--delete', '--stats',
            os.path.join(BACKUP_DIR, 'files/'), DATA_FILES_DIR
        ]
        run(cmd, log_command=True)
        set_files_perms()
