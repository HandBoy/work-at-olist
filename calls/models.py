
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Create your models here.

# Enumeration makes further modifications, if necessary, easier
CALL_TYPES = (
    ('S', 'Start'),
    ('E', 'End'),
)

# Setting the validator for the phone according to the
# the repository's guidelines
# Phone numbers have to be all digits (0-9)
# Their length has to be between 10 (2 area digits + 8 phone digits)
# and 11 (2 area digits + 9 phone digits)
phone_validator_regex = RegexValidator(
    regex=r'^\d{10,11}$',
    code="invalid_phone_number",
    message='Phone numbers must be all digits,'
    + ' with 2 area code digits and 8 or 9 phone number digits.'
)


class Charge(models.Model):
    """
    Class to save a a charge  phone
    """
    name = models.CharField(max_length=100)
    standard_time_start = models.TimeField()
    standard_time_end = models.TimeField()
    standing_time_charge = models.FloatField()
    standing_time_minute = models.FloatField()
    reduced_time_start = models.TimeField()
    reduced_time_end = models.TimeField()
    reduced_time_charge = models.FloatField()
    reduced_time_minute = models.FloatField()


class Call(models.Model):
    """
    Class to save a duration and price of a call
    Its is the link (one to one) between classes StartCall and EndCall
    """
    duration = models.DurationField(blank=True, null=True)
    price = models.FloatField(blank=True, default=0)
    charge = models.ForeignKey(
        Charge,
        on_delete=models.CASCADE,
        related_name='charge',
        default=1)

    def format_duration(self):
        """
        format the duration according the repository's guidelines
        if duration: 11:43:23.032322
        this return: 11h43m23s
        """
        days, seconds = self.duration.days, self.duration.seconds
        hours = (days * 24) + (seconds // 3600)
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return '{:02d}h:{:02d}m:{:02d}s'.format(hours, minutes, seconds)

    def format_price(self):
        """
        format the price according the repository's guidelines
        if prive: 6.3452234
        this return: R$6.34
        """
        return ('R$%.2f' % (self.price))


class CallStart(models.Model):
    """
    Class to save when the call started,
    what number started the call and the number that received the call
    """
    type = models.CharField(
        max_length=1,
        choices=CALL_TYPES,
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

    def validate_source_and_destination(self):
        '''
        Validates that call records cannot have the same source and
        destination, if the fields exist, if their size is adequate
        or whether they are the same.
        '''
        if self.source is None:
            raise ValidationError(
                'Cannot create a call with no source')

        elif self.destination is None:
            raise ValidationError(
                'Cannot create a call without no destination')

        elif self.source == self.destination:
            raise ValidationError(
                'Cannot create a call where source'
                + ' is the same as the destination.')

        if ((len(self.source) < 9) or (len(self.source) > 11)):
            raise ValidationError(
                'Phone numbers must be all digits, with 2 area code digits'
                + ' and 8 or 9 phone number digits.')

        if ((len(self.destination) < 9) or (len(self.destination) > 11)):
            raise ValidationError(
                'Phone numbers must be all digits, with 2 area code digits'
                + ' and 8 or 9 phone number digits.')

    def save(self, *args, **kwargs):
        """
        Validate models fields

        Override the models.Model.save() method to ensure
        don't create a record in which there are invalid or
        inconsistent fields.
        """
        self.validate_source_and_destination()

        super(CallStart, self).save(*args, **kwargs)


class CallEnd(models.Model):
    """
    Class to save when the call ended
    """
    type = models.CharField(
        max_length=1,
        choices=CALL_TYPES,
        default='E')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='call_end')
