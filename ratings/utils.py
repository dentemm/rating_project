# Utility functions

from django.db import models
from django.utils.functional import memoize
from django.contrib.contenttypes.models import ContentType

from .models import Score

def _get_content(instance_or_content):
	'''
	Returns a *(content_type, object_id)* tuple for a given model instance or a *(content_type, object_id)* tuple 
	'''

	try:
		object_id = instance_or_content.pk

	except AttributeError:
		return instance_or_content

	else:
		return get_content_type_for_model(type(instance_or_content)), object_id)


def get_content_type_for_model(model):
	return ContentType.objects.get_for_model(model)

def upsert_score(instance_or_content, key):
	'''
	Update or create currecnt score values for target object. 
	Returns an *score, created* sequence
	'''

	content_type, object_id = _get_content(instance_or_content)
	score, created = Score.objects.get_or_create(content_type=content_type, object_id=object_id, key=key)

	score.recalculate()
