# Apache Prerequisites #
Need an apache2 with mod\_wsgi enabled (`a2enmod mod_wsgi`)

# Configuration #
  1. Create a file `apache.wsgi` with:
```
import os
import sys

# fix a restriction of mod_wsgi:
sys.stdout = sys.stderr

# /path/to/django/MyProject without MyProject !!!
sys.path.append('/path/to')

# Change following line according to your project name
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyProject.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```
  1. Apache2 configuration sample for a virtual host:
```
NameVirtualHost *:80
<VirtualHost *:80>
    ServerName host.domain.tld
    ServerAdmin webmaster@host.domain.tld
    DocumentRoot /var/www/

    WSGIScriptAlias / /path/to/django/MyProject/apache.wsgi

    Alias "/media" "/path/to/django/MyProject/media/"
    <Location "/media">
        SetHandler None
    </Location>

    Alias "/admin_media" "/usr/lib/python2.5/site-packages/django/contrib/admin/media/"
    <Location "/admin_media">
        SetHandler None
    </Location>
</VirtualHost>
```
  1. Reload apache configuration:
```
/etc/init.d/apache force-reload
```