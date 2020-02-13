#!/usr/bin/env python
import dateparser
from training.models import Training

headers = (
    'received',
    'email',
    'title',
    'description',
    'start',
    'end',
    'location',
    'use_gtn',
    'attendance',
    'advertise_eu',
    'blogpost',
    'website',
    'gtn_links',
    'training_identifier',
    'name',
    'non_gtn_links',
    'other_requests',
    'processed',
    'days_until',
    'gdpr',
    'days_since'
)

x = open('data.tsv', 'r').read().strip().split('\n')
for idx, line in enumerate(x):
    if idx == 0:
        continue

    line = line.split('\t')
    d = dict(zip(headers, line))
    del  d['days_until']
    del  d['gdpr']
    del  d['days_since']
    del  d['blogpost']

    d['received'] = dateparser.parse(d['received']).date()
    d['start'] = dateparser.parse(d['start']).date()
    d['end'] = dateparser.parse(d['end']).date()

    if d['processed'] == 'yes':
        d['processed'] = 'AP'
    else:
        d['processed'] = 'UN'

    if d['advertise_eu'] == 'yes':
        d['advertise_eu'] = 'Y'
    else:
        d['advertise_eu'] = 'N'

    d['location'] = [
        x.strip().split(' ')[0]
        for x in
        d['location'].split(',')
    ]

    __import__('pprint').pprint(d)
    t = Training(**d)
    t.save()
