# -*- coding: utf-8 -*-

from django.db import models


class AThing(models.Model):

    KIND_CHOICES_d = {
        'flavour' : 'tipo',
        'geo' : 'territorio',
        'topic' : 'tematica',
        'target' : 'target',
        'web' : 'servizi web',
        
    }
    KIND_CHOICES = KIND_CHOICES_d.items()

    KIND_VALUE_CHOICES_d = {
        'flavour' : {
            'association' : 'associazione',
            'group' : 'gruppo informale',
            'mailing-list' : 'lista',
            'company' : 'azienda',
        },
        'topic' : {
            'ALTRO' : 'ALTRO',
            'BIRRA E PIZZATE' : 'BIRRA E PIZZATE',
            'PRINCIPII DEL SL' :'PRINCIPII DEL SL',
            'SCUOLE' : 'SCUOLE',
            'TRASHWARE' :'TRASHWARE',
            'CORSI' : 'CORSI',
            'CONTENUTI LIBERI' : 'CONTENUTI LIBERI',
            'PROGRAMMAZIONE' : 'PROGRAMMAZIONE',
        },
        'web' : {
            'ALTRO' : 'ALTRO',
            'GOOGLE' : 'GOOGLE',
            'FRIENDICA' : 'FRIENDICA',
            'DIASPORA' : 'DIASPORA',
            'FACEBOOK' : 'FACEBOOK',
            'TWITTER' : 'TWITTER',
            'IDENTI.CA' : 'IDENTI.CA',
            'IRC/JABBER' : 'IRC/JABBER',
            'FORUM' : 'FORUM',
            'NEWSLETTER' : 'NEWSLETTER',
            'MAILING LIST' : 'MAILING LIST',
        }
    }

    kind = models.CharField(max_length=64, choices=KIND_CHOICES)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return "^s::%s" % (kind, value)


class AGroup(models.Model):
    
    name = models.CharField(max_length=256)
    email = models.EmailField()
    website = models.URLField()
    city = models.CharField(max_length=256, blank=True)
    year = models.DateField(null=True, blank=True)
    n_people = models.PositiveIntegerField(blank=True, default=1)
    n_hacktivist = models.PositiveIntegerField(blank=True, default=1)

    thing_set = models.ManyToManyField(AThing, through="WeightedThing")

    def __unicode__(self):
        return self.name

class WeightedThing(models.Model):

    agroup = models.ForeignKey(AGroup)
    athing = models.ForeignKey(AThing)
    weight = models.PositiveSmallIntegerField(default=1)
    
