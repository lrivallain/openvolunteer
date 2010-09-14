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
from ovsettings import *

from django.db import models
from django.conf import settings
from django.template import defaultfilters

import os
import Image


def avatar_upload(instance, filename):
    """
    Upload the avatar to a file with volunteer name for a better
    organization

    instance : (object) - current volunteer
    filename : (string) - the title of uploaded file to get extension

    # Create a test volunteer
    >>> i = Volunteer.objects.create(name='Smith',firstname='David')

    # get complete filename
    >>> cfn = avatar_upload(i, 'toto.jpg')
    >>> print cfn.split('/')[len(cfn.split('/'))-1]
    davidsmith.jpg

    # get complete filename
    >>> cfn = avatar_upload(i, 'toto.png')
    >>> print cfn.split('/')[len(cfn.split('/'))-1]
    davidsmith.png

    >>> i.firstname = 'David Dude'
    >>> cfn = avatar_upload(i, 'toto.png')
    >>> print cfn.split('/')[len(cfn.split('/'))-1]
    david-dudesmith.png

    """
    # slugify name and firstname to avoid unicode problem
    slug_firstname = defaultfilters.slugify(instance.firstname)
    slug_name = defaultfilters.slugify(instance.name)

    # test if folder is available
    path  = settings.MEDIA_ROOT + OPENVOLUNTEER_APP_NAME + '/avatars/'
    if not os.path.exists(path):
        os.mkdir(path)

    # create complete filename and remove if existing
    file = "%s%s" % (slug_firstname, slug_name)
    type = filename.split('.')[len(filename.split('.'))-1]
    complete_filename = path + file + '.' + type
    if os.path.exists(complete_filename):
        os.remove(complete_filename)

    return complete_filename


