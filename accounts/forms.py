from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UpdateUserProfileForm(UserChangeForm):
    password = None

    class Meta :
        model = User 
        fields = ['username','first_name','last_name','email','date_joined']
        labels = {'email': 'Email'}



# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer  # Replace with your actual model
#         fields = ['phone_no']

#     # def __init__(self, *args, **kwargs):
#     #     super(CustomerForm, self).__init__(*args, **kwargs)
#     #     # Exclude the user field from the form
#     #     self.fields['phone_no'].initial = self.instance.phone_no
        