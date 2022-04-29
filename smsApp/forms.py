from django import forms
from .models import Contact, ContactList, Campaign


class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=13, min_length=10, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    additional1 = forms.CharField(max_length=30, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    additional2 = forms.CharField(max_length=30, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    list_name = forms.ModelChoiceField(queryset=ContactList.objects.all())

    class Meta:
        model = Contact
        fields = ['phone_number', 'first_name', 'last_name', 'additional1', 'additional2', 'list_name']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['list_name'].widget.attrs['class'] = 'form-control form-select'


class CampaignForm(forms.ModelForm):
    include_options = (
        ("-----", "-----"),
        ("number", "number"),
        ("firstname", "firstname"),
        ("lastname", "lastname"),
        ("additional1", "additional1"),
        ("additional2", "additional2"),
    )
    title = forms.CharField(max_length=100, required=False)
    list_name = forms.ModelChoiceField(queryset=ContactList.objects.all())
    include = forms.ChoiceField(choices=include_options, required=False)
    message = forms.Textarea()

    class Meta:
        model = Campaign
        fields = ['title', 'list_name', 'include', 'message']
        widgets = {'message': forms.Textarea(
            attrs={'rows': '5', 'cols': '90', 'max_length': '160', 'class': 'form-control',
                   'placeholder': " Write your Message here"})}
