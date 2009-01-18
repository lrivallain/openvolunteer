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
from demo.openvolunteer.models import *
from django.contrib import admin

class VolunteerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations personnelles', {'fields': ('name','firstname','birthday')}),
        ('Coordonnées', {'fields': ('phone_home','phone_mobile','email','address')}),
        ('Divers', {'fields': ('avatar','inscription_date','ca_member','comments')}),
    )
    list_display = ('name','firstname','email','phone_home','phone_mobile','ca_member')
    search_fields = ['name','firstname','email','phone_home','phone_mobile','ca_member']
    list_filter = ['ca_member']


class EventAdmin(admin.ModelAdmin):
    fields = ('title','stripped_title','date','place','affiche')
    list_display = ('title','date','place')
    list_filter = ['date']
    date_hierarchy = 'date'
    prepopulated_fields = {"stripped_title": ("title",)}
    search_fields = ['title','date']


class JobAdmin(admin.ModelAdmin):
    fields = ('title','stripped_title','description','boss')
    list_display = ('title',)
    list_filter = ['boss']
    prepopulated_fields = {"stripped_title": ("title",)}
    search_fields = ['title','boss']
    

class AnswerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Qui? Où? Quand?', {'fields': ('event','volunteer','job')}),
        ('Contacts', {'fields': ('presence','date','last_request')}),
        ('Divers', {'fields': ('comments',)}),
    )
    list_display = ('event','volunteer','presence','job')
    list_filter = ['event']
    search_fields = ['event','volunteer']

class NeedAdmin(admin.ModelAdmin):
    fields = ('event','job','number')
    list_filter = ['event']
    list_display = ('event','job','number')
    search_fields = ['event','job']

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Need, NeedAdmin)
