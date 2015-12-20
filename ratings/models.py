from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Score(models.Model):
	'''
	Een score voor een bijhorende content object
	'''
	content_type = models.ForeignKey(ContentType, related_name='score')

	# Het aantal stemmen dat werd uitgebracht om tot de huidige score te komen
	votes_count = models.PositiveIntegerField(default=0) 
	# De feitelijke score
	score = models.DecimalField() 

	def get_votes(self):

		return Vote.objects.filter(content_type=self.content_type, object_id=self.object_id)

	def recalculate(self, weight=0):

		existing_votes = self.get_votes()



class Vote(models.Model):
	'''
	Een enkele stem voor een bepaald content object, gelinkt aan een gebruiker
	'''

	content_type = models.ForeignKey(ContentType)
	user = models.ForeignKey(User, related_name='votes')
	# Een unique identifier voor een model instance, dit is typisch de pk van het object
	object_id = models.PositiveIntegerField()
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
	'''
	Voeg deze mixin toe aan een model dat je wil raten, of waarvan je bepaalde fields (ForeignKey fields) wil raten
	'''

	# All rateable fields of a given object
	rating_fields = ArrayField()
	# Voor elk van deze fields wordt een score bijgehouden, via een dict (key-value = field-rating)
	field_scores = JSONField()

	def field_score(self, field):

		return 10

	def global_score(self):

		for field in self.rating_fields:

			current_score = field_scores[field]


	'''def __init__(self, fields=[]):

		for field in fields:

			self.fields.append(field)'''

