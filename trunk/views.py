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
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime

@login_required(redirect_field_name='next')
def index(request):
    """Open volunteers home page - Display links to main pages"""
    volunteers = Volunteer.objects.all().order_by('?')[:10]
    events = Event.objects.all().order_by('-date')[:10]
    answers = Answer.objects.all().order_by('-date')[:10]
    jobs = Job.objects.exclude(title="none").all().order_by('?')[:10]
    return render_to_response('openvolunteer/index.html',
                              {'volunteers':volunteers,
                               'events':events,
                               'answers':answers,
                               'jobs':jobs},
                               context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def volunteer_index(request):
    """Display a search form (and a list of volunteers)"""
    try:
        query = request.GET["q"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query == "" or query == " ":
            return render_to_response('openvolunteer/volunteer_index.html',
                                      {'results': [], 'terms': ""},
                                      context_instance=RequestContext(request))
        else:
            search_terms=query.split(' ')
            # get all volunteers
            volunteers = Volunteer.objects.all()
            for term in search_terms:
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term)|
                                               Q(email__icontains = term)|
                                               Q(phone_home__icontains = term)|
                                               Q(phone_mobile__icontains = term)).all().order_by('name')
    # If there is no 'q' value, return empty results
    except:
        volunteers = []
        query = ""
    return render_to_response('openvolunteer/volunteer_index.html',
                              {'results': volunteers, 'terms': query},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def volunteer_details(request, volunteer_id):
    """Display volunteer details and link to modify them"""
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        error_message = ''
    except:
        volunteer = ""
        error_message = 'Aucun bénévole ne correspond à votre requête.'
    return render_to_response('openvolunteer/volunteer_details.html',
                              {'volunteer': volunteer,
                               'error_message': error_message},
                              context_instance=RequestContext(request))


from  ovvcard import _vcard_string
@login_required(redirect_field_name='next')
def volunteer_vcard(request,vcard_type, volunteer_id):
    """View function for returning single vcard"""
    volunteer = Volunteer.objects.get(id=volunteer_id)
    output = _vcard_string(volunteer, vcard_type)
    if (output != ""):
        filename = "%s-%s.vcf" % (volunteer.firstname, volunteer.name)
        response = HttpResponse(output, mimetype="text/x-vCard")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    else:
        response = HttpResponseNotFound('<h1>Type de téléphone invalide!</h1>')
    return response


@login_required(redirect_field_name='next')
def event_index(request):
    """Display a search form (and a list of volunteers)"""
    events = []
    try:
        query = request.GET["q"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query == "" or query == " ":
            events = Event.objects.all().order_by('-date')[:10]
            return render_to_response('openvolunteer/event_index.html',
                                      {'events': events, 'results': results, 'terms': ""},
                                      context_instance=RequestContext(request))
        else:
            search_terms=query.split(' ')
            # get all events
            results = Event.objects.all()
            for term in search_terms:
                # search events corresponding to search term
                results = results.filter(Q(title__icontains = term)|
                                         Q(date__icontains = term)|
                                         Q(place__icontains = term)).all().order_by('date')
    # If there is no 'q' value, return empty results
    except:
        events = Event.objects.all().order_by('-date')[:10]
        results = []
        query = ""
    return render_to_response('openvolunteer/event_index.html',
                              {'events': events, 'results': results, 'terms': query},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_details(request, event_id):
    """Display event details and link to modify them"""
    try:
        event = Event.objects.get(id=event_id)
        needs = Need.objects.filter(event=event).all()
        error_message = ''
    except:
        needs = []
        event = ""
        error_message = 'Aucun événement ne correspond à votre requête.'
    return render_to_response('openvolunteer/event_details.html',
                              {'event': event,
                               'needs': needs,
                               'error_message': error_message},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_volunteers(request, event_id):
    """Display volunteers for an event"""
    try:
        event = Event.objects.get(id=event_id)
        error_message = ''
    except:
        event = ""
        answers = ""
        error_message = 'Aucun événement ne correspond à votre requête.'
        return render_to_response('openvolunteer/event_answers.html',
                                  {'event': event,
                                   'answers': answers,
                                   'error_message': error_message},
                                  context_instance=RequestContext(request))
    try:
        answers = Answer.objects.filter(event=event,presence=True).all().order_by('job')
    except:
        event = ""
        answers = ""
        error_message = 'Aucune réponse positive pour le moment.'
    return render_to_response('openvolunteer/event_answers.html',
                              {'event': event,
                               'answers': answers,
                               'error_message': error_message},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_tocontact(request, event_id):
    """Display not contacted volunteers for an event"""
    try:
        event = Event.objects.get(id=event_id)
        error_message = ''
    except:
        event = ""
        not_contacted = ""
        error_message = 'Aucun événement ne correspond à votre requête.'
        return render_to_response('openvolunteer/event_noanswers.html',
                                  {'event': event,
                                   'volunteers': not_contacted,
                                   'error_message': error_message},
                                  context_instance=RequestContext(request))
    try:
        volunteers = []
        not_contacted = []

        answers = Answer.objects.filter(event=event).all()
        for answer in answers:
            volunteers.append(answer.volunteer)

        all_volunteers = Volunteer.objects.all()
        for volunteer in all_volunteers:
            if volunteer not in volunteers:
                not_contacted.append(volunteer)
    except:
        event = ""
        not_contacted = ""
        error_message = 'Tous les bénévoles de la liste ont répondu.'
    return render_to_response('openvolunteer/event_noanswers.html',
                              {'event': event,
                               'volunteers': not_contacted,
                               'error_message': error_message},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def answer_index(request):
    """Display answers search form or results"""
    try:
        query_volunteer = request.GET["v"]
        query_event = request.GET["e"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query_event == "" or query_event == " ":
            events = Event.objects.all()
            return render_to_response('openvolunteer/answer_index.html',
                                      {'results': [],'events': events, 'terms': ""},
                                      context_instance=RequestContext(request))
        event = Event.objects.get(id=query_event)
        answers = Answer.objects.filter(event=event).all()

        # if volunteer fied is not empty, filter the result to get
        #   only correspondant volunteers.
        if query_volunteer != "" and query_volunteer != " ":
            # to do... so do nothing for the moment
            query_volunteer = ""

    # If there is no 'v' or 'e' value, return empty results
    except:
        event = ""
        answers = []
        query_volunteer = ""
    events = Event.objects.all()
    return render_to_response('openvolunteer/answer_index.html',
                              {'results': answers,'events': events, 'event': event, 'terms': query_volunteer},
                              context_instance=RequestContext(request))

from random import randrange
def myRandomizer(QuerySet):
    random_list = len(QuerySet)
    for i in range(random_list):
        item1, item2 = randrange(random_list), randrange(random_list)
        QuerySet[item1], QuerySet[item2] = QuerySet[item2], QuerySet[item1]
    return QuerySet


@login_required(redirect_field_name='next')
def job_index(request, selected_job=""):
    """Display index for job informations"""
    jobs = Job.objects.exclude(title="none").all()
    try:
        job = Job.objects.get(stripped_title=selected_job)
        error_message = ""
    except:
        job = ""
        error_message = "Aucun poste ne correspond a cette requete"
    return render_to_response('openvolunteer/job_index.html',
                              {'jobs': jobs, 'selected_job': job},
                              context_instance=RequestContext(request))


#RESULTS_STORAGE = []
@login_required(redirect_field_name='next')
def list_volunteer_index(request):
    """Display a form to generate a filtered list of volunteers"""
    if request.method == 'GET':
        return render_to_response('openvolunteer/list_volunteer_form.html',{},context_instance=RequestContext(request))
    elif request.method == 'POST':
        volunteers = Volunteer.objects.all()
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
            search_terms=filter.split(' ')
            print search_terms
            for term in search_terms:
                print term
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term)).all()
        except:
            pass
        #global RESULTS_STORAGE
        #RESULTS_STORAGE = volunteers
        #print RESULTS_STORAGE
        return render_to_response('openvolunteer/list_volunteer_form.html',
                              {'volunteers': volunteers},
                              context_instance=RequestContext(request))
