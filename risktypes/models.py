
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class RiskType(models.Model):
	user_risktype = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE,)
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	date_created = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	# this is not used in the pilot but reserved for the real app
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

	class Meta:
		verbose_name = 'RiskType'
		verbose_name_plural = 'RiskTypes'

class RiskField(models.Model):
	user_riskfield = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE,)
	risktype = models.ForeignKey(RiskType, related_name="risktype_riskfield", on_delete = models.CASCADE,)
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	TEXT = 1
	NUMBER = 2
	DATE = 3
	ENUM = 4
	
	TYPE_CHOICES = (
		(TEXT, 'Text'),
		(NUMBER, 'Number'),
		(DATE, 'Date'),	
		(ENUM, 'Enum'),	
	)
	type = models.CharField(max_length=256,choices=TYPE_CHOICES,
		default=TEXT)
    
	length = models.IntegerField( default = 256, validators=[MaxValueValidator(1e65)])
	len_decim = models.IntegerField( default = 0,validators=[MaxValueValidator(1e30)])
	min_value = models.IntegerField( default = 0, validators=[MinValueValidator(-1e65)])
	max_value = models.IntegerField( default = 256, validators=[MaxValueValidator(1e65)])
	order = models.IntegerField(default = 1)
	is_nullable = models.BooleanField(default=True)
	enum_values = models.TextField(default = '')
	date_created = models.DateTimeField(default=timezone.now)
	
	class Meta:
		verbose_name = 'RiskField'
		verbose_name_plural = 'RiskFields'
