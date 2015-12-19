from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Score(models.Model):
	'''
	Een score voor een bijhorende content object
	'''
	content_type = models.ForeignKey(ContentType)

	votes_counts = models.PositiveIntegerField() # Het aantal stemmen dat werd uitgebracht om tot de huidige score te komen
	score = models.DecimalField() # De feitelijke score



class Vote(models.Model):
	'''
	Een enkele stem voor een bepaald content object, gelinkt aan een gebruiker
	'''

	content_type = models.ForeignKey(ContentType)
	user = models.ForeignKey(User, related_name='votes')
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:

		# Een gebruiker kan maar 1 stem uitbrengen op een bepaald object
		unique_together = (	
			('content_type', 'object_id', 'user')
		)

	def __unicode__(self):
		return 'Score van %s' % (self.user)

class RatingMixin(models.Model):

	fields = ArrayField()

	def __init__(self, fields={}):

		for key in fields:





