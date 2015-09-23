from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class List(models.Model):

    @property
    def name(self):
        first_text = self.item_set.first().text.split(" ")
        return " ".join(first_text[0:5]) + "..."
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):

    def __str__(self):
        return self.text 

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
