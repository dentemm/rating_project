from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Score(models.Model):
	'''
	Een score voor een bijhorende content object
	'''
	content_type = models.ForeignKey(ContentType)



class Vote(models.Model):
	'''
	Een enkele stem voor een bepaald content object, gelinkt aan een gebruiker
	'''

	content_type = models.ForeignKey(ContentType)
	user = models.ForeignKey(User, related_name='votes')

	class Meta:

		# Een gebruiker kan maar 1 stem uitbrengen op een bepaald object
		unique_together = (	
			('content_type', 'object_id', 'user')
		)

