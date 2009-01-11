#-*- coding: utf-8 -*-
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
