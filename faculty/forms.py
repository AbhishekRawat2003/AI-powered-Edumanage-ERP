from authentication.forms import CustomUserForm
from .models import Admin,Faculty,Subject,LeaveReportFaculty,FeedbackFaculty
from django import forms
from django.forms.widgets import DateInput

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class FacultyForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields + \
            ['course' ]

class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'faculty', 'course']

class LeaveReportFacultyForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportFacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportFaculty
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackFacultyForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackFacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackFaculty
        fields = ['feedback']

class FacultyEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields