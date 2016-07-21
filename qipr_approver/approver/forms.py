
from django import forms
from approver.models import Training

def get_training_section():
	trainings = [(training.pk,training.name) for training in Training.objects.all()]
	return forms.MultipleChoiceField(choices=trainings, widget=forms.CheckboxSelectMultiple())

class ProjectForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    proposed_start_date = forms.DateField(label='Proposed Start Date',
                                          widget=forms.DateInput({'type':'date'}))
    proposed_end_date = forms.DateField(label='Proposed End Date',
                                        widget=forms.DateInput({'type':'date'}))

class AboutYouForm(forms.Form):
    user_name = forms.CharField(label='UserName', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    webpage_url = forms.CharField(label='Personal Webpage Url', max_length=100)
    email = forms.EmailField(label='GatorLink Email',max_length= 50)
    business_phone = forms.IntegerField(label='Business Phone')
    contact_phone = forms.IntegerField(label='Contact Phone')
    training = get_training_section()
