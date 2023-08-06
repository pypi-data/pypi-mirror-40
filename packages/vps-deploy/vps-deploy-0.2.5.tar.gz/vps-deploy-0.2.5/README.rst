==========
VPS Deploy
==========

This Python package contains a number of Fabric 1.x deployment functions that I use
across various web-related projects.


Getting started
---------------

I prefer to install Fabric as a system package::

  $ sudo apt install fabric
  $ pip install --user --no-deps vps-deploy

Alternately, just install with pip::

  $ pip install --user vps-deploy

Fabric is a neat tool for automating deployment processes. To get started,
create a `fabfile.py` in your top-level project directory. It might look
something like this:

.. code:: python

    from fabric.api import env

    from vps_deploy.django_fabric import (
        fix_permissions, flush_memcached, grep_for_pdb, lint, prepare_django,
        prepare_virtualenv, reload_uwsgi, transfer_files_git, update_nginx)

    env.user = 'web'
    env.hosts = ['example.com']
    env.app_user = 'www-data'
    env.project_dir = '/home/web/example'
    env.virtualenv = '/home/web/.virtualenvs/example-django-py34'
    env.site_name = 'example'
    env.requirements = 'project/requirements.txt'
    env.settings = 'project.settings.live'
    env.uwsgi_conf = 'deploy/uwsgi.ini'
    env.nginx_conf = 'deploy/nginx.conf'
    env.python = '/home/web/local/bin/python3.4'

    def deploy():
        """Install or deploy updates to this website."""

        grep_for_pdb()
        lint()
        transfer_files_git()
        prepare_virtualenv()
        prepare_django()
        fix_permissions(
            read=['deploy', 'project'],
            read_write=['project/media'])
        reload_uwsgi()
        flush_memcached()
        update_nginx()


Deploying
---------

To update your live deployment, run:

`fab deploy`

Obviously you'll need a few things in this depends on a few things; such as
having SSH access to the server, having installed Nginx, uWSGI Emperor, Python,
Memcached, a database etc. These are mostly thing you'll set up once with
relatively vanilla settings and share across multiple projects.
