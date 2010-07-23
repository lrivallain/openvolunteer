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
from models import *
from forms import *
from errors import *

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

import datetime


@login_required(redirect_field_name='next')
def answer_index(request):
    """
    Display answers search form or results
    """
    allowed_sorting = ['volunteer__name','volunteer__firstname',
                       'volunteer__email','volunteer__phone_home',
                       'volunteer__phone_mobile','volunteer__address',
                       'volunteer__birth_place','volunteer__birthday',
                       'volunteer__social_security_number','volunteer__ca_member',
                       'job','presence']
    events = Event.objects.all()
    try:
        query_event = request.GET["q"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query_event == "" or query_event == " ":
            return render_to_response('openvolunteer/answer_index.html',
                                      {'results': [],'events': events, 'terms': ""},
                                      context_instance=RequestContext(request))
        sort = get_sorting_parameters(request, 'volunteer__name', allowed_sorting)
        event = Event.objects.get(id=query_event)
        answers = Answer.objects.filter(event=event).all().order_by(sort)

    # If there is no 'v' or 'e' value, return empty results
    except:
        event = ""
        answers = []
    return render_to_response('openvolunteer/answer_index.html',
                              {'results': answers,'events': events,
                               'event': event},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def answer_tocontact(request, event_id):
    """
    Display not contacted volunteers for an event
    """
    allowed_sorting = ['name','firstname',
                       'email','phone_home',
                       'phone_mobile','address',
                       'birth_place','birthday',
                       'social_security_number','ca_member']
    event = get_object_or_404(Event, id=event_id)
    try:
        volunteers = []
        not_contacted = []

        answers = Answer.objects.filter(event=event).all()
        for answer in answers:
            volunteers.append(answer.volunteer)

        sort = get_sorting_parameters(request, 'name', allowed_sorting)
        all_volunteers = Volunteer.objects.all().order_by(sort)
        for volunteer in all_volunteers:
            if volunteer not in volunteers:
                not_contacted.append(volunteer)
    except:
        event = ""
        not_contacted = ""
    return render_to_response('openvolunteer/answer_unknown.html',
                              {'event': event,
                               'volunteers': not_contacted},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def answer_positives(request, event_id):
    """
    Display volunteers for an event with positive answer
    """
    allowed_sorting = ['volunteer__name','volunteer__firstname',
                       'volunteer__email','volunteer__phone_home',
                       'volunteer__phone_mobile','volunteer__address',
                       'volunteer__birth_place','volunteer__birthday',
                       'volunteer__social_security_number','volunteer__ca_member',
                       'job','presence']
    event = get_object_or_404(Event, id=event_id)

    try:
        sort = get_sorting_parameters(request, 'volunteer__name', allowed_sorting)
        answers = Answer.objects.filter(event=event,presence="yes").all().order_by(sort)
    except:
        event = ""
        answers = ""
    return render_to_response('openvolunteer/answer_positives.html',
                              {'event': event,
                               'answers': answers},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_answer_delete(request, answer_id):
    """
    Delete an answer
    """
    answer = get_object_or_404(Answer, id=answer_id)
    url = answer.event.get_answer_url()
    answer.delete()
    return redirect(url)


@csrf_protect
@login_required(redirect_field_name='next')
def event_answer_add(request, event_id, volunteer_id=None):
    """
    Add an answer for current event
    """
    answer = Answer()
    answer.event = get_object_or_404(Event, id=event_id)
    form = AnswerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                answer = answer_add_or_edit(request, form, answer)
            except:
                message = "L'ajout a échoué ! (error code: %d)" % ERROR_ANSWER_ADD_SAVING
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status,
                                           'message': message},
                                          context_instance=RequestContext(request))
            return redirect(answer.event.get_answer_url())
        else:
            message = "L'ajout a échoué ! (error code: %d)" % ERROR_ANSWER_ADD_INVALIDFORM
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        jobs = Job.objects.all()
        sel_opts_job = ''
        for job in jobs:
            sel_opts_job += "<option value='%d'>%s</option>\n" % (job.id, job.title)

        volunteers = Volunteer.objects.all()
        sel_opts_vol = ''
        for vol in volunteers:
            sel_opts_vol += "<option value='%d'" % vol.id
            try:
                if (int(volunteer_id) == vol.id):
                    sel_opts_vol += "selected='selected'"
            except:
                pass
            sel_opts_vol += ">%s %s</option>\n" % (vol.name, vol.firstname)

        return render_to_response('openvolunteer/answer_edit.html',
                                  {'answer': answer, 'sel_opts_vol': sel_opts_vol,
                                   'sel_opts_job': sel_opts_job, 'form': form},
                                  context_instance=RequestContext(request))


@csrf_protect
@login_required(redirect_field_name='next')
def event_answer_edit(request, answer_id):
    """
    Update answer informations
    """
    answer = get_object_or_404(Answer, id=answer_id)
    form = AnswerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                answer = answer_add_or_edit(request, form, answer)
            except:
                message = "La modification a échoué ! (error code: %d)" % ERROR_ANSWER_EDIT_SAVING
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status,
                                           'message': message},
                                          context_instance=RequestContext(request))
            return redirect(answer.event.get_answer_url())
        else:
            message = "La modification a échoué ! (error code: %d)" % ERROR_ANSWER_EDIT_INVALIDFORM
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        jobs = Job.objects.all()
        sel_opts_job = ''
        for job in jobs:
            sel_opts_job += "<option value='%d'" % job.id
            if (answer.job == job):
                sel_opts_job += "selected='selected'"
            sel_opts_job += ">%s</option>\n" % (job.title)

        volunteers = Volunteer.objects.all()
        sel_opts_vol = ''
        for vol in volunteers:
            sel_opts_vol += "<option value='%d'" % vol.id
            if (answer.volunteer == vol):
                sel_opts_vol += "selected='selected'"
            sel_opts_vol += ">%s %s</option>\n" % (vol.name, vol.firstname)

        return render_to_response('openvolunteer/answer_edit.html',
                                  {'answer': answer, 'sel_opts_vol': sel_opts_vol,
                                   'sel_opts_job': sel_opts_job, 'form': form},
                                  context_instance=RequestContext(request))


