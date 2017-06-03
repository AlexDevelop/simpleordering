# import fabrics API functions - self-explanatory once you see
from main.params import *
from fabric.api import *
env.hosts = [
    '{user}@{server}'.format(user=fab_user, server=fab_server)
]

def deploy_prod():
    # env['dir'] = ''
    with cd(fab_deployment_dir):
        with prefix('source venv/bin/activate'):
            run('git pull')
            run('pip install -r src/requirements.txt')
            run('python src/manage.py migrate')
            run('python src/manage.py collectstatic --noinput')
    sudo('service apache2 restart', pty=False)
