from django.contrib import admin
from app.models import *
# Register your models here.

from import_export import resources

from import_export.admin import ImportExportModelAdmin


class DepartmentAdmin(ImportExportModelAdmin):
    class Meta:
       model = Department


@admin.register(Offer)
class OfferAdmin(ImportExportModelAdmin):

    list_display = ('company', 'deadline', 'offer_type','required_batch')
    list_filter = ('offer_type','required_batch','company')
    search_fields = ('company__name', 'note')
    
@admin.register(Application)
class ApplicationAdmin(ImportExportModelAdmin):

    list_display = ('student','offer' ,'status')
    list_filter = ('status',)
    search_fields = ('student__name','student__USN', 'offer__note')
    



admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Education)
# admin.site.register(Offer)
admin.site.register(SPC)
# admin.site.register(Application)


# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_subscribed', 'valid_till')
#     # list_filter = ('is_subscribed',)
#     search_fields = ('user',)
#     actions = ['subscribe_30_days']

#     def subscribe_30_days(self, request, queryset):
#         dt = datetime.date.today() + datetime.timedelta(days=30)
#         queryset.update(valid_till=dt)

