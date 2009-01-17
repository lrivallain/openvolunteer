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
import vobject

def _vcard_string(person, vcard_type):
    """
    Helper function for vcard views. Accepts a 'person' object 
    with certain attributes (firstname, lastname, email, phone, id)
    and returns a string containing serialized vCard data.
    """
    # vobject API is a bit verbose...
    vcard = vobject.vCard()
    
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=person.name, given=person.firstname)
    
    vcard.add('fn')
    vcard.fn.value = "%s %s" % (person.firstname, person.name)
    
    vcard.add('email')
    vcard.email.type_param = 'INTERNET'
    vcard.email.value = person.email
    
    if (vcard_type == "home"):
        vcard.add('tel')
        vcard.tel.type_param = 'HOME'
        vcard.tel.value = person.phone_home
    elif (vcard_type == "mobile"):
        vcard.add('tel')
        vcard.tel.type_param = 'CELL'
        vcard.tel.value = person.phone_mobile
    else:
        return ""
    
    vcard.add('address')
    vcard.address.value = person.address
    
    output = vcard.serialize()
    return output
