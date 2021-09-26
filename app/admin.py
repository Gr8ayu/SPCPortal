from django.contrib import admin
from app.models import User, Department, Offer, Company, Education
from app.models import Application, Faculty, Student, SPC, Contact
from app.models import DepartmentGroupEmail

# Register your models here.

# from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_type",)}),)


admin.site.register(User, MyUserAdmin)


class DepartmentAdmin(ImportExportModelAdmin):
    class Meta:
        model = Department


@admin.register(Offer)
class OfferAdmin(ImportExportModelAdmin):

    list_display = ("company", "deadline", "offer_type",
                    "category", "required_batch")
    list_filter = ("offer_type", "required_batch",
                   "category", "eligible_gender")
    search_fields = ("company__name", "note")


@admin.register(Application)
class ApplicationAdmin(ImportExportModelAdmin):

    list_display = ("student", "offer", "status")
    list_filter = ("status",)
    search_fields = ("student__name", "student__USN", "offer__note")


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Education)
admin.site.register(SPC)
admin.site.register(DepartmentGroupEmail)
