from django.db import models

class Raspi( models.Model ):
    name = models.CharField( max_length = 30, unique = True )
    ip = models.GenericIPAddressField()

class Datapoint( models.Model ):
    client = models.ForeignKey( Raspi, on_delete = models.CASCADE )
    type = models.CharField( max_length = 30 )
    point = models.DecimalField( max_digits = 10, decimal_places = 2 )
    datetime = models.DateTimeField( auto_now_add = True )
