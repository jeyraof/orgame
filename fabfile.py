# -*- coding: utf-8 -*-

from fabric.api import env, prefix, cd, sudo
from contextlib import contextmanager

env.user = 'root'
env.hosts = ['do.monodiary.net']

env.shell = "/bin/sh -c"

env.deploy_user = 'jaeyoung'
env.server_base = '/home/jaeyoung/orgame'
env.server_env = '%s/.venv' % env.server_base
env.server_env_activate = 'source %s/bin/activate' % env.server_env


@contextmanager
def virtualenv():
    with cd(env.server_base), prefix(env.server_env_activate):
        yield


def user_run(cmd):
    sudo(cmd, user=env.deploy_user)


def git_pull():
    with cd(env.server_base):
        user_run('git pull')


def service(name, cmd):
    sudo('service %(name)s %(cmd)s' % {'name': name, 'cmd': cmd})


def web_service(cmd):
    service('orgame', cmd)


def start_web():
    web_service('start')


def stop_web():
    web_service('stop')


def restart_web():
    web_service('restart')


def deploy():
    git_pull()
    restart_web()
