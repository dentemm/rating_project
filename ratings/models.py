from __future__ import unicode_literals

from datetime import datetime

from django.db import models
#from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User

from .managers import VoteManager

# Create your models here.

__all__ = ('Score', 'Vote', )

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
	# De feitelijke score (totaalsom ?)
	score = models.IntegerField() 

	key = models.CharField(max_length=32)

	class Meta:
		unique_together = (
			('content_type', 'object_id', 'key')
		)

	def __unicode__(self):
		return u'%s scored %s with %s votes' % (self.content_object, self.score, self.votes_count)

	def get_votes(self):

		return Vote.objects.filter(content_type=self.content_type, object_id=self.object_id, key=self.key)

	
	def recalculate(self, commit=True):

		existing_votes = self.get_votes()



class Vote(models.Model):
	'''
	Een enkele stem voor een bepaald content object, gelinkt aan een gebruiker
	'''

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'content_id')

	# De gebruiker die een stem uitbrengt
	user = models.ForeignKey(User, related_name='votes')

	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)

	objects = VoteManager()


	class Meta:

		# Een gebruiker kan maar 1 stem uitbrengen op een bepaald object
		unique_together = (	
			('content_type', 'object_id', 'user')
		)

	def __unicode__(self):
		return u'%s gaf een score van %s op %s' % (self.user, self.score, self.content_object) 

	def save(self, *args, **kwargs):
		self.modified_at = datetime.now()

		super(Vote, self).save(*args, **kwargs)





# Niet meer nodig, zal worden vervangen door een field
class RatingMixin(models.Model):
	'''
	Voeg deze mixin toe aan een model dat je wil raten, of waarvan je bepaalde fields (ForeignKey fields) wil raten
	'''

	scores = GenericRelation(Score)
	votes = GenericRelation(Vote)

	class Meta:
		abstract = True

	# Wat is key hier? mss het field?
	def get_score(self, key):
		return Score.objects.get_for(self, key)



