from django import forms

from .models import JourneyInformation, Profile

class JourneyInformationForm(forms.ModelForm):
    class Meta:
        model = JourneyInformation
        fields = '__all__'
    
    def clean(self):
        cleaned_data = self.cleaned_data.copy()
        for field, value in self.cleaned_data.items(): 
            cleaned_data[field] = value
            
        return cleaned_data
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']