# Requirements #
You need:
  * Python 2.5 installed on current host
  * Python Imaging Library (1.1.6 recommended)
  * Django 1.1 installed on current host
  * An access to a database engine (MySQL server for example)

# Install it #
  1. Get the last tarball of [quick\_DjangoProject\_setup](http://openvolunteer.googlecode.com/files/quick_DjangoProject_setup.tar.gz)
  1. Extract the content of this tarball by:
```
tar -xzf quick_DjangoProject_setup.tar.gz 
```
  1. Go to new `ovdemo/` folder and run install script:
```
cd ovdemo
chmod +x ov_install.sh 
./ov_install.sh
```
  1. Configure the database settings in `settings.py` file:
```
DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
```
  1. run the both command to synchronize database and run a test server:
```
python manage.py syncdb
python manage.py runserver
```
  1. access to http://127.0.0.1:8000

# Deployment #
Have a look to ApacheDeployement page