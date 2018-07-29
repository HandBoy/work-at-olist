from django.db import models

# Create your models here.

class Call(models.Model):
    duration = models.DurationField()
    price =  models.FloatField()

class CallStart(models.Model):
    TYPE = (
    ('S', 'Start'),
    ('E', 'End'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='call_start')
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return self.source

class CallEnd(models.Model):
    TYPE = (
    ('S', 'Start'),
    ('E', 'End'),
    )
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