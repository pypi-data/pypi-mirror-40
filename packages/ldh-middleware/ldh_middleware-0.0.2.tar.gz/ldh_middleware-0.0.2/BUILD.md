# Building a deb package #

This file details the steps that need to be taken to build a Debian
package.  We used Debian Stretch to build the package but using any
other Debian based distribution should generate a valid package for
that distribution.

Install Ruby packages and configure the user environment for Ruby 2.4.0:

```
$ sudo apt-get install rbenv ruby-build
$ rbenv install 2.4.0
$ rbenv global 2.4.0
```

Install FPM gem:

```
$ rbenv exec gem install fpm
```

Install the tools needed to create a virtual environment and install
LDH from PyPI:

```
$ sudo apt-get install python3-pip virtualenv libsasl2-dev libldap2-dev libssl-dev
$ sudo pip3 install virtualenv-tools3
$ pip3 install --user setuptools
```

Now we can build a Debian package from the LDH version available in PyPI by running:

```
$ make debpypi
```

or we can build a Debian package with the sources available in our directory by running:

```
$ make debsource
```

After a successful execution you will get a `ldh-middleware_<VERSION>_amd64.deb` file.
