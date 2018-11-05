from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from Datamana.models import Client, Datatype, Datapoint


def index( request ):

    return HttpResponse( "See data here!" )
