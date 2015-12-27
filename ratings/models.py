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

	# Create relation to ContentType (content_type, content_id and content_object attributes needed)
	content_type = models.ForeignKey(ContentType)
	content_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'content_id') # generic relation

	# DB optimalization
	#key = models.CharField(max_length=32)

	votes_count = models.PositiveIntegerField(default=0) 
	total_score = models.IntegerField(default=0) 
	average = models.FloatField(default=0)


	class Meta:
		unique_together = (
			('content_type', 'object_id', )
		)

	def __unicode__(self):
		return u'%s scored %s with %s votes' % (self.content_object, self.score, self.votes_count)

	@property
	def percentage(self):
	    return 100 * (self.average / defaults.RANGE)

	def to_dict(self):
		return {
			'count': self.votes_count,
			'total': self.total_score,
			'average' : self.average,
			'percentage': self.percentage,
		}
	

	def get_votes(self):

		return Vote.objects.filter(content_type=self.content_type, object_id=self.object_id, key=self.key)

	
	def recalculate(self, commit=True):

		existing_votes = self.get_votes().aggregate(total=models.Sum('score'), votes_count=models.Count('id'), average=models.Avg('score'))

		self.total_score = existing_votes['total_score'] or 0
		self.votes_count = existing_votes['votes_count']

		if self.votes_count:
			self.average = self.total_score / self.votes_count

		else:
			self.average = 0

		if commit:
			self.save()



class Vote(models.Model):
	'''
	Een enkele stem voor een bepaald content object, gelinkt aan een gebruiker
	'''

	# Create relation to ContentType (content_type, content_id and content_object attributes needed)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'content_id')

	key = models.CharField(max_length=32)
	score = models.FloatField()

	# De gebruiker die een stem uitbrengt
	user = models.ForeignKey(User, related_name='votes')

	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)

	objects = VoteManager()


	class Meta:

		# Een gebruiker kan maar 1 stem uitbrengen op een bepaald object
		unique_together = (	
			('content_type', 'object_id', 'key', 'user')
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




