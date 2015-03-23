# Introduction #
This page is a draft way to setup OpenVolunteer on an existing Django project. It describes the prerequisite of setup, configuration of application.

There is no instruction to setup Django, but you can found more details for this step in  [this page](http://docs.djangoproject.com/en/dev/intro/install/) on the official django web site.

# Get openvolunteer #
## Prerequisites ##
  * Python v2.5
    * _[Download Python v2.5](http://www.python.org/download/releases/2.5.4/)_
    * _python-mysqldb library installed._
  * Django >= v1.0 (recommended: v1.1) installation **with admin interface**, **authentication** and **static file access** enabled
    * _[Download Django\_v1.1](http://www.djangoproject.com/download/1.1/tarball/)_
    * _[Setup documentation](http://docs.djangoproject.com/en/dev/intro/install/)_
    * _[HowTo enable admin interface](http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin)_
    * _[HowTo configure static file access](http://docs.djangoproject.com/en/dev/ref/settings/#media-root)_
    * _[HowTo setup authentication](http://docs.djangoproject.com/en/dev/topics/auth/#topics-auth)_
  * Python Imaging Library (provided in packages mirrors of most of commons Linux based distributions)
    * _[Download PIL 1.1.6](http://effbot.org/downloads/Imaging-1.1.6.tar.gz)_
    * Run `python setup.py install` to setup

## Install it ##
  1. Get the last tarball of OpenVolunteer in [download section](http://openvolunteer.googlecode.com/files)
  1. Extract the content of this tarball by:
```
tar -xzf openvolunteer_v0.2.tar.gz 
```
  1. Move openvolunteer folder to django project folder by:
```
mv openvolunteer /path/to/django/MyProject/
```
  1. In the dir MyProject settings file (`settings.py`)
    1. add `'openvolunteer',` to  `INSTALLED_APPS`.
    1. add `'openvolunteer.context_processors.settings',` to `TEMPLATE_CONTEXT_PROCESSORS`
    1. add `/path/to/django/MyProject/openvolunteer/templates',` to `TEMPLATE_DIRS`
  1. In the project url file (urls.py), add the following line to urlpatterns (according to project name):
```
(r'^openvolunteer/', include('MyProject.openvolunteer.urls')),
```
  1. create an `openvolunteer` folder at the media root path
```
mkdir media/openvolunteer/
```

## Configure it ##
  1. In `openvolunteer` folder, open the `ovsettings.py` file.
  1. Change the folowing lines according to the current project, app and path:
```
OPENVOLUNTEER_PROJ_NAME   = "MyProject"
OPENVOLUNTEER_APP_NAME    = "openvolunteer"
OPENVOLUNTEER_PROJ_ROOT   = "/path/to/django/MyProject"
```

## Test it ##
  1. From project folder, launch the creation of mysql tables:
> > ` python manage.py syncdb `
  1. From project folder, launch the django development server:
> > ` python manage.py runserver `
  1. Open the http://127.0.0.1:8000/openvolunteer/ link in a web browser.

# Deployment #
Have a look to ApacheDeployement page