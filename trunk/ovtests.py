#-*- coding: utf-8 -*-
from demo.openvolunteer.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime


RESULTS_STORAGE = []
@login_required(redirect_field_name='next')
def list_volunteer_index(request):
    """Display a form to generate a filtered list of volunteers"""
    if request.method == 'GET':
        print "0"
        return render_to_response('openvolunteer/list_volunteer_form.html',{},context_instance=RequestContext(request))
    elif request.method == 'POST':
        volunteers = Volunteer.objects.all()
        #volunteers = "fiozejfiojzefoj"
        print "1"
        try:
            filter = request.REQUEST["filter_address"]
            volunteers = volunteers.exclude(address="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_phone"]
            volunteers = volunteers.exclude(phone_home="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_mobile"]
            volunteers = volunteers.exclude(phone_mobile="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_email"]
            volunteers = volunteers.exclude(email="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_ca"]
            volunteers = volunteers.exclude(ca_member="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_old"]
            print filter
            if (filter == 'on'):
                limit = datetime.date.today()
                limit = limit.replace(limit.year-18)
                # to be tested and checked!!!!!!!!
                volunteers = volunteers.exclude(birthday__gt=limit)
        except:
            pass
        try:
            filter = request.REQUEST["filter_name"]
            print "2"
            search_terms=filter.split(' ')
            print search_terms
            for term in search_terms:
                print term
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term)).all()
        except:
            pass

            # get display fields
            #if (request.GET["display_address"] == "on"):
            #    form_display_address = True
            #else:
            #    form_display_address = False
            # 
            #if (request.GET["display_email"] == "on"):
            #    form_display_email = True
            #else:
            #    form_display_email = False
            # 
            #if (request.GET["display_phone1"] == "on"):
            #    form_display_phone1 = True
            #else:
            #    form_display_phone1 = False
            #
            #if (request.GET["display_phone2"] == "on"):
            #    form_display_phone2 = True
            #else:
            #    form_display_phone2 = False
            #
            #if (request.GET["display_ca"] == "on"):
            #    form_display_ca = True
            #else:
            #    form_display_ca = False
            #
            #if (request.GET["display_birth"] == "on"):
            #    form_display_birth = True
            #else:
            #    form_display_birth = False
            #
            #if (request.GET["display_incr"] == "on"):
            #    form_display_incr = True
            #else:
            #    form_display_incr = False
        print "7"
        global RESULTS_STORAGE
        RESULTS_STORAGE = volunteers
        print RESULTS_STORAGE
        return render_to_response('openvolunteer/list_volunteer_form.html',
                              {'volunteers': volunteers},
                              context_instance=RequestContext(request))




import csv
from django.http import HttpResponse
from django.template import loader, Context
def csv_generator(request):
    '''Generate a csv file for OOo import'''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=volunteer_list.csv'

    #writer = csv.writer(response)
    #writer = UnicodeWriter(response, quoting=csv.QUOTE_ALL)
    #writer.writerow(['Nom', 'Prenom', 'Email', 'Telephone fixe', 'Mobile', 'Naissance', 
    #                 'Inscription', 'Membre du CA?'])
    print "CSV"
    print RESULTS_STORAGE

    t = loader.get_template('openvolunteer/exportVolunteer.csv')
    c = Context({
        'volunteers': RESULTS_STORAGE,
    })
    response.write(t.render(c))

    #for volunteer in RESULTS_STORAGE:
        #writer.writerow([volunteer.name, volunteer.firstname, volunteer.email,
        #                 volunteer.phone_home, volunteer.phone_mobile, volunteer.birthday,
        #                 volunteer.inscription_date, volunteer.ca_member])
        #writer.writerow(volunteer)
    return response
