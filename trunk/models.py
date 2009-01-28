#-*- coding: utf-8 -*-
"""
    ---------------------------------------------------------------------------

                               OpenVolunteer
                     Copyright 2009, Ludovic Rivallain

    ---------------------------------------------------------------------------
    This file is part of OpenVolunteer.

    OpenVolunteer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenVolunteer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with OpenVolunteer.  If not, see <http://www.gnu.org/licenses/>.
    ---------------------------------------------------------------------------
"""

from django.db import models
from django.conf import settings
from django.utils.dates import *

def avatar_upload(instance, filename):
    '''create a file with volunteer name to a better oarganization'''
    type = filename.split('.')[len(filename.split('.'))-1]
    path = settings.MEDIA_ROOT + '/openvolunteer/avatars/'
    file = "%s%s" % (instance.firstname, instance.name)
    return path + file + '.' + type

# Create your models here.
class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_home = models.CharField(max_length=20,blank=True)
    phone_mobile = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    avatar = models.FileField(upload_to=avatar_upload,blank=True)
    inscription_date = models.DateField(help_text='Première inscription dans ce fichier le:',null=True, blank=True)
    comments = models.TextField(blank=True)
    ca_member = models.BooleanField('Membre du CA courant?',blank=True)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.name)
        
    def get_absolute_url(self):
        return "/openvolunteer/volunteer/%d" % self.id
        
    def get_photo_url(self):
        filename = self.avatar.path.split('/')[len(self.avatar.path.split('/'))-1]
        return "/media/openvolunteer/avatars/%s" % filename

def affiche_upload(instance, filename):
    '''create a file with event title to a better oarganization'''
    type = filename.split('.')[len(filename.split('.'))-1]
    path = settings.MEDIA_ROOT + '/openvolunteer/affiches/'
    file = instance.stripped_title
    return path + file + '.' + type

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de com poser une url.')
    date = models.DateField()
    place = models.CharField(max_length=100,blank=True)
    volunteers = models.ManyToManyField(Volunteer,blank=True)
    affiche = models.FileField(upload_to=affiche_upload,blank=True)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/openvolunteer/event/%d" % self.id
    def get_affiche_url(self):
        filename = self.affiche.path.split('/')[len(self.affiche.path.split('/'))-1]
        return "/media/openvolunteer/affiches/%s" % filename


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de com poser une url.')
    description = models.TextField(blank=True)
    boss = models.ManyToManyField(Volunteer, help_text='Responsables de commission', blank=True)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/openvolunteer/job/%s#%s" % (self.stripped_title, self.stripped_title)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event)
    volunteer = models.ForeignKey(Volunteer)
    presence = models.BooleanField('Sera présent comme bénévole?',blank=True)
    job = models.ForeignKey(Job,null=True,blank=True)
    comments = models.TextField(blank=True)
    date = models.DateField(help_text='Date de la réponse',null=True,blank=True)
    last_request = models.DateField(help_text='Dernière relance',null=True,blank=True)


class Need(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    event = models.ForeignKey(Event)
    job = models.ForeignKey(Job)
       
    def __unicode__(self):
        return u"%s %s" % (self.event, self.job)
    def get_completed_nb(self):
        answers = Answer.objects.filter(event=self.event,job=self.job,presence=True).all()
        return len(answers)
    def get_completed_status(self):
        a = len(Answer.objects.filter(event=self.event,job=self.job,presence=True).all())
        b = int(self.number)
        if (a >= b):
            return True
        else:
            return False
