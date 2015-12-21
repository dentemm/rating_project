from datetime import datetime
#from md5 import new as md5

from django.db.models import PositiveIntegerField, IntegerField
from django.contrib.contenttypes.models import ContentType

from .models import Score, Vote
from .forms import RatingFormField

class Rating(object):
	'''
	This is a python object to represent a rating. 
	'''

	def __init__(self, score, votes):
		self.score = score
		self.votes = votes

class RatingManager(object):
	'''
	RatingManager 
	'''

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

	def get_score(self):

		if not (self.votes and self.score):
			return 0

		return float(self.score/self.votes)

	def get_rating_for_user(self, user):
		'''
		Returns the rating for a given user
		'''

		kwargs = dict (

			content_type = self.get_content_type(),
			object_id = self.instance.pk,
			key = self.field.key,
		)

class RatingCreator(object):
	'''
	RatingCreator creates a python Rating object, and is used on RatingField 
	'''

	def __init__(self, field):

		self.field = field
		self.votes_field_name = '%s_votes' % (self.field.name, )
		self.score_field_name = '%s_score' % (self.field.name, )

	def __get__(self, instance, type=None):
		if instance = None:
			return self.field

		return RatingManager(instance, self.field)

	def __set__(self, instance, value):
		if isinstance(value, Rating):
			setattr(instance, self.votes_field_name, value.votes)
			setattr(instance, self.score_field_name, value.score)

		else:
			raise TypeError("%s value must be a Rating instance, not '%r' " % (self.field.name, value))


class RatingField(PositiveIntegerField):
	'''
	Rating field voegt 2 DB kolommen toe, namelijk het aantal votes en de score (totaalscore als som)
	'''

	def __init__(self, *args, **kwargs):

		self.range = kwargs.pop('range', 5)
		# self.weight = kwargs.pop('range', 0) if trying to implement weight based ratings

		kwargs['default'] = 0
		kwargs['blank'] = True

		super(RatingField, self).__init__(*args, **kwargs)

	def contribute_to_class(self, cls, name):

		self.name = name
		#self.key = md5(self.name).hexdigest()

		# votes field
		self.votes_field = PositiveIntegerField(editable=False, default=0, blank=True)
		cls.add_to_class('%s_votes' % (self.name, ), self.votes_field) # Add <model_name>_votes to class

		# score sum field
		self.score_field = IntegerField(editable=False, default=0, blank=True)
		cls.add_to_class('%s_score' % (self.name, ), self.score_field) # Add <model_name>_score to class

		field = RatingCreator(self)

		if not hasattr(cls, '_ratings'):
			cls._ratings = []

		cls._ratings.append(self)

		setattr(cls, name, field)


	def formfield(self, **kwargs):

		defaults = {'form_class': forms.RatingFormField}
		defaults.update(kwargs)

		return super(RatingField, self).formfield(**defaults)

