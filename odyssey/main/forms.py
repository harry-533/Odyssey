from django import forms

from .models import JourneyInformation, Profile

# Form used on the home page to gather the users holiday information (destination, budget, dates)
class JourneyInformationForm(forms.ModelForm):
    class Meta:
        model = JourneyInformation
        fields = '__all__'
    
    def clean(self):
        cleaned_data = self.cleaned_data.copy()
        for field, value in self.cleaned_data.items(): 
            cleaned_data[field] = value
            
        return cleaned_data

# Form used to gather the new image for the user's profile image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']