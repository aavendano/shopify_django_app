from django.db import models


class ShopConfig(models.Model):
    shop = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    isonline = models.BooleanField(default=False)  # Field name made lowercase.
    scope = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)  # Field name made lowercase.
    refresh_token = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    refresh_token_expires = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
