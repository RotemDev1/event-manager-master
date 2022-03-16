from django import forms
from .models import RateEvent, EventComment, EventRecommend


RATE_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class RateEventForm(forms.ModelForm):

    rate = forms.CharField(label='Rate Event:',
                           widget=forms.RadioSelect(choices=RATE_CHOICES))

    class Meta:
        model = RateEvent
        fields = ['rate']


class eventCommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        label="Add Comment:",
        widget=forms.Textarea(attrs={'style': 'max-height: 5em'}))

    class Meta:
        model = EventComment
        fields = ['text']


class eventRecommendForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        label="Say few words:",
        widget=forms.Textarea(attrs={'style': 'max-height: 2.5em'}))

    class Meta:
        model = EventRecommend
        fields = ['text']
