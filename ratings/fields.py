from datetime import datetime

from django.db.models import PositiveIntegerField
from django.contrib.contenttypes.models import ContentType


from .models import Score, Vote

class Rating(object):

	def __init__(self, score, votes):
		self.score = score
		self.votes = votes

class RatingManager(object):

	def __init__(self, instance, field):

		self.content_type = None
		self.instance = instance
		self.field = field

		self.votes_field_name = "%s_votes" % (self.field.name, )
		self.score_field_name = "%s_score" % (self.field.name, )

	def get_ratings(self):
		'''
		Returns a Vote queryset
		'''

		return Vote.objects.filter(content_type=self.get_content_type(), object_id=self.instance.pk, key=self.field.key)

	def get_rating_for_user(self, user):
		'''
		Returns the rating for a given user
		'''

		kwargs = dict (

			content_type = self.get_content_type(),
			object_id = self.instance.pk,
			key = self.field.key,
		)

class RatingField(PositiveIntegerField):

	def __init__(self, *args, **kwargs):

		super(RatingField, self).__init__(*args, **kwargs)