class Volunteer(models.Model):
    """
    A volunteer is a personn linked to organization. Lot of
    informations are needed to contact him.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text='Nom (Une majuscule puis des minuscules)')
    firstname = models.CharField(max_length=100, help_text='Prénom (Une majuscule puis des minuscules)')
    email = models.EmailField(blank=True, null=True, help_text='Adresse email (yyyyyy@monfai.fr)')
    phone_home = models.CharField(max_length=20, blank=True, null=True,
                                  help_text='Téléphone fixe: 2 chiffres par deux chiffres, séparés par des espaces')
    phone_mobile = models.CharField(max_length=20, blank=True, null=True,
                                    help_text='Téléphone mobile: 2 chiffres par deux chiffres, séparés par des espaces')
    address = models.TextField(blank=True, null=True, help_text='Adresse')
    birthday = models.DateField(null=True, blank=True, help_text='Date de naissance (utiliser le calendrier)')
    birth_place = models.CharField(max_length=100, help_text='Lieu de naissance', blank=True, null=True)
    social_security_number = models.BigIntegerField(help_text='Numéro de sécurité sociale (15 chiffres)', blank=True, null=True)
    avatar = models.FileField(upload_to=avatar_upload,blank=True,help_text='Photo d\'identité')
    inscription_date = models.DateField(null=True, blank=True, auto_now_add=True,
                                        help_text='Date de la première inscription dans ce fichier.')
    comments = models.TextField(blank=True, null=True)
    ca_member = models.BooleanField('Membre du CA courant?', blank=True)

    class Meta:
        ordering = ('name','firstname')

    def __unicode__(self):
        return "%s %s" % (self.name, self.firstname)

    @models.permalink
    def get_absolute_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.volunteer_details', (), {'volunteer_id': str(self.id)})

    @models.permalink
    def get_edit_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.volunteer_edit', (), {'volunteer_id': str(self.id)})

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.volunteer_delete', (), {'volunteer_id': str(self.id)})

    @models.permalink
    def get_vcard_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.volunteer_vcard', (), {'volunteer_id': str(self.id)})

    def get_photo_url(self):
        filename = self.avatar.path.split('/')[len(self.avatar.path.split('/'))-1]
        return "/media%s/avatars/%s" % (OPENVOLUNTEER_WEB_ROOT, filename)

    def save(self, *args, **kwargs):
        super(Volunteer, self).save(*args, **kwargs)
        if self.avatar:
            im = Image.open(self.avatar.name)
            size = 300, 300
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(self.avatar.name)


def affiche_upload(instance, filename):
    """
    Upload the event poster to a file with event title for a better
    organization

    instance : (object) - current volunteer
    filename : (string) - the title of uploaded file to get extension

    # Create a test volunteer
    >>> from datetime import datetime
    >>> i = Event.objects.create(title='My super Event', date=datetime.now())
    >>> i.stripped_title = 'my-super-event'

    # get complete filename
    >>> cfn = affiche_upload(i, 'toto.jpg')
    >>> print cfn.split('/')[len(cfn.split('/'))-1]
    my-super-event.jpg

    # get complete filename
    >>> cfn = affiche_upload(i, 'toto.png')
    >>> print cfn.split('/')[len(cfn.split('/'))-1]
    my-super-event.png
    """
    # test if folder is available
    path  = settings.MEDIA_ROOT + OPENVOLUNTEER_APP_NAME + '/affiches/'
    if not os.path.exists(path):
        os.mkdir(path)

    # create complete filename and remove if existing
    file = instance.stripped_title
    type = filename.split('.')[len(filename.split('.'))-1]
    complete_filename = path + file + '.' + type
    if os.path.exists(complete_filename):
        os.remove(complete_filename)

    return complete_filename

class Event(models.Model):
    """
    An event is just an event with date and place.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,help_text='Nom de l\'événement')
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de composer une url.')
    date = models.DateField(help_text='Date de l\'événement')
    place = models.CharField(max_length=100,blank=True,help_text='Lieu de l\'événement')
    affiche = models.FileField(upload_to=affiche_upload,blank=True,help_text='Affiche de l\'événement')

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_details', (), {'event_id': str(self.id)})

    @models.permalink
    def get_edit_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_edit', (), {'event_id': str(self.id)})

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_delete', (), {'event_id': str(self.id)})

    @models.permalink
    def get_comment_add_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_comment_add', (), {'event_id': str(self.id)})

    @models.permalink
    def get_need_add_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_need_add', (), {'event_id': str(self.id)})

    @models.permalink
    def get_answer_add_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_answer_add', (), {'event_id': str(self.id)})

    def get_answer_url(self):
        return "%s/answer/?v=&q=%d" % (OPENVOLUNTEER_WEB_ROOT, self.id)

    @models.permalink
    def get_positives_answer_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.answer_positives', (), {'event_id': str(self.id)})

    @models.permalink
    def get_unknown_answer_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.answer_tocontact', (), {'event_id': str(self.id)})

    def get_affiche_url(self):
        filename = self.affiche.path.split('/')[len(self.affiche.path.split('/'))-1]
        return "/media%s/affiches/%s" % (OPENVOLUNTEER_WEB_ROOT, filename)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if self.affiche:
            im = Image.open(self.affiche.name)
            size = 300, 300
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(self.affiche.name)


