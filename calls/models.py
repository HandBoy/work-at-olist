from datetime import timedelta

from django.db import models

# Create your models here.
TYPE = (
    ('S', 'Start'),
    ('E', 'End'),
)


class Call(models.Model):
    duration = models.DurationField(blank=True)
    price = models.FloatField(blank=True, default=0)

    def get_duration(self):
        # formating duration
        days = self.duration.days
        seconds = self.duration.seconds

        minutes = seconds // 60
        seconds = seconds % 60

        hours = minutes // 60 + (days*24)
        minutes = minutes % 60

        return '{:02d}h:{:02d}m:{:02d}s'.format(hours, minutes, seconds)



class CallStart(models.Model):
    type = models.CharField(max_length=1, choices=TYPE, default='S')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(Call, on_delete=models.CASCADE, 
                                related_name='call_start')
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return self.source
        

class CallEnd(models.Model):
    type = models.CharField(max_length=1, choices=TYPE, default='E')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(Call, on_delete=models.CASCADE,
                                related_name='call_end')


class RatePlans(models.Model):
    name = models.CharField(max_length=100)
    standard_time_start = models.TimeField()
    standard_time_end = models.TimeField()
    standing_time_charge = models.FloatField()
    standing_time_minute = models.FloatField()
    reduced_time_start = models.TimeField()
    reduced_time_end = models.TimeField()
    reduced_time_charge = models.FloatField()
    reduced_time_minute = models.FloatField()
