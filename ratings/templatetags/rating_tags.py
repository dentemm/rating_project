from django import template

from .models import Vote

register = template.Library()


def rating_for_user(parser, token):
	'''
	Ga na of de gebruiker reeds een Vote heeft uitgebracht op een gegeven object,
	en voeg het Vote object toe aan de context als het bestaat. Zoniet is de value 0

	Gebruik: {% rating_by_user on instance as vote %} 
	'''

	bits = token.contents.split()

	if len(bits) != 6:
		raise template.TemplateSyntaxError(" '%s' aanvaardt exact 5 argumenten" % (bits[0],) )

	if bits[2] != 'on':
		raise template.TemplateSyntaxError("Tweede argument van '%s' moet 'on' zijn" % (bits[0], ) )

	if bits[4] != 'as':
		raise template.TemplateSyntaxError("Vierde argument van '%s' moet 'as' zijn" % (bits[0], ) )

	return RatingByUser(bits[1], bits[3], bits[5])

register.tag('rating_by_user', rating_for_user)
