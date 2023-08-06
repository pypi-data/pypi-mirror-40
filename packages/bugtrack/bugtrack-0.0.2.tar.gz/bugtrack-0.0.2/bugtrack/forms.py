from generalobj.forms import GeneralObjForm

from .models import Bug


class BugForm(GeneralObjForm):
    class Meta:
        model = Bug
        fields = ('category', 'priority', 'severity', 'assigned_to', \
                'subject', 'text', 'executor', 'tester', 'parent', 'depends_on')