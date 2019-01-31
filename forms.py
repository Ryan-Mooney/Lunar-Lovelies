from django import forms

class ProductFilterForm(forms.Form):
	input_type='checkbox'
	clothes=forms.BooleanField(required=False)
	dresses=forms.BooleanField(required=False)
	shirts=forms.BooleanField(required=False)
	crafts=forms.BooleanField(required=False)

class ContactMailer(forms.Form):
	email_address=forms.EmailField(required=True)
	contact_message=forms.CharField(required=True)

class SubscribeForm(forms.Form):
	email_address=forms.EmailField(required=True)