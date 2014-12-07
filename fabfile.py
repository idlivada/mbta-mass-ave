from fabric.api import run, cd, env, sudo, prompt
from fabric.contrib.files import exists, upload_template

env.hosts = ['root@162.243.102.184']

rootdir = "/var/www/"
homedir = rootdir + "mbta-mass-ave/"
apache_conf = '/etc/apache2/sites-enabled/mbta-mass-ave.conf'

def install():
    run("apt-get install -y --no-upgrade python-pip build-essential git libmysqlclient-dev apache2 python-dev libapache2-mod-wsgi", shell=False)
    run("pip install --upgrade pip")
    run("pip install virtualenv")
    install_code()

def install_code():
    if not exists(homedir+".git/"):
        with cd(rootdir):
            run("git clone https://github.com/idlivada/mbta-mass-ave.git")

    with cd(homedir):
        run("git pull")
        run("virtualenv env --no-site-packages")
        run("source %s/env/bin/activate && pip install -r %s/requirements.txt" % (homedir, homedir))
        
        if not exists(apache_conf):
            domain = prompt('Enter domain (e.g. mbta.example.com):')
            apache_context = {'homedir' : homedir, 'servername' : domain}
            upload_template(filename='vhost.conf.jinja', destination=apache_conf, 
                            use_jinja=True, context=apache_context)
            
    apache_restart()

def apache_restart():
    sudo("service apache2 restart")
