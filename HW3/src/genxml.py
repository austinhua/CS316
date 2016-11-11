#!/usr/bin/env python

import sys
import codecs
import datetime
import yaml
from xml.dom.minidom import getDOMImplementation

# Try to use the faster C-based yaml parser:
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

doc = getDOMImplementation().createDocument(None, 'congress', None)
committee_nodes = dict()
subcommittee_nodes = dict()

def gen_person(person):
    p = doc.createElement('person')
    p.setAttribute('id', person['id']['bioguide'])
    p.setAttribute('name', person['name']['official_full'])
    p.setAttribute('birthday', person['bio']['birthday'])
    p.setAttribute('gender', person['bio']['gender'])
    for role in person['terms']:
        r = doc.createElement('role')
        r.setAttribute('type', role['type'])
        r.setAttribute('startdate', role['start'])
        r.setAttribute('enddate', role['end'])
        if datetime.datetime.strptime(role['end'], '%Y-%m-%d') >= datetime.datetime.now():
            r.setAttribute('current', '1')
        r.setAttribute('party', role['party'])
        r.setAttribute('state', role['state'])
        if 'district' in role:
            r.setAttribute('district', str(role['district']))
        p.appendChild(r)
    return p

def gen_committee(committee):
    c = doc.createElement('committee')
    c.setAttribute('type', committee['type'])
    c.setAttribute('code', committee['thomas_id'])
    c.setAttribute('displayname', committee['name'])
    if 'subcommittees' in committee:
        for subcommittee in committee['subcommittees']:
            s = doc.createElement('subcommittee')
            s.setAttribute('code', subcommittee['thomas_id'])
            s.setAttribute('displayname', subcommittee['name'])
            c.appendChild(s)
    return c

def add_memberships(code, members):
    c = committee_nodes[code] if code in committee_nodes else \
        subcommittee_nodes[code]
    # this firstChild business is to ensure that committee members
    # appear subcommittees:
    f = c.firstChild
    for member in members:
        m = doc.createElement('member')
        m.setAttribute('id', member['bioguide'])
        if 'title' in member:
            m.setAttribute('role', member['title'])
        if f:
            c.insertBefore(m, f)
        else:
            c.appendChild(m)
    return

congress = doc.documentElement

sys.stderr.write('***** processing current legislators *****\n')
persons = yaml.load(file('legislators-current.yaml', 'r'),
                    Loader=Loader)
ps = doc.createElement('people')
congress.appendChild(ps)
for person in persons:
    ps.appendChild(gen_person(person))

sys.stderr.write('***** processing current committees *****\n')
committees = yaml.load(file('committees-current.yaml', 'r'),
                       Loader=Loader)
cs = doc.createElement('committees')
congress.appendChild(cs)
for committee in committees:
    c = gen_committee(committee)
    cs.appendChild(c)
    committee_nodes[c.getAttribute('code')] = c
    for s in c.childNodes:
        subcommittee_nodes[c.getAttribute('code') + s.getAttribute('code')] = s

sys.stderr.write('***** processing current memberships *****\n')
committee_memberships = yaml.load(file('committee-membership-current.yaml', 'r'),
                                  Loader=Loader)
for code, members in committee_memberships.iteritems():
    add_memberships(code, members)

print doc.toprettyxml(indent=' '*4, encoding='utf-8')
