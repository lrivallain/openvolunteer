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
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from forms import *

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
    """
    Display volunteer details and link to modify them
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    return render_to_response('openvolunteer/volunteer_details.html',
                              {'volunteer': volunteer},
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
    if (output != ""):
        # slugify filename to avoid some unicode issues
        filename = "%s-%s" % (volunteer.firstname, volunteer.name)
        filename = "%s.vcf" % defaultfilters.slugify(filename)

        response = HttpResponse(output, mimetype="text/x-vCard")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    else:
        response = HttpResponseNotFound('<h1>La génération de la Vcard a échoué!</h1>')
    return response


@login_required(redirect_field_name='next')
def volunteer_delete(request, volunteer_id):
    """
    Delete current volunteer
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteer.delete()
    return redirect("/openvolunteer/volunteer/")


@login_required(redirect_field_name='next')
def volunteer_edit(request, volunteer_id):
    """
    Add or Update volunteer infos
    """
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    form = VolunteerForm(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                volunteer = volunteer_add_or_edit(request, form, volunteer)
                message = "Modification effectuée !<br><a href='%s'" % volunteer.get_absolute_url()
                message += "' title='Revenir à la fiche'>Retour</a>"
                status = "success"
            else:
                message = "La modification a échoué ! (error code: 101)"
                status = "error"
        except:
            message = "La modification a échoué ! (error code: 102)"
            status = "error"
    else:
        return render_to_response('openvolunteer/volunteer_edit.html',
                              {'volunteer': volunteer, 'form': form},
                              context_instance=RequestContext(request))
    return render_to_response('openvolunteer/operation_result.html',
                              {'status': status,
                               'message': message},
                              context_instance=RequestContext(request))

@login_required(redirect_field_name='next')
def volunteer_add(request):
    """
    Add volunteer infos
    """
    volunteer = Volunteer()
    form = VolunteerForm(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                volunteer = volunteer_add_or_edit(request, form, volunteer)
                message = "Ajout effectué !<br><a href='%s'" % volunteer.get_absolute_url()
                message += "' title='Voir la fiche'>Voir la fiche de ce nouveau bénévole</a>"
                status = "success"
            else:
                message = "L'ajout a échoué ! (error code: 103)"
                status = "error"
        except:
            message = "L'ajout a échoué ! (error code: 104)"
            status = "error"
    else:
        return render_to_response('openvolunteer/volunteer_edit.html',
                              {'form': form},
                              context_instance=RequestContext(request))
    return render_to_response('openvolunteer/operation_result.html',
                              {'status': status,
                               'message': message},
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
    volunteer.save()
    return volunteer
