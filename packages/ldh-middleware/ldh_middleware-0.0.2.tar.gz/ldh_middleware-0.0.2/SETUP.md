Prerequisites
-------------

* Debian 9
* Python 3.5
* Django 1.11 (included in Python packages below)
* Nginx
* RabbitMQ server
    * Must be accessible at `amqp://guest:guest@localhost:5672//`
    * This can be achieved with just `apt install rabbitmq-server`
* Additional dependencies (Debian package names):
    * `libsasl2-dev`
    * `libldap2-dev`
    * `libssl-dev`
    * `python3-dev`
    * `supervisor`
    * `uwsgi`
    * `uwsgi-emperor`
    * `uwsgi-plugin-python3`
    * `virtualenv`
* Python/Django dependencies: see `requirements.txt`
* External resources:
    * LDAP database
    * WooCommerce instance
      * [REST API enabled](https://docs.woocommerce.com/document/woocommerce-rest-api/)
      * [WooCommerce Subscriptions](https://woocommerce.com/products/woocommerce-subscriptions/)
      * [JWT Authentication for WP REST API](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/)
    * OpenVPN instance (SSH access)
      * Including [openvpn-confgen](https://code.puri.sm/liberty/openvpn_confgen)
      * Typically, the Nginx user (`www-data`) will need SSH access
      * Test with `sudo -u www-data ssh -p PORT REMOTE_USER@HOSTNAME`
      * The user needing access can be changed in
        `purist_middleware_monitor.conf`

Other versions and alternatives may work but are untested.

Setup
-----

* Install Debian packages:

    ```
    $ sudo apt-get install python3-pip virtualenv libsasl2-dev libldap2-dev
    ```

* Create installation folders:

    * `/opt/purist/middleware/` (code)
    * `/opt/purist/middleware_virtualenv/` (Python environment)
    * `/etc/opt/purist/middleware/` (configuration)
    * `/var/opt/purist/middleware/static/` (data and static web files)
    * `/var/log/purist/middleware/` (logs)
    * `/var/opt/purist/brand/` (shared data and static web files)
    * `/var/opt/purist/downloads` (downloads area)
    
    ```
    $ sudo sh -c 'for i in /opt/purist/middleware/ \
        /opt/purist/middleware_virtualenv/ \
        /etc/opt/purist/middleware/ \
        /var/log/purist/middleware/ \
        /var/opt/purist/middleware/static/ \
        /var/opt/purist/brand/ \
        /var/opt/purist/downloads; do mkdir -p $i; done'
    ```
* Populate brand data (if is not populated already)

* Set up virtualenv:
    
    * Create virtualenv (`sudo virtualenv /opt/purist/middleware_virtualenv --python=python3`)
    * Become root `sudo -i`
    * Activate virtualenv (`source /opt/purist/middleware_virtualenv/bin/activate`)
    * Install LDH from PyPI (`pip install ldh_middleware`)

* Copy sample config files to their respective locations:

    ```
    cp $VIRTUAL_ENV/config_sample/ldh_middleware/config.ini /etc/opt/purist/middleware/
    cp $VIRTUAL_ENV/config_sample/ldh_middleware/secret.ini /etc/opt/purist/middleware/
    cp $VIRTUAL_ENV/config_sample/ldh_middleware/link_profile.strict.yml /etc/opt/purist/middleware/
    ```
    * Modify those files to fit your site needs. You will need to set `DEBUG_ALL_ACCESS=False` in config.ini if your OpenVPN is not fully configured. You can generate a good `DJANGO_SECRET_KEY` in secret.ini using the command `openssl rand -hex 48`.
* Run initial setup:
    * `ldh_middleware collectstatic`
    * `ldh_middleware migrate`
    * Create the superuser. This requires a working LDAP configuration/environment. You can get a basic LDAP server running following instructions in [BASIC_LDAP.md](BASIC_LDAP.md). Once you have a working LDAP server you can run:
    * `ldh_middleware createsuperuser`
    * Deactivate virtualenv (`deactivate`)
    * Exit root user (`exit`)

* Install and configure Supervisor:

    * Supervisor will spawn a Celery worker, therefore we need a working RabbitMQ server. You can install a basic RabbitMQ server in Debian running: `sudo apt-get install rabbitmq-server`.
    * Install Supervisor, copy the config file and restart it:

    ```
        sudo apt-get install supervisor
        sudo cp /opt/purist/middleware_virtualenv/config_sample/supervisor/purist_middleware_monitor.conf /etc/supervisor/conf.d/
        sudo systemctl restart supervisor
    ```

    * You should see some activity on the celery log file in /var/log/purist/middleware/beat.log

* Install and configure uWSGI:

    ```
        sudo apt-get install uwsgi uwsgi-emperor uwsgi-plugin-python3
        sudo cp /opt/purist/middleware_virtualenv/config_sample/uwsgi_emperor_vassals/purist_middleware.ini /etc/uwsgi-emperor/vassals/
        sudo chown www-data:www-data /var/log/uwsgi/app
        sudo chown --recursive www-data:www-data /var/opt/purist
        sudo systemctl restart uwsgi-emperor
    ```

    * You should see some activity on the vassal log: /var/log/uwsgi/app/purist_middleware.log

* Install and configure Nginx:

    ```
        sudo apt-get install nginx
        sudo cp /opt/purist/middleware_virtualenv/config_sample/nginx/purist_middleware /etc/nginx/sites-available/
    ```

    * Modify `/etc/nginx/available_sites/purist_middleware` file changing `server_name` values accordingly. You will also need a working SSL certificate for your host. Once you have that enable the site:

    ```
        sudo ln --symbolic /etc/nginx/sites-available/purist_middleware /etc/nginx/sites-enabled/
        sudo systemctl restart nginx
    ```

Now point your web browser to https://example.com (obviously replacing example.com by your domain) and you should see LDH up and running. Try to login with the super user you created with `ldh_middleware createsuperuser`.

If the site does not work check the logs for errors:

* `/var/log/nginx/access.log`
* `/var/log/nginx/error.log`
* `/var/log/purist/middleware/beat.log`
* `/var/log/supervisor/supervisord.log`
* `/var/log/uwsgi/emperor.log`
* `/var/log/uwsgi/app/purist_middleware.log`

For more options and details see
<https://docs.djangoproject.com/en/1.11/#the-development-process>

Configure
---------

* Log in to admin interface as superuser
* Define intervals in Django_Celery_Beat > Intervals
* Define periodic tasks in Django_Celery_Beat > Periodic tasks
* Define known products in Limit Monitor > External bundles

Update
------

* Stop site
* Update packages with `apt update && apt upgrade`
* Update code in `/opt/purist/middleware/`
* Update settings in `/etc/opt/purist/middleware/`
* Update virtualenv:
    * Activate virtualenv (`./bin/activate.py`)
    * Update Python packages (`pip install  --requirement requires/requirements.txt`)
    * Do not use `pip install --update` as this will not respect requirements
* Update site:
    * Run `./manage.py collectstatic`
    * Run `./manage.py migrate` (see **Migrations** below)
* Start site

Migrations
----------

This is a workaround for [django-ldapdb issue #155](https://github.com/django-ldapdb/django-ldapdb/issues/115).

If you need to make a new migration:

* Open `ldapregister.0003_ldapgroup_ldapperson`
* Switch `LdapGroup.cn` and `LdapPerson.uid` from non-primary to primary
* Run `makemigrations`
* Switch `LdapGroup.cn` and `LdapPerson.uid` back to non-primary
* If you have just added a new LDAP table, switch `NewTable.key` to
  non-primary too
* Run `migrate`

You only need to do this when creating new migrations (`makemigrations`)
not when running existing migrations (`migrate`).

Usage
-----

See [README.md](README.md)
