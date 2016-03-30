from fabric.api import cd, run, env
from fabvenv import virtualenv


def staging():
    projectname = 'isi-mip'

    basepath = '/srv/isi-mip.sinnwerkstatt.com/%s'

    env.hosts = ['{0}@{0}.sinnwerkstatt.com'.format(projectname)]
    env.path = basepath % projectname
    env.virtualenv_path = basepath % (projectname+'env')
    env.backup_path = basepath % 'backups'
    env.push_branch = 'staging'
    env.push_remote = 'origin'
    env.reload_cmd = 'supervisorctl restart {0}'.format(projectname)
    env.db_name = projectname
    env.db_username = projectname
    env.after_deploy_url = 'http://%s.sinnwerkstatt.com' % projectname


def production():
    pass


def reload_webserver():
    run("%(reload_cmd)s" % env)


def migrate():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py migrate --settings=config.settings.production" % env)


def ping():
    run(
        "echo %(after_deploy_url)s returned:  \>\>\>  $(curl --write-out %%{http_code} --silent --output /dev/null %(after_deploy_url)s)" % env)


def deploy():
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)
        with virtualenv(env.virtualenv_path):
            run("pip install -Ur requirements/production.txt")
            run("./manage.py collectstatic --noinput --settings=config.settings.production")

    migrate()
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
