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
from ovsettings import *

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

import datetime
import csv
import os


@login_required(redirect_field_name='next')
def volunteer_index(request):
    """
    Display a search form (and a list of volunteers)
    """
    try:
        query = request.GET["q"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query == "" or query == " ":
            return render_to_response('openvolunteer/volunteer_index.html',
                                      {'results': [], 'terms': ""},
                                      context_instance=RequestContext(request))
        else:
            search_terms = query.split(' ')
            # get all volunteers
            volunteers = Volunteer.objects.order_by('name')
            for term in search_terms:
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term)|
                                               Q(email__icontains = term)|
                                               Q(phone_home__icontains = term)|
                                               Q(phone_mobile__icontains = term))
            # if only one result, goes to volunteer details page
            if (len(volunteers) == 1):
                return volunteer_details(request, volunteers[0].id)
            # in other cases, we generate csv file for export
            else:
                list_volunteer_csv(volunteers)
    # If there is no 'q' value, return empty results
    except:
        volunteers = []
        query = ""
    return render_to_response('openvolunteer/volunteer_index.html',
                              {'results': volunteers, 'terms': query},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def volunteer_details(request, volunteer_id):
    """
    Display volunteer details and link to modify them
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)

    jobs = []
    limit = datetime.date.today()
    limit = limit.replace(limit.year - OPENVOLUNTEER_JOB_DELAY)

    answers = Answer.objects.filter(volunteer=volunteer, presence="yes")
    for answer in answers:
        if answer.event.date > limit:
            if answer not in jobs:
                jobs.append(answer)
    return render_to_response('openvolunteer/volunteer_details.html',
                              {'volunteer': volunteer,
                               'jobs': jobs},
                              context_instance=RequestContext(request))


from django.template import defaultfilters
from  ovvcard import _vcard_string
@login_required(redirect_field_name='next')
def volunteer_vcard(request, volunteer_id):
    """
    View function for returning single vcard
    """
    volunteer = Volunteer.objects.get(id=volunteer_id)
    output = _vcard_string(volunteer)
    if (output == ""):
        message = "La génération a échoué ! (error code: %d)" % ERROR_VOLUNTEER_VCARD_GENERATION
        status = "error"
        return render_to_response('openvolunteer/operation_result.html',
                                  {'status': status, 'message': message},
                                  context_instance=RequestContext(request))

    # slugify filename to avoid some unicode issues
    filename = "%s-%s" % (volunteer.firstname, volunteer.name)
    filename = "%s.vcf" % defaultfilters.slugify(filename)

    response = HttpResponse(output.encode('iso-8859-1'), mimetype="text/x-vCard")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


@login_required(redirect_field_name='next')
def volunteer_delete(request, volunteer_id):
    """
    Delete current volunteer
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteer.delete()
    return redirect(OPENVOLUNTEER_WEB_ROOT + '/volunteer/')


@csrf_protect
@login_required(redirect_field_name='next')
def volunteer_edit(request, volunteer_id):
    """
    Add or Update volunteer infos
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    form = VolunteerForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            try:
                volunteer = volunteer_add_or_edit(request, form, volunteer)
            except:
                message = "La modification a échoué ! (error code: %d)" % ERROR_VOLUNTEER_EDIT_SAVING
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status, 'message': message},
                                          context_instance=RequestContext(request))
            return redirect(volunteer)
        else:
            message = "La modification a échoué ! (error code: %d)" % ERROR_VOLUNTEER_EDIT_INVALIDFORM
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status, 'message': message},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('openvolunteer/volunteer_edit.html',
                                  {'volunteer': volunteer, 'form': form},
                                  context_instance=RequestContext(request))


@csrf_protect
@login_required(redirect_field_name='next')
def volunteer_add(request):
    """
    Add volunteer infos
    """
    volunteer = Volunteer()
    form = VolunteerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                volunteer = volunteer_add_or_edit(request, form, volunteer)
            except:
                message = "L'ajout a échoué ! (error code: %d)" % ERROR_VOLUNTEER_ADD_SAVING
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status, 'message': message},
                                          context_instance=RequestContext(request))
            return redirect(volunteer)
        else:
            message = "L'ajout a échoué ! (error code: %d)" % ERROR_VOLUNTEER_ADD_INVALIDFORM
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status, 'message': message},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('openvolunteer/volunteer_edit.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


def volunteer_add_or_edit(request, form, volunteer):
    """
    Add or update volunteer infos
    """
    volunteer.name = form.cleaned_data['name']
    volunteer.firstname = form.cleaned_data['firstname']
    if (request.REQUEST['email'] != ''):
        volunteer.email = form.cleaned_data['email']
    else: volunteer.email = ''
    if (request.REQUEST['phone_home'] != ''):
        volunteer.phone_home = form.cleaned_data['phone_home']
    else: volunteer.phone_home = ''
    if (request.REQUEST['phone_mobile'] != ''):
        volunteer.phone_mobile = form.cleaned_data['phone_mobile']
    else: volunteer.phone_mobile = ''
    if (request.REQUEST['address'] != ''):
        volunteer.address = form.cleaned_data['address']
    else: volunteer.address = ''
    if (request.REQUEST['birth_place'] != ''):
        volunteer.birth_place = form.cleaned_data['birth_place']
    else: volunteer.birth_place = ''
    if ((request.REQUEST['birthday_year'] != '') and
        (request.REQUEST['birthday_month'] != '') and
        (request.REQUEST['birthday_day'] != '')):
        volunteer.birthday = datetime.date(int(request.REQUEST['birthday_year']),
                                           int(request.REQUEST['birthday_month']),
                                           int(request.REQUEST['birthday_day']))
    else: volunteer.birthday = None
    if (request.REQUEST['social_security_number'] != ''):
        volunteer.social_security_number = int(request.REQUEST['social_security_number'])
    try:
        if (request.REQUEST['ca_member']):
            volunteer.ca_member = True
        else: volunteer.ca_member = False
    except: volunteer.ca_member = False
    if (request.REQUEST['comments'] != ''):
        volunteer.comments = form.cleaned_data['comments']
    else: volunteer.comments = ''

    try:
        if (request.REQUEST['delete_avatar']):
            volunteer.avatar.delete(save=False)
    except: pass

    try:
        if request.FILES['avatar']:
            volunteer = handle_volunteer_avatar(volunteer, request.FILES['avatar'])
    except: pass

    volunteer.save()
    return volunteer


@csrf_protect
@login_required(redirect_field_name='next')
def list_volunteer_index(request):
    """
    Display a form to generate a filtered list of volunteers
    """
    if request.method == 'GET':
        return render_to_response('openvolunteer/list_volunteer_form.html',
                                  {},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        volunteers = Volunteer.objects.all()
        if request.REQUEST["filter_q"]:
            filter = request.REQUEST["filter_q"]
            volunteers = volunteers.filter(Q(name__icontains = filter)|
                                           Q(firstname__icontains = filter))
        try:
            filter = request.REQUEST["filter_address"]
            volunteers = volunteers.exclude(address="")
        except: pass
        try:
            filter = request.REQUEST["filter_phone"]
            volunteers = volunteers.exclude(phone_home="")
        except: pass
        try:
            filter = request.REQUEST["filter_mobile"]
            volunteers = volunteers.exclude(phone_mobile="")
        except: pass
        try:
            filter = request.REQUEST["filter_email"]
            volunteers = volunteers.exclude(email="")
        except: pass
        try:
            filter = request.REQUEST["filter_ca"]
            volunteers = volunteers.exclude(ca_member="")
        except: pass
        try:
            filter = request.REQUEST["filter_old"]
            print filter
            if (filter == 'on'):
                limit = datetime.date.today()
                limit = limit.replace(limit.year-18)
                volunteers = volunteers.exclude(birthday__gt=limit)
        except: pass
        try:
            filter = request.REQUEST["filter_name"]
            search_terms=filter.split(' ')
            print search_terms
            for term in search_terms:
                print term
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term))
        except: pass
        if volunteers:
            list_volunteer_csv(volunteers)
        return render_to_response('openvolunteer/list_volunteer_form.html',
                              {'volunteers': volunteers},
                              context_instance=RequestContext(request))


def list_volunteer_csv(volunteers):
    """
    Export volunteers into CSV file
    """

    path =  settings.MEDIA_ROOT + OPENVOLUNTEER_APP_NAME + "/csv"
    filename = path + "/volunteer_list.csv"

    if not os.path.exists(path):
        os.mkdir(path)

    if os.path.isfile(filename):
        os.remove(filename)

    writer = csv.writer(open(filename, 'w'))
    writer.writerow(['Nom', 'Prénom', 'Email', 'Numéro de téléphone',
                     'Numéro de mobile', 'Date de Naissance', 'Inscription',
                     'Membre du CA'])

    for volunteer in volunteers:
        if volunteer.birthday:
           birthday = "%d/%d/%d" % (volunteer.birthday.day,
                                    volunteer.birthday.month,
                                    volunteer.birthday.year)
        else:
           birthday = ""

        if volunteer.inscription_date:
           inscription = "%d/%d/%d" % (volunteer.inscription_date.day,
                                       volunteer.inscription_date.month,
                                       volunteer.inscription_date.year)
        else:
           inscription = ""

        if volunteer.ca_member:
            ca = "oui"
        else:
            ca = "non"
        writer.writerow([unicode(s).encode('utf-8') for s in (
                             volunteer.name,
                             volunteer.firstname,
                             volunteer.email,
                             volunteer.phone_home,
                             volunteer.phone_mobile,
                             birthday,
                             inscription,
                             ca)
                        ])
    return filename


def handle_volunteer_avatar(volunteer, file):
    """
    Save uploaded file for volunteer avatar
    """
    filename = file.name
    volunteer.avatar.save(filename, file, save=True)
    return volunteer


@login_required(redirect_field_name='next')
def volunteer_byjob(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    volunteers = []
    limit = datetime.date.today()
    limit = limit.replace(limit.year - OPENVOLUNTEER_JOB_DELAY)

    answers = Answer.objects.filter(job=job, presence="yes")
    for answer in answers:
        if answer.event.date > limit:
            if answer.volunteer not in volunteers:
                volunteers.append(answer.volunteer)

    if volunteers:
        list_volunteer_csv(volunteers)
    return render_to_response('openvolunteer/volunteer_byjob.html',
                              {'volunteers': volunteers, 'job': job, 'limit': limit},
                              context_instance=RequestContext(request))
