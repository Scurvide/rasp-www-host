from django.db import models

# Models used for database

class Client( models.Model ):
    name = models.CharField( max_length = 30, unique = True )
    secretId = models.CharField( max_length = 30, unique = True )
    current_command = models.CharField( max_length = 30 )

class Command( models.Model ):
    name = models.CharField( max_length = 30, unique = True )
    client = models.ManyToManyField( Client )

class Datapoint( models.Model ):
    client = models.ForeignKey( Client, on_delete = models.CASCADE )
    command = models.ForeignKey( Command, on_delete = models.CASCADE )
    point = models.DecimalField( max_digits = 10, decimal_places = 2 )
    unit = models.CharField( max_length = 5 )
    datetime = models.DateTimeField( auto_now_add = True )
