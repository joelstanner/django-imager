from django import forms
from django.forms import ModelForm
from models import ImagerProfile


class ProfileForm(ModelForm):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = ImagerProfile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['follows'].queryset = ImagerProfile.objects.exclude(
            user=kwargs['instance'].user)
        self.fields['blocked'].queryset = ImagerProfile.objects.exclude(
            user=kwargs['instance'].user)
        self.fields['first_name'].value = kwargs['instance'].user.first_name

    def save(self, *args, **kwargs):
        obj = super(ProfileForm, self).save(*args, **kwargs)
        obj.user.first_name = self.cleaned_data['first_name']
        obj.user.last_name = self.cleaned_data['last_name']
        obj.user.email = self.cleaned_data['email']
        obj.user.save()
        return obj
