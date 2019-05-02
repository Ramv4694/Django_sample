# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class zonegroup(models.Model):
    Location = models.CharField(max_length=30)
    Class = models.CharField(max_length=30)
    FabricName = models.CharField(max_length=100)
    FabricA = models.CharField(max_length=100)
    FabricB = models.CharField(max_length=100)
    Array = models.CharField(max_length=100)


    def __str__(self):
        #return "{0}, {1}".format(self.Location,self.Class,self.FabricName,self.FabricA,self.FabricB)

        return (self.Location,self.Class,self.FabricName,self.FabricA,self.FabricB,self.Array)

    class Meta:
        managed = True

class Arraygroup(models.Model):
    Location = models.CharField(max_length=30)
    Class = models.CharField(max_length=30)
    Array = models.CharField(max_length=100)


    def __str__(self):
        #return "{0}, {1}".format(self.Location,self.Class,self.FabricName,self.FabricA,self.FabricB)

        return (self.Location,Self.Class,Self.Array)

    class Meta:
        managed = True


class Hostgroup(models.Model):
    HostName = models.CharField(max_length=100)
    FabricName = models.CharField(max_length=30)
    Class = models.CharField(max_length=30)
    Vsan = models.CharField(max_length=50)
    Wwn = models.CharField(max_length=100)

    def __str__(self):
            #return "{0}, {1}".format(self.Location,self.Class,self.FabricName,self.FabricA,self.FabricB)
        return (self.Host,Self.FabricName,Self.Class,Self.Vsan,Self.Wwn)
    class Meta:
        managed = True
