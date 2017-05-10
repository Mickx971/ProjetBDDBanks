# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json

graphs =""
# Create your views here.
def home(request):
    temps = datetime.datetime.now()
    request.session['graphs'] = ""
    return render(request, "home.html", locals())


def search(request):
    global graphs
    if 'key' in request.GET:
        keyword = request.GET.get('key', '') #ici on recupere la requette rechercher

        # Code a ajouter pour faire une recherche dans La DB Graph
        # ..
        # ..
        print keyword
    j = """{
    "nodes":[
        {"name":"keyword","group":1,"info":" la requeste chercher"},
        {"name":"Toufik","group":2,"info":" la requeste cherchefqsdfr"},
        {"name":"Mickix","group":3},
        {"name":"Ahmed","group":1}
    ],
    "links":[
        {"source":2,"target":1,"weight":1},
        {"source":0,"target":2,"weight":3}
    ]
    }"""
    graphs = json.loads("["+j+","+j+"]")
    return HttpResponse(len(graphs), content_type="application/json")

def graphI(request, id):
    global graphs
    #graphs = request.session.get("graphs")
    print graphs
    return HttpResponse(json.dumps(graphs[int(id)]), content_type="application/json")


def result(request):
    j = """{
      "nodes":[
    		{"name":"keyword","group":1},
    		{"name":"Toufik","group":2},
    		{"name":"Mickix","group":3},
    		{"name":"Ahmed","group":1}
    	],
    	"links":[
    		{"source":2,"target":1,"weight":1},
    		{"source":0,"target":2,"weight":3}
    	]
    }"""
    return HttpResponse(j, content_type="application/json")


def getNoeudInfo(request):
    return HttpResponse("information")