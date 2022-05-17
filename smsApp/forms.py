from django import forms

from .models import Contact, ContactList, Campaign


class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=13, min_length=10, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    additional1 = forms.CharField(max_length=30, required=False)
    additional2 = forms.CharField(max_length=30, required=False)
    list_name = forms.ModelChoiceField(queryset=ContactList.objects.all())

    class Meta:
        model = Contact
        fields = ['phone_number', 'first_name', 'last_name', 'additional1', 'additional2', 'list_name']




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
            attrs={'rows': '5', 'cols': '90', 'placeholder': " Write your Message here"})}


"""class SingleCampaignForm(forms.ModelForm):
    include_options = (
        ("-----", "-----"),
        ("number", "number"),
        ("firstname", "firstname"),
        ("lastname", "lastname"),
        ("additional1", "additional1"),
        ("additional2", "additional2"),
    )
    title = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=14, required=True)
    list_name = forms.ModelChoiceField(queryset=ContactList.objects.all())
    include = forms.ChoiceField(choices=include_options, required=False)
    message = forms.Textarea()

    class Meta:
        model = Campaign
        fields = ['title', 'phone_number', 'list_name', 'include', 'message']"""

