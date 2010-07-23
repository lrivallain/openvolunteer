from models import *
from ovsettings import *

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q


@login_required(redirect_field_name='next')
def api_volunteer_get(request):
    """
    Retrieve volunteers in json
    """
    response = HttpResponse()
    try:
        query = request.GET["q"]
        limit = request.GET["limit"]
        if query == "" or query == " ":
            volunteers = []
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
        if volunteers and limit:
            volunteers = volunteers[:int(limit)]
    except:
        volunteers = []
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(volunteers, ensure_ascii=False, stream=response)
    return response


#                                                  NOT USED AT NOW !!!

@login_required(redirect_field_name='next')
def api_event_get(request):
    """
    Retrieve events in json
    """
    response = HttpResponse()
    try:
        query = request.GET["q"]
        limit = request.GET["limit"]
        if query == "" or query == " ":
            events = []
        else:
            search_terms=query.split(' ')
            # get all events
            events = Event.objects.order_by('date')
            for term in search_terms:
                # search events corresponding to search term
                try:
                    # try to filter with date:
                    events = events.filter(Q(title__icontains = term)|
                                           Q(date__year = int(term)) |
                                           Q(date__month = int(term))|
                                           Q(date__day = int(term))  |
                                           Q(place__icontains = term))
                except:
                    # if error when using date filter:
                    events = events.filter(Q(title__icontains = term)|
                                             Q(place__icontains = term))
    # If there is no 'q' value, return empty results
    except:
        events = []
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(events, ensure_ascii=False, stream=response)
    return response
