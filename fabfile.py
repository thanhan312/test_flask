###############
### imports ###
###############

from fabric.api import cd, env, lcd, put, prompt, local, sudo, run
from fabric.contrib.files import exists


##############
### config ###
##############

local_app_dir = './test_flask'
local_config_dir = './config'

remote_app_dir = '/home'
remote_git_dir = '/home/test_flask'
remote_flask_dir = remote_app_dir + '/test_flask'
remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

env.hosts = ['news']  # replace with IP address or hostname
# env.user = 'user'
# env.password = 'blah!'

# use file ssh config detect server
env.use_ssh_config = True


#############
### tasks ###
#############


def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    if exists('/etc/supervisor/conf.d/test_flask.conf') is False:
        with lcd(local_config_dir):
            with cd(remote_supervisor_dir):
                put('./test_flask.conf', './', use_sudo=True)
                sudo('supervisorctl reread')
                sudo('supervisorctl update')


def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo('supervisorctl start test_flask')


def deploy():
    """
    1. Copy new Flask files
    2. Restart gunicorn via supervisor
    """
    """
    1. lcd = local cd (maybe :v)
    2. cd = cd
    """
    with cd(remote_flask_dir):
        run('git pull')
        sudo('supervisorctl restart test_flask')


def rollback():
    """
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        local('git push origin master')
        sudo('supervisorctl restart test_flask')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def create():
    install_requirements()
    install_flask()
    configure_nginx()
    configure_supervisor()
    configure_git()
