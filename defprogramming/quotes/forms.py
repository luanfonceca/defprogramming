from django import forms
from django.core.mail import send_mail
from django.conf import settings

class QuoteForm(forms.Form):
  name = forms.CharField(label='Your name', max_length=50)
  email = forms.EmailField(label='Your e-mail')
  quote = forms.Field(label='Quote', widget=forms.Textarea)
  authors = forms.CharField(label='Authors, separated by commas')
  tags = forms.CharField(label='Tags, separated by commas')
  source = forms.CharField(label='Source (website, book etc.)')

  def save(self):
    message = ("%(quote)s\n\n"
               "From: %(name)s <%(email)s>\n"
               "Authors: %(authors)s\n"
               "Tags: %(tags)s\n"
               "Source: %(source)s\n") % self.cleaned_data

    send_mail('[defprogramming] New quote',
              message,
              self.cleaned_data['email'],
              [settings.SERVER_EMAIL],
              fail_silently=False)
