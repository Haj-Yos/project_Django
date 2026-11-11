from django.db import models


class Mesure(models.Model):
    topic = models.CharField(max_length=100)
    value = models.FloatField()
    date_prise = models.DateTimeField()
    date_reception = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_prise']

    def __str__(self):
        return f"{self.topic} = {self.value} @ {self.date_prise:%Y-%m-%d %H:%M:%S}"