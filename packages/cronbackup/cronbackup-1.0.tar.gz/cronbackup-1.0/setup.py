import os
from setuptools import setup, find_packages

data_files = [('/usr/lib/systemd/system', ['cronbackup.service'])]
cur_directory_path = os.path.abspath(os.path.dirname(__file__))
for root, dirs, files in os.walk(cur_directory_path + '/.cronbackup'):
    _tmp_path = root[len(cur_directory_path) + 1:]
    root = os.path.join(os.getenv('HOME'), _tmp_path)
    for file in files:
        data_files.append((root, [os.path.join(_tmp_path, file)]))

setup(
    name='cronbackup',
    version='1.0',
    author='liuyang',
    url='',
    py_modules=['cronbackup'],
    unzip=False,
    data_files=data_files,
    install_requires=['apscheduler', 'pathlib'],
    entry_points={
        'console_scripts': [
            'cronbackup = cronbackup:main',
        ],
    })
