from django.db import models
from datetime import timedelta

# Create your models here.
TYPE = (
    ('S', 'Start'),
    ('E', 'End'),
)


class Call(models.Model):
    duration = models.DurationField(blank=True, default=timedelta())
    price =  models.FloatField(blank=True, default=0)

class CallStart(models.Model):
    type = models.CharField(max_length=1,choices=TYPE, default='E')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='call_start')
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return self.source


class CallEnd(models.Model):
    type = models.CharField(max_length=1,choices=TYPE, default='S')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='call_end')


'''
Call Start Record
{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}

Call End Record
{
   "id":  // Record unique identificator;
   "type":  // Indicate if it's a call "start" or "end" record;
   "timestamp":  // The timestamp of when the event occured;
   "call_id":  // Unique for each call record pair.
}

'''