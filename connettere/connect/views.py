# Create your views here.i
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from connect.models import AGroup,AThing
from django.http import HttpResponse,HttpResponseRedirect

import pydot
import random 


def home(request):
    
    all_group_list = AGroup.objects.all().order_by('-name')
   
    return render_to_response('home.html', {'all_group_list': all_group_list},context_instance=RequestContext(request))


def graph(request):
    
    try:
        selected_group = AGroup.objects.get(name=request.POST['group'])
    except (KeyError, AGroup.DoesNotExist):
        # Redisplay
        all_group_list = AGroup.objects.all().order_by('-name')
        return render_to_response('home.html', {'all_group_list' : all_group_list,'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
           
        """ rankdir: orientation of the graph
            graph_type: directed, non-directed
            nodesep: minimum vertical distance between adjacent ranks of nodes
            ranksep: minimum horizontal distance between adjacent nodes of equal rank
    """
        mygraph = pydot.Dot(rankdir='LR',graph_type='digraph',nodesep='1',ranksep='2')
                
        thing_nodes = []
        i = 0
        s = '"'
        hop = 15000
        color = 100000

        for thing in AThing.objects.all():
            t_node = pydot.Node(thing.__unicode__().replace("::"," ").replace("\"",""), style="filled", fillcolor="green")
            thing_nodes.insert(i,t_node)
            #mygraph.add_node(t_node)
            #print "add thing node: %s" % (t_node.get_name())
            i = i + 1

        color += hop
        even = 0
         
        group_node = pydot.Node(selected_group.__unicode__().replace("\"",""), style="filled", fillcolor="red")
        #print group.__unicode__().replace("\"","")
        mygraph.add_node(group_node)
        #print "add group node: %s" % (group_node.get_name())
        for thing in selected_group.thing_set.all():
            for thing_node in thing_nodes:
                #print "GROUP: %s; %s" % (group.__unicode__(), s + thing.__unicode__().replace("::"," ") + s)
                #print thing_node.get_name()
                if (s + thing.__unicode__().replace("::"," ") + s) == thing_node.get_name():
                    #print '#' + str(color)
                    mygraph.add_node(thing_node)
                    edge = pydot.Edge(group_node, thing_node,color='#' + str(color))
                    mygraph.add_edge(edge)
                    #print "add edge from: %s to: %s" % (group_node.get_name(),thing_node.get_name())
                    break
        file_dir = settings.PROJECT_ROOT + "/static/"
        filename = "image" + str(random.randrange(0,9999)) + ".png"
        mygraph.write_png(file_dir + filename)
        #mygraph.write_png(settings.PROJECT_ROOT + "/static/prova.png")

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('connect.views.result', args=(selected_group.name,"prova.png",)))
        return HttpResponseRedirect(reverse('result', args=(selected_group.name,selected_group.city,filename,)))


def result(request,group,place,filename):
    
    return render_to_response('result.html',{'group': group,'place': place,'filename':filename},context_instance=RequestContext(request))
