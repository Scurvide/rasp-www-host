from django.db import models

class Client( models.Model ):
    name = models.CharField( max_length = 30, unique = True )
    secretid = models.CharField( max_length = 30, unique = True )
    ip = models.GenericIPAddressField()
    datamode = models.CharField( max_length = 30 )

class Datatype( models.Model ):
    name = models.CharField( max_length = 30, unique = True )
    client = models.ManyToManyField( Client )

class Datapoint( models.Model ):
    client = models.ForeignKey( Client, on_delete = models.CASCADE )
    datatype = models.ForeignKey( Datatype, on_delete = models.CASCADE )
    point = models.DecimalField( max_digits = 10, decimal_places = 2 )
    datetime = models.DateTimeField( auto_now_add = True )
