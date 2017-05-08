# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import datetime

# Create your views here.
def home(request):
    temps = datetime.datetime.now()
    return render(request, "home.html", locals())


def search(request):
    Html_to_return = ""

    if 'key' in request.GET:
        keyword = request.GET.get('key', '') #ici on recupere la requette rechercher

        # Code a ajouter pour faire une recherche dans La DB Graph
        # ..
        # ..

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
        text_file = open("static/g.json", "w")
        text_file.write(j)
        text_file.close()

        return HttpResponse("true")
