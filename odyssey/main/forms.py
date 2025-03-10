from django import forms

from .models import JourneyInformation

class JourneyInformationForm(forms.ModelForm):
    class Meta:
        model = JourneyInformation
        fields = '__all__'
    
    def clean(self):
        for field, value in self.cleaned_data.items(): 
            self.cleaned_data['field'] = value.lower() 