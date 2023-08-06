# Install OpenLDAP and LDAP utilities

```
    sudo apt-get install slapd ldap-utils
```
Debian package manager will create a new DB for you with the top entry being you domainname broken up in domain components. For the domain 'example.com' this will be `dc=example,dc=com`. The package manager will also ask to set the admin password for the DB. This password should be the same you have set in the secret.ini config file.
You can check that LDAP service is working by listing the entries created by the installation:

```
    ldapsearch -H ldap://localhost -b "dc=example,dc=com" -D "cn=admin,dc=example,dc=com" -W
```
If the above command does not succeed you can check the details of the DB created using this command:

```
    sudo cat /etc/ldap/slapd.d/cn\=config/olcDatabase\=\{1\}mdb.ldif
```
`olcSuffix` value is your top entry and what should be used for `-b` parameter in the ldapsearch command. `olcRootDN` value should be used for `-D` parameter. The `-W` tells ldapsearch to prompt for password.

Modify the `reg_bases.ldif` to match your domain values and add the LDAP entries that will hold the groups and the people:

```
    ldapadd -H ldap://localhost -D "cn=admin,dc=example,dc=com" -W -f /opt/purist/middleware_virtualenv/config_sample/ldap/reg_bases.ldif
```

This gives you a very basic LDAP environment suitable for development. Remember to set `AUTH_LDAP_START_TLS=False` in config.ini as this LDAP server has not been configured for TLS communication.
