from django.db import models
from django.urls import reverse


class ContactList(models.Model):
    list_name = models.CharField(max_length=100)
    list_description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.list_name


class Contact(models.Model):
    phone_number = models.CharField(max_length=13, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    additional1 = models.CharField(max_length=30, blank=True, null=True)
    additional2 = models.CharField(max_length=30, blank=True, null=True)
    list_name = models.ForeignKey(ContactList, default=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.list_name} {self.phone_number}'


class Campaign(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField()
    list_name = models.ForeignKey(ContactList, default=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    statusCode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
