from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *
from .sms import SendSMS
import datetime
import csv
import re
import ast


class HomeView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'smsApp/index.html'


@login_required
def home(request):
    total_count, sent_count, failed_count, total_cost = 0, 0, 0, 0
    campaigns = Campaign.objects.all()
    num = Campaign.objects.filter(date_created__date='2022-05-06').count()
    for campaign in campaigns:
        total_count += 1
        if campaign.status == 'Success':
            sent_count += 1
        else:
            failed_count += 1

    return render(request, 'smsApp/index.html', {'cost': total_cost, 'count': total_count, 'sent':sent_count,'n': num,'failed': failed_count})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        previous_days = [datetime.date.today()]
        day_count = [Campaign.objects.filter(date_created__date=datetime.date.today() - datetime.timedelta(days=14)).count()]
        failed_count = [Campaign.objects.filter(date_created__date=datetime.date.today() - datetime.timedelta(days=14),status='Failed').count()]
        for i in range(1, 14):
            previous_days.append(datetime.date.today() - datetime.timedelta(days=i))
        previous_days.sort(reverse=False)
        for i in range(1, 14):
            day_count.append(Campaign.objects.filter(date_created__date=previous_days[i]).count())
            failed_count.append(Campaign.objects.filter(date_created__date=previous_days[i], status='Failed').count())
        print(day_count)
        print(failed_count)
        labels = previous_days
        default_items = day_count
        data = {
            'labels': labels,
            "default": default_items,
            "failed": failed_count
        }
        return Response(data)


class ContactListView(LoginRequiredMixin, ListView):
    model = ContactList
    template_name = 'smsApp/contact_list_view.html'
    context_object_name = 'contactlist'


class ContactListCreateView(LoginRequiredMixin, CreateView):
    model = ContactList
    fields = '__all__'
    template_name = 'smsApp/contact_list_form.html'
    success_url = reverse_lazy('contact-list')


class ContactListDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactList
    template_name = 'smsApp/contact_list_delete.html'
    success_url = reverse_lazy('contact-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
            messages.success(request, f"{self.object.list_name} has been deleted")
        except ProtectedError as e:
            messages.error(request, f"Error: Can't delete contact list as it has some sent campaigns")
            return redirect('contact-list')

        return redirect('contact-list')


class ContactListDetailView(LoginRequiredMixin, DetailView):
    model = ContactList
    template_name = 'smsApp/contact_list_detail.html'


class ContactCreateView(LoginRequiredMixin, CreateView):
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


class ContactListUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactList
    fields = '__all__'
    template_name = 'smsApp/contact_list_edit_form.html'
    success_url = reverse_lazy('contact-list')


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'smsApp/contact_delete.html'
    success_url = reverse_lazy('contact-list')


class CampaignListView(LoginRequiredMixin, ListView):
    model = CampaignList
    template_name = 'smsApp/campaign_view.html'
    context_object_name = 'campaigns'
    ordering = ['-date_created']


def campaign_detail(request, list_name):
    campaign_list = Campaign.objects.filter(list_name=list_name)
    return render(request, 'smsApp/campaign_detail_view.html', {'list_name': list_name, 'campaign_list': campaign_list})


def campaign_search(request):
    if request.method == "POST":
        searched = request.POST['search']
        campaigns = Campaign.objects.filter(title__contains=searched)
        return render(request, 'smsApp/campaign_search.html', {'searched': searched, 'campaigns': campaigns})
    else:
        return render(request, 'smsApp/campaign_search.html', {})


def campaign_create_csv_all(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    campaigns = Campaign.objects.all()
    failed_count = 0
    success_count = 0
    sent_count = 0

    writer.writerow(['Title', 'Phone Number', 'Message', 'Contact List', 'Cost', 'Status'])

    for campaign in campaigns:
        writer.writerow([campaign.title, campaign.phone_number, campaign.message, campaign.list_name, campaign.cost,
                         campaign.status])

        if campaign.status == 'Failed':
            failed_count += 1
        elif campaign.status == 'Success':
            success_count += 1
        elif campaign.status == 'Sent':
            sent_count += 1

    writer.writerow([f'Failed: {failed_count}', f'Delivered: {success_count}', f'Sent: {sent_count}'])
    response['Content-Disposition'] = f'attachment; filename={datetime.date.today()} bulkSMS report.csv'

    return response


def campaign_create_csv(request, list_name):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    campaigns = Campaign.objects.filter(list_name=list_name)
    failed_count = 0
    success_count = 0
    sent_count = 0

    writer.writerow(['Title', 'Phone Number', 'Message', 'Contact List', 'Cost', 'Status'])

    for campaign in campaigns:
        writer.writerow([campaign.title, campaign.phone_number, campaign.message, campaign.list_name, campaign.cost,
                         campaign.status])

        if campaign.status == 'Failed':
            failed_count += 1
        elif campaign.status == 'Success':
            success_count += 1
        elif campaign.status == 'Sent':
            sent_count += 1

    writer.writerow([f'Failed: {failed_count}', f'Delivered: {success_count}', f'Sent: {sent_count}'])
    response['Content-Disposition'] = f'attachment; filename={datetime.date.today()} bulkSMS report for' \
                                      f' {campaign.list_name} contact list.csv'
    return response


class SingleCampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    template_name = "smsApp/campaign_single_detail_view.html"
    context_object_name = 'campaign'


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = ContactList
    template_name = 'smsApp/campaign_detail_view.html'
    ordering = ['-date_created']


def create_campaign_list(form):
    CampaignList.objects.create(title=form.instance.title, message=form.instance.message,
                                list_name=form.instance.list_name)


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'smsApp/campaign_form.html'
    success_url = reverse_lazy('campaign')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                contact_list = Contact.objects.filter(list_name=form.instance.list_name)
                create_campaign_list(form)
                success_count = 0
                failed_count = 0
                for contact in contact_list:
                    first_name = '{N/A}'
                    last_name = '{N/A}'
                    additional1 = '{N/A}'
                    additional2 = '{N/A}'

                    SendSMS.phone_number = [str(contact.phone_number).strip()]
                    custom_message = str(form.instance.message)

                    try:
                        if contact.first_name:
                            first_name = contact.first_name
                        if contact.last_name:
                            last_name = contact.last_name
                        if contact.additional1:
                            additional1 = contact.additional1
                        if contact.additional2:
                            additional2 = contact.additional2

                        for raw_message in (
                                ('{number}', contact.phone_number), ('{firstname}', first_name),
                                ('{lastname}', last_name),
                                ('{additional1}', additional1),
                                ('{additional2}', additional2)):
                            custom_message = custom_message.replace(*raw_message)

                        if '{N/A}' not in custom_message:
                            SendSMS.message = custom_message
                            raw_response = SendSMS().send()
                            try:
                                raw_response_dict = re.findall("\[([^\[\]]*)\]", str(raw_response))
                                message = ast.literal_eval(raw_response_dict[0])
                                sms = Campaign(title=form.instance.title, phone_number=contact.phone_number,
                                               message=custom_message,
                                               list_name=form.instance.list_name, cost=message['cost'],
                                               status=message['status'], statusCode=message['statusCode'])
                                sms.save()
                                print(message['cost'])
                                success_count += 1
                            except Exception as e:
                                failed_count += 1
                                sms = Campaign(title=form.instance.title, phone_number=contact.phone_number,
                                               message=custom_message,
                                               list_name=form.instance.list_name, cost= "MWK 0.0000",
                                               status='Failed', statusCode=0)
                                sms.save()
                                continue
                        else:
                            continue
                    except Exception as e:
                        failed_count += 1
                        sms = Campaign(title=form.instance.title, phone_number=contact.phone_number,
                                       message=custom_message,
                                       list_name=form.instance.list_name, cost="MWK 0.0000",
                                       status='Failed', statusCode=0)
                        sms.save()

                if failed_count:
                    messages.success(request, f"Message delivered to {success_count} contacts and undelivered to {failed_count} contacts in {form.instance.list_name} ")
                else:
                    messages.success(request, f"Message delivered to {success_count} contacts in {form.instance.list_name}")
                return redirect('campaign')

            except Exception as e:
                messages.error(request, f"Error: 103 python {e}) ERROR")
                return redirect('campaign-create')

        else:
            messages.error(request, f"Error:  Something is wrong with your entry")
            return redirect('campaign-create')


"""class SingleCampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = SingleCampaignForm
    template_name = 'smsApp/campaign_form.html'
    success_url = reverse_lazy('campaign')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                contact_list = Contact.objects.filter(phone_number__exact=form.instance.phone_number)
                create_campaign_list(form)
                for contact in contact_list:
                    first_name = '{N/A}'
                    last_name = '{N/A}'
                    additional1 = '{N/A}'
                    additional2 = '{N/A}'

                    SendSMS.phone_number = [str(contact.phone_number).strip()]
                    custom_message = str(form.instance.message)

                    try:
                        if contact.first_name:
                            first_name = contact.first_name
                        if contact.last_name:
                            last_name = contact.last_name
                        if contact.additional1:
                            additional1 = contact.additional1
                        if contact.additional2:
                            additional2 = contact.additional2

                        for raw_message in (
                                ('{number}', contact.phone_number), ('{firstname}', first_name),
                                ('{lastname}', last_name),
                                ('{additional1}', additional1),
                                ('{additional2}', additional2)):
                            custom_message = custom_message.replace(*raw_message)

                        if '{N/A}' not in custom_message:
                            SendSMS.message = custom_message
                            raw_response = SendSMS().send()
                            print(raw_response)
                            try:
                                raw_response_dict = re.findall("\[([^\[\]]*)\]", str(raw_response))
                                message = ast.literal_eval(raw_response_dict[0])
                                sms = Campaign(title=form.instance.title, phone_number=contact.phone_number,
                                               message=custom_message,
                                               list_name=form.instance.list_name, cost=message['cost'],
                                               status=message['status'], statusCode=message['statusCode'])
                                sms.save()
                                print(message['cost'])
                                messages.success(request, f"Message sent to all contacts in {form.instance.list_name}")
                            except Exception as e:
                                messages.error(request, f"Error: 102 {raw_response} as it causes( python {e}) ERROR")
                                return redirect('campaign-create')
                        else:
                            messages.error(request, f"Error: Check inputs")
                    except Exception as e:
                        messages.error(request, f"Error: Check inputs or message count")

                return redirect('campaign')

            except Exception as e:
                messages.error(request, f"Error: 103 python {e}) ERROR")
                return redirect('campaign-create')

        else:
            messages.error(request, f"Error:  Something is wrong with your entry")
            return redirect('campaign-create')"""


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
