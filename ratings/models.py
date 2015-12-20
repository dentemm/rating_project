from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Score(models.Model):
	'''
	Een score voor een bijhorende content object. 
	'''

	# ContentType generic relations: content_type en content_id required!
	content_type = models.ForeignKey(ContentType)
	content_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'content_id') # generic relation

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

	# Het model waarop wordt gestemd
	content_type = models.ForeignKey(ContentType)
	# De gebruiker die een stem uitbrengt
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

	scores = GenericRelation(Score)
	votes = GenericRelation(Vote)

	class Meta:
		abstract = Trur

	# Wat is key hier? mss het field?
	def get_score(self, key):
		return Score.objects.get_for(self, key)

	'''
	def field_score(self, field):

		return 10

	def global_score(self):

		for field in self.rating_fields:

			current_score = field_scores[field]'''


	'''def __init__(self, fields=[]):

		for field in fields:

			self.fields.append(field)'''

