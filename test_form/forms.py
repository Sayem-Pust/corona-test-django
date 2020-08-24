from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Profile
        fields = ['name', 'age', 'gender', 'body_temperature', 'symptom', 'result', 'additional', 'user', 'advice', 'score',
                  'is_tested', 'emergency_info']
        widgets = {'result': forms.HiddenInput(), 'user': forms.HiddenInput(), 'advice': forms.HiddenInput(),
                   'score': forms.HiddenInput(), 'is_tested': forms.HiddenInput(), 'emergency_info': forms.HiddenInput()}

    def clean_name(self):
        name = self.cleaned_data.get('name')

        for instance in Profile.objects.all():
            if instance.name == name:
                raise forms.ValidationError('Already Exists')
        return name


class ProfileSearchForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'export_to_CSV']
        labels = {
            'name': 'Search Profile'
        }
