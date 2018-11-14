from __future__ import with_statement
from fabric.api import *


def staging():
    projectname = 'isimip'
    basepath = '/srv/isimip.brueck.io/%s'
    env.hosts = ['{0}@{0}.brueck.io'.format(projectname)]
    env.path = basepath % projectname
    env.virtualenv_path = basepath % (projectname+'env')
    env.backup_path = basepath % 'backups'
    env.push_branch = 'django-update'
    env.push_remote = 'origin'
    env.reload_cmd = 'supervisorctl restart {0}'.format(projectname)
    env.db_name = projectname
    env.db_username = projectname
    env.after_deploy_url = 'http://%s.brueck.io' % projectname


def production():
    projectname = 'isimip'
    basepath = '/webservice/isimip.org/%s'
    env.hosts = ['sws@isimip.pik-potsdam.de']
    env.path = basepath % 'htdocs'
    env.virtualenv_path = basepath % 'virtualenv'
    env.push_branch = 'master'
    env.push_remote = 'origin'
    env.db_name = projectname
    env.db_username = projectname
    env.after_deploy_url = 'http://isimip.org'
    env.reload_cmd = 'sudo supervisorctl restart isimip'



def reload_webserver():
    run("%(reload_cmd)s" % env)


def migrate():
    with prefix("source %(virtualenv_path)s/bin/activate" % env):
        run("%(path)s/manage.py migrate --settings=config.settings.production" % env)


def ping():
    run("echo %(after_deploy_url)s returned:  \>\>\>  $(curl --write-out %%{http_code} --silent --output /dev/null %(after_deploy_url)s)" % env)


def deploy():
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)
        with prefix("source %(virtualenv_path)s/bin/activate" % env):
            run("pip install -r requirements/production.txt")
            run("./manage.py collectstatic --noinput --settings=config.settings.production")

    migrate()
    reload_webserver()
    ping()


def soft_deploy():
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)

    reload_webserver()
    ping()

#
# def init_fixtures():
#     with virtualenv(env.virtualenv_path):
#         run("%(path)s/manage.py loaddata init.json" % env)
#
#
# def update():
#     ''' Only deploy and reload modules from git, do no installing or migrating'''
#     with cd(env.path):
#         run("git pull %(push_remote)s %(push_branch)s" % env)
#
#     reload_webserver()
#
#
# def backup():
#     with cd(env.backup_path):
#         run("pg_dump -U %(db_username)s %(db_name)s > %(db_name)s_backup_$(date +%%F-%%T).sql" % env)
#         run("ls -lt")
