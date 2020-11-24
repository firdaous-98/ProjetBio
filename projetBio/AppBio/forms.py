from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Analysis
from django.forms import ClearableFileInput
from django.contrib.auth.models import User

User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email' , 'password1' ,'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('The user is not active')
        return super(UserLoginForm,self).clean(*args,**kwargs)

class ResumeUpload(forms.ModelForm):

    mapping_file = forms.FileField(label='Mapping File')
    sample_size = forms.IntegerField(label = 'Normalization value:Number of reads per samples (default: 50000)')
    min_otu_freq = forms.FloatField(label='Minimum size for an OTU as fraction of all OTUs (default: 0.001)')
    p_perc_identity = forms.FloatField(label='Percent identity for OTUs classifier (default: 0.97)',max_value=0.97, min_value=0.93)


    class Meta:
        model = Analysis
        fields = ['fastq_files', 'mapping_file', 'sample_size', 'min_otu_freq', 'p_perc_identity']
        widgets = {
            'fastq_files': ClearableFileInput(attrs={'multiple': True}),
        }