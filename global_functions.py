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


def get_sorting_parameters(request, default_sort='', allowed_sorting=[]):
    """
    Get sorting parameters from a request.
        request: the web request sent to the view function
        default_sort: the default sorting for view
        allowed_sorting: the sorting parameters allowed to
                         avoid backend errors
    """
    try:
        query_sort = request.REQUEST["sort"]
        if query_sort not in allowed_sorting:
            query_sort = default_sort
    except:
        query_sort = default_sort
    try:
        query_order = request.REQUEST["order"]
    except:
        query_order = 'asc'
    if query_order == 'desc':
        query_sort = '-%s' % query_sort
    return query_sort

