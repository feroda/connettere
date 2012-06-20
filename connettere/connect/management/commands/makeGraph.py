
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
        """ rankdir: orientation of the graph
            graph_type: directed, non-directed
            nodesep: minimum vertical distance between adjacent ranks of nodes
            ranksep: minimum horizontal distance between adjacent nodes of equal rank
    """
        mygraph = pydot.Dot(rankdir='LR',graph_type='digraph',nodesep='1',ranksep='20')
                
        thing_nodes = []
        i = 0
        s = '"'
        hop = 15000
        color = 100000

        for thing in AThing.objects.all():
            t_node = pydot.Node(thing.__unicode__().replace("::"," ").replace("\"",""), style="filled", fillcolor="green")
            thing_nodes.insert(i,t_node)
            mygraph.add_node(t_node)
            #print "add thing node: %s" % (t_node.get_name())
            i = i + 1

        #print "\n"

        for group in AGroup.objects.all():
            #print "\n"
            color += hop
            even = 0
             
            group_node = pydot.Node(group.__unicode__().replace("\"",""), style="filled", fillcolor="red")
            print group.__unicode__().replace("\"","")
            mygraph.add_node(group_node)
            print "add group node: %s" % (group_node.get_name())
            for thing in group.thing_set.all():
                for thing_node in thing_nodes:
                    #print "GROUP: %s; %s" % (group.__unicode__(), s + thing.__unicode__().replace("::"," ") + s)
                    #print thing_node.get_name()
                    if (s + thing.__unicode__().replace("::"," ") + s) == thing_node.get_name():
                        #print '#' + str(color)
                        edge = pydot.Edge(group_node, thing_node,color='#' + str(color))
                        mygraph.add_edge(edge)
                        #print "add edge from: %s to: %s" % (group_node.get_name(),thing_node.get_name())
                        break

        mygraph.write_png(filename)

        return

    def handle(self, *args, **options):
        
        try:
            filename = args[0]
        except IndexError:
            raise CommandError("Usage: %s <filename>" % (self.args))
        
        self.makeGraph(filename)  
