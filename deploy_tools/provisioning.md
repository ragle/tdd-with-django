Provisioning a new site
=======================

## required packages

*  nginx
*  Python 3
*  git
*  pip
*  virtualenv

Debian-like systems: 

`sudo apt-get install nginx git python3 python3-pip`
`pip3 install --user virtualenv`
`pip3 install --user virtualenvwrapper`

Add to `~/.bashrc`:

```bash
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source ~/.local/bin/virtualenvwrapper.sh
```

## nginx virtual host config

*  `$ cp nginx.conf /etc/nginx/sites-available/SITENAME`
*  Edit conf file to refect project paths
*  `$ ln -s /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/SITENAME`
*  `$ sudo service nginx reload`

## Upstart / gunicorn

*  `cp gunicorn-upstart.template.conf /etc/init/SITENAME.conf`
*  edit conf file to reflect project paths
*  sudo start SITENAME
