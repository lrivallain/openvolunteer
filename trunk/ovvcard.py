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

def _vcard_string(person):
    vcard  = u"BEGIN:VCARD\n"
    vcard += u"VERSION:3.0\n"
    vcard += u"FN:%s %s\n"                      % (person.name, person.firstname)
    vcard += u"N:%s;%s;;;\n"                    % (person.firstname, person.name)
    if person.email:
        vcard += u"EMAIL;TYPE=INTERNET:%s\n"    % person.email
    if person.phone_home:
        vcard += u"TEL;TYPE=HOME:%s\n"          % person.phone_home
    if person.phone_mobile:
        vcard += u"TEL;TYPE=CELL:%s\n"          % person.phone_mobile
    vcard += u"END:VCARD"

    return vcard
