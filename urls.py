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
from django.conf.urls.defaults import *
from django.contrib.comments import urls

urlpatterns = patterns('demo.openvolunteer.views',
    # MAIN view
    (r'^$', 'index'),

    # VOLUNTEERS views, search tool and vcard generation
    (r'^volunteer/$','volunteer_index'),
    (r'^volunteer/add/$','volunteer_add'),
    (r'^volunteer/(?P<volunteer_id>\d+)/$', 'volunteer_details'),
    (r'^volunteer/vcard/(?P<volunteer_id>\d+)/$', 'volunteer_vcard'),
    (r'^volunteer/delete/(?P<volunteer_id>\d+)/$', 'volunteer_delete'),
    (r'^volunteer/edit/(?P<volunteer_id>\d+)/$', 'volunteer_edit'),

    # LISTS generators
    (r'^volunteer/list/$','list_volunteer_index'),

    # EVENTS views and search tool
    (r'^event/$', 'event_index'),
    (r'^event/add/$', 'event_add'),
    (r'^event/(?P<event_id>\d+)/$', 'event_details'),
    (r'^event/edit/(?P<event_id>\d+)/$', 'event_edit'),
    (r'^event/delete/(?P<event_id>\d+)/$', 'event_delete'),

    # ANSWERS views and search tool
    (r'^answers/event/(?P<event_id>\d+)/$', 'event_volunteers'),
    (r'^answers/event/csv/(?P<event_id>\d+)/$', 'event_csv'),
    (r'^answers/nocontact/event/(?P<event_id>\d+)/$', 'event_tocontact'),
    (r'^answer/$','answer_index'),

    # JOBS views and index
    (r'^job/$','job_index'),
    (r'^job/add/$','job_add'),
    (r'^job/edit/(?P<job_id>\d+)/$','job_edit'),
    (r'^job/delete/(?P<job_id>\d+)/$','job_delete'),
)

urlpatterns += patterns('',
    # Provide access to css files
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': APPLICATION_PATH + '/static-files'}),
)
