# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Session(models.Model):
    id = models.TextField(primary_key=True)
    shop = models.TextField()
    state = models.TextField()
    isonline = models.BooleanField(db_column='isOnline')  # Field name made lowercase.
    scope = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    accesstoken = models.TextField(db_column='accessToken')  # Field name made lowercase.
    userid = models.BigIntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='firstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='lastName', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(blank=True, null=True)
    accountowner = models.BooleanField(db_column='accountOwner')  # Field name made lowercase.
    locale = models.TextField(blank=True, null=True)
    collaborator = models.BooleanField(blank=True, null=True)
    emailverified = models.BooleanField(db_column='emailVerified', blank=True, null=True)  # Field name made lowercase.
    refreshtoken = models.TextField(db_column='refreshToken', blank=True, null=True)  # Field name made lowercase.
    refreshtokenexpires = models.DateTimeField(db_column='refreshTokenExpires', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Session'
