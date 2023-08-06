from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from djangoldp_account.models import ChatConfig


class Circle(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    team = models.ManyToManyField(User, blank=True)
    owner = models.ForeignKey(User, related_name="owned_circles", on_delete=models.DO_NOTHING)
    chatConfig = models.ForeignKey(ChatConfig, related_name="circles", on_delete=models.DO_NOTHING, null=True)

    def get_absolute_url(self):
        return reverse_lazy('circle-detail', kwargs={'pk': self.pk})

    class Meta:
        permissions = (
            ('view_circle', 'Read'),
            ('control_circle', 'Control'),
        )

    def __str__(self):
        return self.name
