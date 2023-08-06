# coding: utf-8
"""
备份目录结构:
$ tree /tmp/cronbackup/

/tmp/cronbackup/
├── mysql_backup
│   ├── mysql_backup_20190114_180644
│   │   └── mysqldump.sql
│   └── mysql_backup_20190114_180649
│       └── mysqldump.sql
└── postgresql_backup
    ├── postgresql_backup_20190114_180644
    │   └── postgresqldump.sql
    └── postgresql_backup_20190114_180649
        └── postgresqldump.sql
"""
import json
import logging
import os
import pathlib
import shutil
import subprocess
from datetime import date, datetime
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BlockingScheduler

FILE_FORMAT = ("[%(asctime)s.%(msecs)03d][%(pathname)s:%(funcName)s]"
               "[%(levelname)s] %(message)s")
LOG = logging.getLogger(__name__)
CONFIG_DIR = os.path.join(os.getenv('HOME'), '.cronbackup')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'cronbackup.json')
BACKUP_FILE_FORMAT = '%Y%m%d_%H%M%S'


def log_init():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    root = logging.getLogger()
    level = config.get('log_level')
    root.setLevel(level)

    log_file = config.get('logfile')
    log_max_size = config.get('logfile_size') * 1024 * 1024
    log_backup_count = config.get('logfile_backup_count')
    fh = RotatingFileHandler(
        log_file, maxBytes=log_max_size, backupCount=log_backup_count)
    fh.setFormatter(
        logging.Formatter(fmt=FILE_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))
    root.addHandler(fh)


def gen_task(backup_dir, sync_config, task_config):
    name = task_config.get('name')
    description = task_config.get('description')
    backup_script_path = task_config.get('backup_script_path')
    keep_time = task_config.get('keep_time')
    issync = task_config.get('sync')
    LOG.info('exec cronbackup task: %s' % name)
    # 执行脚本
    task_backup_dir = os.path.join(backup_dir, name)
    _backup_dir = os.path.join(
        task_backup_dir,
        '%s_%s' % (name, datetime.now().strftime(BACKUP_FILE_FORMAT)))
    pathlib.Path(_backup_dir).mkdir(parents=True, exist_ok=True)
    new_env = os.environ.copy()
    new_env['BACKUP_DIR'] = _backup_dir

    cmd = 'sh %s' % os.path.join(CONFIG_DIR, backup_script_path)
    # TODO: output to logging
    LOG.info('start clean cronbackup(%s) file' % name)
    proc = subprocess.Popen(cmd, shell=True, env=new_env)
    proc.wait()
    # 检查文件并清理过期
    now = datetime.now()
    data_files = os.listdir(task_backup_dir)
    for data_file in data_files:
        time = data_file[-15:]
        _datetime = datetime.strptime(time, BACKUP_FILE_FORMAT)
        if (now - _datetime).days >= keep_time:
            # if (now - _datetime).seconds >= keep_time:
            LOG.info('clean cronbackup(%s) file: %s' % (name, data_file))
            shutil.rmtree(
                os.path.join(task_backup_dir, data_file), ignore_errors=True)
    # 远程同步
    if not issync:
        return
    LOG.info("start sync cronbackup(%s) file" % name)
    remote_server = sync_config.get('remote_server')
    remote_user = sync_config.get('remote_user')
    remote_dir = sync_config.get('remote_dir')
    cmd = 'rsync -avz --delete {task_backup_dir}/ {remote_user}@{remote_server}:/{remote_dir}/{task_name}'.format(
        task_backup_dir=task_backup_dir,
        remote_user=remote_user,
        remote_server=remote_server,
        remote_dir=remote_dir,
        task_name=name)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    LOG.info("end sync cronbackup(%s) file" % name)


def main():
    log_init()

    LOG.info('init cronbackup...')
    scheduler = BlockingScheduler()

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    backup_config = config.get('backup')
    backup_dir = backup_config.get('backup_dir')
    backup_hour = backup_config.get('hour')
    backup_minute = config.get('minute')
    sync_config = config.get('sync')
    for task_config in config.get('tasks'):
        if not task_config.get('enable'):
            continue
        LOG.info('gen cronbackup task: %s' % task_config.get('name'))
        scheduler.add_job(
            gen_task,
            'cron',
            # 'interval',
            seconds=5,
            args=(backup_dir, sync_config, task_config),
            day_of_week='0-6',
            hour=backup_hour,
            minute=backup_minute)

    scheduler.start()


if __name__ == "__main__":
    main()