class Job(models.Model):
    """
    A job is a for a volunteer a work to to during an event. Manager
    can add a description an link a job to a responsible.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,help_text='Nom du poste')
    stripped_title = models.SlugField(db_index=True, max_length=255,
                                      help_text='Titre sans espaces et caractères spéciaux afin de com poser une url.')
    description = models.TextField(blank=True)
    boss = models.ManyToManyField(Volunteer,help_text='Responsables de commission',blank=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s/job/#job-%d" % (OPENVOLUNTEER_WEB_ROOT, self.id)

    @models.permalink
    def get_list_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.volunteer_byjob', (), {'job_id': str(self.id)})

    @models.permalink
    def get_edit_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.job_edit', (), {'job_id': str(self.id)})

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.job_delete', (), {'job_id': str(self.id)})


PRESENCE_CHOICES = (
    ('maybe', 'Peut-être'),
    ('yes', 'Oui'),
    ('no', 'Non'),
)


class Answer(models.Model):
    """
    An answer is the result of a request made by volunteer manager
    to see who will be present at an event. It's possible to assign
    a volunteer to a job in case of positive answer.
    """
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event,help_text='Évènement')
    volunteer = models.ForeignKey(Volunteer,help_text='Cliquez sur l\'icone pour chercher le bénévole')
    presence = models.CharField(max_length=5, choices=PRESENCE_CHOICES)
    job = models.ForeignKey(Job,null=True,blank=True,help_text='Poste')
    comments = models.TextField(blank=True,help_text='Commentaires')
    date = models.DateField(help_text='Date de la réponse',null=True,blank=True,auto_now=True)
    last_request = models.DateField(help_text='Dernière relance',null=True,blank=True)
    updating_vol_info = models.BooleanField(help_text='Fiche bénévole envoyée?',blank=True)
    updated_vol_info = models.BooleanField(help_text='Fiche bénévole retournée?',blank=True)

    class Meta:
        ordering = ('event','volunteer')

    def get_all_schedules(self):
        return Schedule.objects.filter(answer=self)

    @models.permalink
    def get_edit_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_answer_edit', (), {'answer_id': str(self.id)})

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_answer_delete', (), {'answer_id': str(self.id)})


class Need(models.Model):
    """
    A need is a number of volunteers wanted to complete a job for
    a specific event.
    """
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(help_text='Nombre de personnes nécessaire à ce poste')
    event = models.ForeignKey(Event,help_text='Évènement')
    job = models.ForeignKey(Job,help_text='Poste')

    class Meta:
        ordering = ('event','job')

    def __unicode__(self):
        return u"%s %s" % (self.event, self.job)

    @models.permalink
    def get_planning_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.need_planning', (), {'need_id': str(self.id)})

    @models.permalink
    def get_edit_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.need_edit', (), {'need_id': str(self.id)})

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.need_delete', (), {'need_id': str(self.id)})

    def get_completed_nb(self):
        return len(Answer.objects.filter(event=self.event,job=self.job,presence="yes"))

    def get_completed_status(self):
        if (self.get_completed_nb() >= int(self.number)):
            return True
        else:
            return False

    def get_positives_answers(self):
        answers = Answer.objects.filter(event=self.event,presence="yes", job=self.job)
        return answers


class Comment(models.Model):
    """
    A very simple comment system for Event details
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text='Nom et Prénom')
    email = models.EmailField(blank=True, null=True, help_text='Adresse email (yyyyyy@monfai.fr)')
    comment = models.TextField(help_text='Commentaire')
    pub_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event,help_text='Évènement')

    class Meta:
        ordering = ('pub_date',)

    def __unicode__(self):
        return "%s on %s - %0*d/%0*d%d" % (self.name, self.event, 2, self.pub_date.day,
                                           2, self.pub_date.month, self.pub_date.year)

    def get_absolute_url(self):
        return "%s#c%d" % (self.event.get_absolute_url(), self.id)

    @models.permalink
    def get_delete_url(self):
        return (OPENVOLUNTEER_APP_PREFIX + 'views.event_comment_delete', (), {'comment_id': str(self.id)})

class Schedule(models.Model):
    """
    Save schedule info for answers
    """
    id = models.AutoField(primary_key=True)
    answer = models.ForeignKey(Answer,help_text='Réponse')
    start = models.DateTimeField()
    end = models.DateTimeField()
    next_day = models.BooleanField(help_text='Jour suivant?',blank=True)

    class Meta:
        ordering = ('next_day', 'start','end')

    @models.permalink
    def get_delete_url(self):
         return (OPENVOLUNTEER_APP_PREFIX + 'views.schedule_delete', (), {'schedule_id': str(self.id)})
