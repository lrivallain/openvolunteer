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
    (r'^volunteer/(?P<volunteer_id>\d+)/$', 'volunteer_details'),
    (r'^volunteer/vcard/(?P<vcard_type>\D{3,})/(?P<volunteer_id>\d+)/$', 'volunteer_vcard'),
    # LISTS generators
    (r'^volunteer/list/$','list_volunteer_index'),
    (r'^volunteer/csv/$','csv_generator'),
    
    # EVENTS views and search tool
    (r'^event/$', 'event_index'),
    (r'^event/(?P<event_id>\d+)$', 'event_details'),
    
    # ANSWERS views and search tool
    (r'^answers/event/(?P<event_id>\d+)/$', 'event_volunteers'),
    (r'^answers/nocontact/event/(?P<event_id>\d+)/$', 'event_tocontact'),
    (r'^answer/$','answer_index'),
    
    # JOBS views and index
    (r'^job/$','job_index'),
    (r'^job/(?P<selected_job>\D{3,})/$','job_index'),
    
    # LISTS generators
    (r'^list/$','list_volunteer_index'),
    #(r'^list/csv/$','csv_generator'),
)

urlpatterns += patterns('',
    # Provide MEDIA data to application
    #  -- deprecated with MEDIA_ROOT use --
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': APPLICATION_PATH + '/media'}), #APPLICATION_PATH + '/media'}),
    
    # Provide access to css files
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': APPLICATION_PATH + '/static-files'}),
)
