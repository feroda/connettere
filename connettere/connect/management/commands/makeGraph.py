
from django.core.management.base import BaseCommand, CommandError
from connect.models import AThing,AGroup

import pydot 

ENCODING = "iso-8859-1"

class Command(BaseCommand):
    """ This command outputs Graphs representing this application model 
"""

    args = '<filename>'

    help = """ Make Graphs """ 


    def makeGraph(self, filename):
        mygraph = pydot.Dot(graph_type='graph')
        
        thing_nodes = []
        i = 0
        s = '"'
        hop = 30000
        color = 100000

        for thing in AThing.objects.all():
            thing_nodes.insert(i,pydot.Node(thing.__unicode__().replace("::"," "), style="filled", fillcolor="green"))
            i = i + 1

        for group in AGroup.objects.all():
            color += hop
            group_node = pydot.Node(group.__unicode__(), style="filled", fillcolor="red")
            for thing in group.thing_set.all():
                for thing_node in thing_nodes:
                    #print s + thing.__unicode__().replace("::"," ") + s
                    #print thing_node.get_name()
                    if (s + thing.__unicode__().replace("::"," ") + s) == thing_node.get_name():
                        print '#' + str(color)
                        edge = pydot.Edge(group_node, thing_node,color='#' + str(color))
                        mygraph.add_edge(edge)
                        break

        mygraph.write_png(filename)

        return

    def handle(self, *args, **options):
        
        try:
            filename = args[0]
        except IndexError:
            raise CommandError("Usage: %s <filename>" % (self.args))
        
        self.makeGraph(filename)  
