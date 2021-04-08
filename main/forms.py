from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .mongo import mongodata
import datetime
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class NameForm(forms.Form):
    db = mongodata()
    trainerList = db.trainer_names()
    Trainer = forms.ChoiceField(choices=[(x, x) for x in trainerList])
    collegeList = db.college_names()
    College = forms.ChoiceField(choices=[(x, x) for x in collegeList])
    Start_Date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    Start_Date.widget.attrs.update({'class': 'datepicker', 'autocomplete':'off'})
    End_Date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    End_Date.widget.attrs.update({'class': 'datepicker', 'autocomplete':'off'})
    Hours_per_day = forms.IntegerField()
    c1 = [('online', 'Online'), ('offline', 'Offline')]
    Mode_of_Training = forms.ChoiceField(choices=c1, widget=forms.RadioSelect)
    Pay_per_day = forms.IntegerField()
    c2 = [('Yes', 'Yes'), ('No', 'No')]
    Food = forms.ChoiceField(choices=c2, widget=forms.RadioSelect)
    Accomodation = forms.ChoiceField(choices=c2, widget=forms.RadioSelect)

    def clean_Hours_per_day(self):
        hours = self.cleaned_data['Hours_per_day']
        if hours < 0:
            raise forms.ValidationError("Hours per day should be greater than zero")
        return hours

    def clean_Pay_per_day(self):
        pay = self.cleaned_data['Pay_per_day']
        if pay < 0:
            raise forms.ValidationError("Pay per day should be greater than zero")
        return pay

    def clean_Start_Date(self):
        sd = self.cleaned_data['Start_Date']
        if sd < datetime.date.today():
            raise forms.ValidationError("*The date cannot be in the past")
        return sd
    def clean_End_Date(self):
        ed = self.cleaned_data['End_Date']
        if ed < datetime.date.today():
            raise forms.ValidationError("*The date cannot be in the past")
        return ed


class TrainerForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.CharField(max_length=50)
    phno = forms.CharField(max_length=10)
    location = forms.CharField(max_length=30)
    bank = forms.CharField(max_length=20)
    acc_no = forms.CharField(max_length=15)
    ifsc = forms.CharField(max_length=10)
    pan = forms.CharField(max_length=10)

class CollegeForm(forms.Form):
    name = forms.CharField(max_length=50)
    location = forms.CharField(max_length=30)