from django.contrib.auth.models import User
from django.db import models

class CLDate(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.__class__.__name__)


class Switch(CLDate):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sorted = models.IntegerField(default=0)

    def get_code(self):
        if self.code:
            return self.code
        return self.name

    def __str__(self):
        return self.name


class BugStatus(Switch):
    color = models.CharField(max_length=16, blank=True, null=True)
    bgcolor = models.CharField(max_length=16, blank=True, null=True)


class Priority(Switch):
    color = models.CharField(max_length=16, blank=True, null=True)
    is_bold = models.BooleanField(default=False)


class Severity(Switch):
    color = models.CharField(max_length=16, blank=True, null=True)
    is_bold = models.BooleanField(default=False)


class Category(Switch):
    color = models.CharField(max_length=16, blank=True, null=True)
    parent = models.CharField(max_length=16, blank=True, null=True)

class Bug(CLDate):
    user = models.ForeignKey(User)
    executor = models.ForeignKey(User, blank=True, null=True, \
            related_name='executor')
    tester = models.ForeignKey(User, blank=True, null=True, \
            related_name='tester')
    parent = models.ForeignKey(User, blank=True, null=True, \
            related_name='parent')
    assigned_to = models.ForeignKey(User, related_name='assigned_to')
    category = models.ForeignKey(Category)
    priority = models.ForeignKey(Priority)
    severity = models.ForeignKey(Severity)
    bugstatus = models.ForeignKey(BugStatus)
    depends_on = models.CharField(max_length=256, default='', \
            blank=True, null=True)
    subject = models.CharField(max_length=256)
    text = models.TextField()

    def can_be_edited(self, user):
        return True

    def can_be_commented(self, user):
        return True


class BugEntity(CLDate):
    user = models.ForeignKey(User)
    bug = models.ForeignKey(Bug)
    safe = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    status_change = models.BooleanField(default=False)
    private = models.BooleanField(default=False)


class SavedSearch(CLDate):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    search_phrase = models.CharField(max_length=1024)
    bgcolor = models.CharField(max_length=32, blank=True, null=True)