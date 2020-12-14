from django import forms
from apiSNN.models import UploadImage

class ImageForm(forms.ModelForm):
    
    class Meta:
        model = UploadImage
        fields = ['image']