def answer_add_or_edit(request, form, answer):
    """
    Add or update answer infos
    """
    answer.volunteer = Volunteer.objects.get(id=request.REQUEST['volunteer'])
    if (request.REQUEST['job'] != ''):
        answer.job = Job.objects.get(id=request.REQUEST['job'])
    if (request.REQUEST['presence']):
        answer.presence = form.cleaned_data['presence']
    if ((request.REQUEST['lastrequest_year'] != '') and
        (request.REQUEST['lastrequest_month'] != '') and
        (request.REQUEST['lastrequest_day'] != '')):
        answer.last_request = datetime.date(int(request.REQUEST['lastrequest_year']),
                                            int(request.REQUEST['lastrequest_month']),
                                            int(request.REQUEST['lastrequest_day']))
    else: answer.last_request = None
    try:
        if (request.REQUEST['updating_vol_info']):
            answer.updating_vol_info = True
        else: volunteer.updating_vol_info = False
    except: answer.updating_vol_info = False
    try:
        if (request.REQUEST['updated_vol_info']):
            answer.updated_vol_info = True
        else: answer.updated_vol_info = False
    except: answer.updated_vol_info = False
    if (request.REQUEST['comments'] != ''):
        answer.comments = form.cleaned_data['comments']
    else: answer.comments = ''
    answer.save()
    return answer


def get_sorting_parameters(request, default_sort, allowed_sorting):
    try:
        query_sort = request.GET["sort"]
        if query_sort not in allowed_sorting:
            query_sort = default_sort
    except:
        query_sort = default_sort
    try:
        query_order = request.GET["order"]
    except:
        query_order = 'asc'
    if query_order == 'desc':
        query_sort = '-%s' % query_sort
    return query_sort
