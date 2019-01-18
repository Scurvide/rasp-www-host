from django.shortcuts import render

# Base page renderer

def index( request ):

    return render( request, 'base.html' )
