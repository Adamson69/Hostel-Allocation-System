from django import forms
from django.contrib.auth.models import User
from .models import Application, StudentProfile, Hostel

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    matric_no = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=(("male","Male"),("female","Female")))
    level = forms.CharField(max_length=20, required=False)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["preferred_hostel","note"]
    preferred_hostel = forms.ModelChoiceField(
        queryset=Hostel.objects.all(), empty_label="Select hostel"
    )

    def __init__(self, *args, **kwargs):
        user_gender = kwargs.pop("user_gender", None)
        super().__init__(*args, **kwargs)
        from .models import Hostel as H
        qs = H.objects.all()
        if user_gender in ("male","female"):
            qs = qs.filter(gender=user_gender)
        self.fields["preferred_hostel"].queryset = qs
