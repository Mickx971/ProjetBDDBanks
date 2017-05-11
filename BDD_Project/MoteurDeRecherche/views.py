# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from banks.database import graph
from banks.algorithm.generic import GenericBANKS

graphs =""
node = graph.Graph()
banks = GenericBANKS()
# Create your views here.
def home(request):
    temps = datetime.datetime.now()
    request.session['graphs'] = ""
    return render(request, "home.html", locals())


def search(request):
    global graphs
    global node
    global banks
    keyword = ""
    nbrArc = 10
    treetype = True
    if 'key' in request.GET:
        keyword = request.GET.get('key', '') #ici on recupere la requette rechercher
        nbrArc = request.GET.get('arc', '')
        treetype = request.GET.get('treetype', '')

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

    trees = banks.search(keyword.split(), nbrArc, strictDiff=True)
    graphs = node.transformToClientStructure(trees)
    print len(graphs)

    return HttpResponse(len(graphs), content_type="application/json")

def graphI(request, id):
    global graphs

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


def getNoeudInfo(request, idnode):
    global node
    information = node.getNodeById(int(idnode))
    return HttpResponse(json.dumps(information), content_type="application/json")