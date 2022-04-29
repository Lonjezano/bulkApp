from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *
from .sms import SendSMS


class HomeView(ListView):
    model = Contact
    template_name = 'smsApp/index.html'


class ContactListView(ListView):
    model = ContactList
    template_name = 'smsApp/contact_list_view.html'
    context_object_name = 'contactlist'


class ContactListCreateView(CreateView):
    model = ContactList
    fields = '__all__'
    template_name = 'smsApp/contact_list_form.html'
    success_url = reverse_lazy('contact-list')


class ContactListDetailView(DetailView):
    model = ContactList
    template_name = 'smsApp/contact_list_detail.html'


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'smsApp/contact_form.html'
    success_url = reverse_lazy('contact-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["lists"] = ContactList.objects.filter(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if len(request.FILES) != 0:
            files = request.FILES['file']
            if form.is_valid():
                try:
                    if str(files).endswith(".csv"):
                        file_data = files.read().decode("utf-8")
                        lines = file_data.split("\n")
                        for line in lines:
                            fields = line.split(",")
                            try:
                                if len(line) != 0:
                                    if len(fields) < 5:
                                        missing_value = 5 - len(fields)
                                        for i in range(missing_value):
                                            fields.insert(len(fields), "")
                                    if str(fields[0]).strip().startswith('+'):
                                        contact = Contact(
                                            phone_number=str(fields[0]).strip(), first_name=fields[1],
                                            last_name=fields[2],
                                            additional1=fields[3], additional2=fields[4],
                                            list_name=form.instance.list_name
                                        )
                                        contact.save()
                                    else:
                                        if str(fields[0]).strip().startswith('265'):
                                            phone_number = "+" + str(fields[0]).strip()
                                            contact = Contact(
                                                phone_number=phone_number, first_name=fields[1],
                                                last_name=fields[2],
                                                additional1=fields[3], additional2=fields[4],
                                                list_name=form.instance.list_name
                                            )
                                            get_contacts = Contact.objects.filter(phone_number=phone_number,
                                                                                  list_name=form.instance.list_name).exists()
                                            if get_contacts:
                                                messages.error(request,
                                                               f"{fields[2]} already exists in {form.instance.list_name}")
                                                continue
                                            contact.save()
                                        elif str(fields[0]).strip().startswith('0'):
                                            phone_number = str(fields[0]).strip().replace('0', '+265', 1)
                                            contact = Contact(
                                                phone_number=phone_number, first_name=fields[1],
                                                last_name=fields[2],
                                                additional1=fields[3], additional2=fields[4],
                                                list_name=form.instance.list_name
                                            )
                                            get_contacts = Contact.objects.filter(phone_number=phone_number,
                                                                                  list_name=form.instance.list_name).exists()
                                            if get_contacts:
                                                messages.error(request,
                                                               f"{fields[2]} already exists in {form.instance.list_name}")
                                                continue
                                            contact.save()
                                        elif len(str(fields[0]).strip()) == 9:
                                            phone_number = "+265" + str(fields[0]).strip()
                                            contact = Contact(
                                                phone_number=phone_number, first_name=fields[1],
                                                last_name=fields[2],
                                                additional1=fields[3], additional2=fields[4],
                                                list_name=form.instance.list_name
                                            )
                                            get_contacts = Contact.objects.filter(phone_number=phone_number,
                                                                                  list_name=form.instance.list_name).exists()
                                            if get_contacts:
                                                messages.error(request,
                                                               f"{fields[2]} already exists in {form.instance.list_name}")
                                                continue
                                            contact.save()
                            except Exception as e:
                                messages.error(request, "Unable to add contacts " + repr(e))
                                pass
                        try:
                            if contact:
                                messages.success(request, f"Contacts added to {form.instance.list_name}")

                        except Exception as e:
                            print(e)
                    else:
                        messages.error(request, "Please Enter CSV")
                        redirect('contact-list')

                except Exception as e:
                    print(e)
                    messages.error(request, "Unable to upload file. " + repr(e))

                return redirect('contact-list')
            else:
                messages.error(request, "Error form no valid")
                return redirect('contact-list')
        else:
            if form.is_valid():
                get_contacts = Contact.objects.filter(phone_number=form.instance.phone_number,
                                                      list_name=form.instance.list_name).exists()
                if get_contacts:
                    messages.error(request,
                                   f"{form.instance.phone_number} already exists in {form.instance.list_name}")
                    return redirect('contact-list')
                else:
                    messages.success(request, "Contact added")
                    if str(form.instance.phone_number).strip().startswith('+'):
                        contact = Contact(
                            phone_number=str(form.instance.phone_number).strip(), first_name=form.instance.first_name,
                            last_name=form.instance.last_name,
                            additional1=form.instance.additional1, additional2=form.instance.additional2,
                            list_name=form.instance.list_name
                        )
                        contact.save()
                        return redirect('contact-list')
                    else:
                        try:
                            if str(form.instance.phone_number).strip().startswith('265'):
                                phone_number = "+" + str(form.instance.phone_number).strip()
                                contact = Contact(phone_number=phone_number,
                                                  first_name=form.instance.first_name,
                                                  last_name=form.instance.last_name,
                                                  additional1=form.instance.additional1,
                                                  additional2=form.instance.additional2,
                                                  list_name=form.instance.list_name
                                                  )
                                contact.save()
                                return redirect('contact-list')
                            elif str(form.instance.phone_number).strip().startswith('0'):
                                phone_number = str(form.instance.phone_number).strip().replace('0', '+265', 1)
                                contact = Contact(phone_number=phone_number,
                                                  first_name=form.instance.first_name,
                                                  last_name=form.instance.last_name,
                                                  additional1=form.instance.additional1,
                                                  additional2=form.instance.additional2,
                                                  list_name=form.instance.list_name)
                                contact.save()
                                return redirect('contact-list')
                        except Exception as e:
                            messages.ERROR(request, "Check phone number format")
                            return redirect('contact-list')
            else:
                return redirect('contact-list')


class CampaignListView(ListView):
    model = Campaign
    template_name = 'smsApp/campaign_view.html'
    context_object_name = 'campaigns'
    ordering = ['-date_created']
    paginate_by = 10


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'smsApp/campaign_form.html'
    success_url = reverse_lazy('campaign')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            try:
                print("Valid form")
                print(form.instance.list_name)
                contact_list = Contact.objects.filter(list_name=form.instance.list_name)

                for contact in contact_list:
                    first_name = '{N/A}'
                    last_name = '{N/A}'
                    additional1 = '{N/A}'
                    additional2 = '{N/A}'

                    SendSMS.phone_number = [str(contact.phone_number).strip()]
                    custom_message = str(form.instance.message)

                    try:
                        if contact.first_name is not None:
                            first_name = contact.first_name
                        if contact.last_name is not None:
                            last_name = contact.last_name
                        if contact.additional1 is not None:
                            additional1 = contact.additional1
                        if contact.additional2 is not None:
                            additional2 = contact.additional2

                        for raw_message in (
                        ('{number}', contact.phone_number), ('{firstname}', first_name), ('{lastname}', last_name),
                        ('{additional1}', additional1),
                        ('{additional2}', additional2)):
                            custom_message = custom_message.replace(*raw_message)

                        if '{N/A}' not in custom_message:
                            SendSMS.message = custom_message
                            raw_response = SendSMS().send()
                        else:
                            continue
                    except Exception as e:
                        messages.error(request, f"Error: Check inputs or message count")
                try:
                    check_sent_status = raw_response['SMSMessageData']["Message"].split(" ")
                    if eval(check_sent_status[2]):
                        sent_status = 1
                    else:
                        sent_status = 0

                    sms = Campaign(title=form.instance.title, message=form.instance.message,
                                   status=sent_status, statusCode=1)
                    sms.save()
                    messages.success(request, f"Message sent to all contacts in {form.instance.list_name}")
                except Exception as e:
                    messages.error(request, f"Error: 102 {raw_response} as it causes( python {e}) ERROR")
                    return redirect('campaign-create')

                return redirect('campaign')

            except Exception as e:
                messages.error(request, f"Error: 103 python {e}) ERROR")
                return redirect('campaign-create')

        else:
            messages.error(request, f"Error:  Something is wrong with your entry")
            return redirect('campaign-create')


"""for contact in contact_list:
    SendSMS.phone_number = [str(contact.phone_number).strip()]
    try:
        for raw_message in (('{number}', contact.phone_number), ('{firstname}', contact.first_name),
                            ('{lastname}', contact.last_name),
                            ('{additional1}', contact.additional1),
                            ('{additional2}', contact.additional2)):
            custom_message = custom_message.replace(*raw_message)
    except Exception as e:
        continue
    SendSMS.message = custom_message
    raw_response = SendSMS().send()"""
