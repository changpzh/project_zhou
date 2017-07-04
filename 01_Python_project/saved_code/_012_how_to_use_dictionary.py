#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
this teach u how to use dict,
'''

people = {
    'Alice': {
        'phone': '2341',
        'addr': 'Foo drive 24'
    },
    'Beth': {
        'phone': '2351',
        'addr': 'Foo drive 25'
    },
    'Jason': {
        'phone': '2361',
        'addr': 'Foo drive 26'
    }
}

#phone number and address lable,
labels = {
    'phone': 'phone number',
    'addr': 'address'
}

name = raw_input('Name: ')

request = raw_input('phone number (p) or address (a)?')

key = request #if request not p or a.
if request == 'p': key = 'phone'
if request == 'a': key = 'addr'

# if name in people: print "%s's %s is %s." % \
#     (name, labels[key], people[name][key])

person = people.get(name, {})
label = labels.get(key, key)
result = person.get(key, 'not available')

print("%s's %s is %s." % (name, label, result))
