import itertools

from django.db.models import Manager
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType


class VoteQuerySet(QuerySet):

	pass

class VoteManager(Manager):

	def get_for_user_in_bulk(self, objects, user):

		objects = list(objects)

		if len(objects) > 0:

			content_type = ContentType.objects.get_for_model(objects[0])
			votes = list(self.filter(content_type__pk=content_type.id,
									object_id__in=[obj._get_pk_val() for obj in objects],
									user__pk=user.id))
			vote_dict = dict([(vote.object_id, vote) for vote in votes])

		else:
			vote_dict = {}

		return vote_dict

class RatingsManager(models.Manager):
	'''
	-- In case of mixin solution --

	This manager is used by Vote AND Score models => generic code (contenttypes framework) needed
	'''

	def get_score_or_vote_for(self, content_object, key, **kwargs):
		# Return Vote or Score DB object for given key, content_type and object_id (so unique!)
		# Was previously named get_for(...)

		content_type = ContentType.objects.get_for_model(type(content_object))

		try:
			# Return Vote or Score DB object for given key, content_type and object_id (so unique!)
			return self.get(key=key, content_type=content_type, object_id=content_object.pk, **kwargs)

		except self.model.DoesNotExist:
			return None

	def filter_for(self, content_object_or_model, **kwargs):
		# Return all Votes or Score related to *content_object_or_model* 
		# content_object_or_model can either be a model instance or a model class

		if isinstance(content_object_or_model, models.base.ModelBase):
			lookups = {
				'content_type': ContentType.objects.get_for_model(type(content_object_or_model)),
			}

		else:
			lookups = {
				'content_type': ContentType.objects.get_for_model(type(content_object_or_model)),
				'object_id': content_object_or_model.pk,
			}

		lookups.update(kwargs)

		return self.filter(**lookups)

	def score_or_votes_for_user(self, **kwargs):
		# Return all Vote or Score instances for a given user

		if 'user' in kwargs:
			user = kwargs.pop('user')
			queryset = self.filter_for(user, **kwargs):

		else:
			queryset = self.filter(**kwargs)

		return QuerysetWithContents(queryset)

