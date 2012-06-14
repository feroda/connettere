# Author: Luca Ferroni <luca@befair.it>
# License: GNU Affero General Public License

from django.core.management.base import BaseCommand, CommandError
from connect.models import AThing,AGroup,WeightedThing
from datetime import datetime

import csv, os, time

ENCODING = "iso-8859-1"

class Command(BaseCommand):
    """ This command loads data from a CSV file where terms are divided by commas
"""

    args = '<filename>'

    help = """ Load data from a CSV file""" 

    filename = "/tmp/csv_" + str(time.time())
    delimiter = ','
    encoding = 'utf-8'

    def read(self, csvdata,fieldnames):
        #Write CSV file with data
        s = csv.Sniffer()
        if s.has_header(csvdata):
            csvdata = csvdata[csvdata.find("\n")+1:]
        csvfile = file(self.filename, "w")
        csvfile.write(csvdata)
        csvfile.close()

        #Read data into dictionary
        csvfile = file(self.filename, "r")
        csvr = csv.DictReader(csvfile,fieldnames=fieldnames,delimiter=self.delimiter)
        rows = []
        for item in csvr:
            rows.append(item)
        csvfile.close()
        os.remove(self.filename)

        return rows

    def handle(self, *args, **options):
        
        try:
            filename = args[0]
        except IndexError:
            raise CommandError("Usage: %s <filename>" % (self.args))

        fieldnames = ["id","Completato","Last page seen","Start language", \
            "Nome del gruppo","Recapito e-mail","Sito web","Citta","Territorio\
            di influenza","Anno di fondazione","Numero soci o componenti",\
            "Numero persone attive","[Mailing list] web","[Newsletter] web",\
            "[Forum] web","[IRC / Jabber] web","[identi.ca] web","[Twitter] web"\
            ,"[Facebook] web","[Diaspora] web","[Friendica] web","[Google] web"\
            ,"[Altro] web","[Programmazione] topic","[Contenuti Liberi] topic"\
            ,"[Corsi] topic","[Trashware] topic","[Scuole] topic",\
            "[Principi del Software Libero] topic","[Birra e pizzate] topic",\
            "[Altro] topic"]
        
        f = file(filename, "r")
        csvdata = f.read()
        f.close()
        values = self.read(csvdata,fieldnames)
        
        for row in values:
            if row["Nome del gruppo"] != '' and row["Recapito e-mail"] != '' and row["Sito web"] != '' and row["Citta"] != '' and row["Anno di fondazione"] != '' and row["Numero soci o componenti"] != '' and row["Numero persone attive"] != '':
                group,created = AGroup.objects.get_or_create(name=row["Nome del gruppo"],email=row["Recapito e-mail"],website=row["Sito web"],city=row["Citta"],year=datetime.strptime(''.join([row["Anno di fondazione"],"/01/01","-","00:00:00"]), "%Y/%m/%d-%H:%M:%S"),n_people=row["Numero soci o componenti"],n_hacktivist=row["Numero persone attive"])
                if created:
                    if row["[Mailing list] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web', value='mailing-list')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Newsletter] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='NEWSLETTER')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Forum] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='FORUM')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[IRC / Jabber] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='IRC/JABBER')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[identi.ca] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='IDENTI.CA')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Twitter] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='TWITTER')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Facebook] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='FACEBOOK')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Diaspora] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='DIASPORA')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Friendica] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='FRIENDICA')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Google] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='GOOGLE')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Altro] web"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='web',value='ALTRO')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Programmazione] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='PROGRAMMAZIONE')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Contenuti Liberi] topic" ].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='CONTENUTI LIBERI')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Corsi] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='CORSI')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Trashware] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='TRASHWARE')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Scuole] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='SCUOLE')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Principi del Software Libero] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='PRINCIPII DEL SL')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Birra e pizzate] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='BIRRA E PIZZATE')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
                    if row["[Altro] topic"].startswith('S'):
                        thing,created = AThing.objects.get_or_create(kind='topic',value='ALTRO')
                        WeightedThing.objects.create(agroup=group,athing=thing,weight=1)
