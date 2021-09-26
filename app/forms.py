from django.forms import ModelForm


from app.models import Contact, Education, Student


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ["user"]


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = "__all__"
        exclude = ["user"]


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ["user", "is_eligible"]
