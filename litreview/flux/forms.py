from django.forms import ModelForm, Textarea, RadioSelect

from .models import Ticket, Review


class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = ('title', 'description', 'image')
		labels = {
			'title': 'Titre',
			'description': 'Description',
			'image': 'Image (optionel)'
		} 


class ReviewForm(ModelForm):
	class Meta:
		CHOICES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')]
		model = Review
		fields = ('headline', 'body', 'rating')
		labels = {
			'headline': 'Livre',
			'body': 'Critique',
			'rating': 'Note'
		}
		widgets = {
			'rating': RadioSelect(choices=CHOICES)
		}