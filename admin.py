#-*- coding: utf-8 -*-
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
