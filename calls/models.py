
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
TYPE = (
    ('S', 'Start'),
    ('E', 'End'),
)

# Enumeration makes further modifications, if necessary, easier
RECORD_TYPES = (
    ('S', 'Start'),
    ('E', 'End'),
)

# Here we define what a valid phone number is,
# following the repository's guidelines
# Phone numbers have to be all digits (0-9)
# Their length has to be between 10 (2 area digits + 8 phone digits)
# and 11 (2 area digits + 9 phone digits)
phone_validator_regex = RegexValidator(
    regex=r'^\d{10,11}$',
    code="invalid_phone_number",
    message='Phone numbers must be all digits,'
    + ' with 2 area code digits and 8 or 9 phone number digits.'
)


class Call(models.Model):
    duration = models.DurationField(blank=True, null=True)
    price = models.FloatField(blank=True, default=0)

    def format_duration(self):
        # formating duration
        days, seconds = self.duration.days, self.duration.seconds
        hours = (days * 24) + (seconds // 3600)
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return '{:02d}h:{:02d}m:{:02d}s'.format(hours, minutes, seconds)

    def format_price(self):
        return ('R$%.2f' % (self.price))


class CallStart(models.Model):
    type = models.CharField(
        max_length=1,
        choices=TYPE,
        default='S')

    call_id = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='call_start')

    source = models.CharField(
        validators=[phone_validator_regex],
        max_length=11)

    destination = models.CharField(
        validators=[phone_validator_regex],
        max_length=11)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source


class CallEnd(models.Model):
    type = models.CharField(
        max_length=1,
        choices=TYPE,
        default='E')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(
        Call, 
        on_delete=models.CASCADE,
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
