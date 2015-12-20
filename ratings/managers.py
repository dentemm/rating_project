import itertools

from django.db.models import Manager
#from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType


class VoteManager(Manager):

	def get_for_user_in_bulk(self, objects, user):

		objects = list(objects)

		if len(objects) > 0:

			ctype = ContentType.objects.get_for_model(objects[0])
			votes = list(self.filter(content_type__pk=ctype.id,
									object_id__in=[obj._get_pk_val() for obj in objects],
									user__pk=user.id))
			vote_dict = dict([(vote.object_id, vote) for vote in votes])

		else:
			vote_dict = {}

		return vote_dict
