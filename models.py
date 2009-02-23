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
from bigint import BigIntegerField

def avatar_upload(instance, filename):
    '''create a file with volunteer name to a better oarganization'''
    type = filename.split('.')[len(filename.split('.'))-1]
    path = settings.MEDIA_ROOT + '/openvolunteer/avatars/'
    file = "%s%s" % (instance.firstname, instance.name)
    return path + file + '.' + type

# Create your models here.
class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text='Nom (Une majuscule puis des minuscules)')
    firstname = models.CharField(max_length=100, help_text='Prénom (Une majuscule puis des minuscules)')
    email = models.EmailField(blank=True, help_text='Adresse email (yyyyyy@monfai.fr)')
    phone_home = models.CharField(max_length=20,blank=True,
                                  help_text='Téléphone fixe: 2 chiffres par deux chiffres, séparés par des espaces')
    phone_mobile = models.CharField(max_length=20,blank=True,
                                    help_text='Téléphone mobile: 2 chiffres par deux chiffres, séparés par des espaces')
    address = models.TextField(blank=True, help_text='Adresse')
    birthday = models.DateField(null=True, blank=True, help_text='Date de naissance (utiliser le calendrier)')
    birth_place = models.CharField(max_length=100, help_text='Lieu de naissance',blank=True)
    social_security_number = BigIntegerField(help_text='Numéro de sécurité sociale (15 chiffres)', blank=True, null=True)
    avatar = models.FileField(upload_to=avatar_upload,blank=True,help_text='Photo d\'identité')
    inscription_date = models.DateField(null=True, blank=True,
                                        help_text='Date de la première inscription dans ce fichier.')
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
    title = models.CharField(max_length=100,help_text='Nom de l\'événement')
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de composer une url.')
    date = models.DateField(help_text='Date de l\'événement')
    place = models.CharField(max_length=100,blank=True,help_text='Lieu de l\'événement')
    affiche = models.FileField(upload_to=affiche_upload,blank=True,help_text='Affiche de l\'événement')
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/openvolunteer/event/%d" % self.id
    def get_affiche_url(self):
        filename = self.affiche.path.split('/')[len(self.affiche.path.split('/'))-1]
        return "/media/openvolunteer/affiches/%s" % filename


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,help_text='Nom du poste')
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de com poser une url.')
    description = models.TextField(blank=True)
    boss = models.ManyToManyField(Volunteer,help_text='Responsables de commission',blank=True)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/openvolunteer/job/%s#%s" % (self.stripped_title, self.stripped_title)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event,help_text='Évènement')
    volunteer = models.ForeignKey(Volunteer,help_text='Cliquez sur l\'icone pour chercher le bénévole')
    presence = models.BooleanField('Sera présent comme bénévole?',blank=True)
    job = models.ForeignKey(Job,null=True,blank=True,help_text='Poste')
    comments = models.TextField(blank=True,help_text='Commentaires')
    date = models.DateField(help_text='Date de la réponse',null=True,blank=True)
    last_request = models.DateField(help_text='Dernière relance',null=True,blank=True)


class Need(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(help_text='Nombre de personnes nécessaire à ce poste')
    event = models.ForeignKey(Event,help_text='Évènement')
    job = models.ForeignKey(Job,help_text='Poste')
       
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
