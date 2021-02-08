# Create your views here.

# GENERIC VIEWS
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/
# https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/


# FORM FROM MODEL
# https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
# https://tutorial.djangogirls.org/en/django_forms/

# CUSTOM USER MODEL
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model


# Signals
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html

from django.shortcuts import redirect
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, EducationForm, StudentForm
# from .models import Contact, Education, Student, Offer, Company, Application
from .models import *
from django.contrib import messages

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max, Min, Sum
from app.analytics import *
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from django.core import mail
from django.utils.html import strip_tags
from django.utils.timezone import utc
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse

def home(request):

    return render(request, 'app/home.html')
    # return render(request, 'app/offer_email_template.html')

@login_required
def dashboard(request):


    user = request.user
    student = request.user.student
    contact = student.contact
    education = student.education

    context = {}
    context['user'] = user
    context['student'] = student
    context['contact'] = contact
    context['education'] = education

    context['analytics'] = {}


    context['analytics']['chart1'] = pie_branch_offer()
    context['analytics']['chart2'] = pie_dream_open_offer()
    context['analytics']['chart3'] = department_wise_yearly_stats(2)
    context['analytics']['chart4'] = pie_dream_open_offer()
    context['analytics']['chart5'] = pie_dream_open_offer()
    

    return render(request, 'app/dashboard.html', context=context)






@login_required 
def edit_profile(request):

    user = request.user.student

    c = user.contact
    e = user.education


    studentForm = StudentForm(instance=user)
    contactForm = ContactForm(instance=c)
    educationForm = EducationForm(instance=e)
    return render(request, 'app/view_profile.html', {'contact_form':contactForm, 'edu_form':educationForm , 'student_form':studentForm })

@login_required 
def edit_contact_details(request):

    if request.method == 'POST':
        
        student = request.user.student
        contact = student.contact

        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            msg = "Message"
            error = "Successfully saved"
            messages.success(request, 'Contact details Updated.')
        else:
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
        # form.user = request.user.student 
        
        return redirect('dashboard')
    else:
        return HttpResponse(status=405)

@login_required 
def edit_education_details(request):

    if request.method == 'POST':
        
        student = request.user.student
        education = student.education

        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            msg = "Message"
            error = "Successfully saved"
            messages.success(request, 'Education details Updated.')
            
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
        return redirect('dashboard')
    else:
        return HttpResponse(status=405)

@login_required 
def edit_profile_details(request):

    if request.method == 'POST':
        
        student = request.user.student
        # education = student.education
        print(request.FILES)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            msg = "Message"
            error = "Successfully saved"
            messages.success(request, 'Profile Updated.')
            
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
        return redirect('dashboard')

    else :
        return HttpResponse(status=405)

def CheckElegibleForApplication(student, offer):

    errors = []

    is_elegible = student.is_eligible



    if not is_elegible:
        errors.append("Student is not elegible or already placed in open Dream Company")

    if Application.objects.filter(student=student, offer=offer).count() >0:
        is_elegible = False
        errors.append("Already Applied")


    if datetime.datetime.now().astimezone(timezone.utc) > offer.deadline:
        is_elegible = False
        errors.append("deadline already passed")

    if student.education.graduation_year != offer.required_batch:
        is_elegible = False
        errors.append("required batch is "+ str(offer.required_batch))

    if student.education.department not in offer.eligible_branches.all():
        is_elegible = False
        errors.append("Your branch is not elegible.")

    if student.education.cgpa < offer.cgpa_cutoff :
        is_elegible = False
        errors.append("CGPA Cutoff requirement not met.")

    if student.education.X_percentage < offer.X_cutoff :
        is_elegible = False
        errors.append("X percentage Cutoff requirement not met.")

    if student.education.X_percentage < offer.XII_cutoff :
        is_elegible = False
        errors.append("XII / Diploma percentage Cutoff requirement not met.")


    if student.gender not in offer.eligible_gender and "OTHER" not in offer.eligible_gender:
        is_elegible = False
        errors.append("your Gender is not elegible")

    if offer.bio_keyword not in student.education.bio:
        is_elegible = False
        errors.append("You don't have match profile for "+offer.bio_keyword)

    return is_elegible, errors
    


class OfferListView(ListView):

    model = Offer
    paginate_by = 10  # if pagination is desired


    def get_queryset(self):
        qs = super(OfferListView, self).get_queryset()
        # name = self.kwargs.get('name', '')
        filters = self.request.GET
        print(filters)
        # print(filters)
        if 'name' in filters.keys():
            # print(True)
            # print(filters['name'])
            qs1 =  qs.filter(company__name__icontains=filters['name'] )
            qs2 = qs.filter(note__icontains=filters['name'])
            qs = qs1 | qs2
        
        if "eligible_only" in filters.keys():
            print("eligible_only")
            ids = []
            for q in qs:
                is_elegible, errors = CheckElegibleForApplication(self.request.user.student,q )
                if is_elegible:
                    ids.append(q.id)
            print(len(qs))
            qs = qs.filter(pk__in=ids) 
            print(len(qs))


        if 'dream_only' in filters.keys():
            qs =qs.filter(offer_type='DREAM')

        if 'open_dream_only' in filters.keys():
            qs =qs.filter(offer_type='OPEN')



        return qs.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OfferDetailView(DetailView):

    model = Offer


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        student = self.request.user.student
        offer = self.object
        
        is_elegible, errors = CheckElegibleForApplication(student, offer)

        context['now'] = datetime.datetime.utcnow().replace(tzinfo=utc)
        # TODO make local time
        context['elegible'] = is_elegible

        if is_elegible:
            messages.success(self.request, 'Eligible for Application.')
        else:
            messages.warning(self.request, 'Not eligible.')



        context['elegiblity_reasons'] = errors

        return context

@login_required
def sendOfferAlert(request, pk):
    if request.user.is_admin_access() :

        domain = get_object_or_404(Site, pk=settings.SITE_ID).domain
        domain = "https://" + domain
        if request.method == 'POST':
            offer = get_object_or_404(Offer, pk=pk)
            
            subject = "RVCE Placements : "+ str(offer.company.name)
            to = request.POST.getlist('email_list')
            to = list(to)

            

            from_email = os.getenv('DEFAULT_FROM_EMAIL')
            html_message = render_to_string('app/offer_email_template.html', { 'offer':offer,'domain_name':domain})
            plain_message = strip_tags(html_message)
            
            status = mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)

            if status == 1:
                messages.success(request, 'Mail sent.')

            return redirect('dashboard')
            
        else:
            offer = get_object_or_404(Offer, pk=pk)
            email_list = DepartmentGroupEmail.objects.all().values('email')
            email_list = list(map(lambda x:x['email'], email_list ))


            branches = offer.eligible_branches.all().values('id')
            ids = list(map(lambda x:x['id'], branches ))

            batch = offer.required_batch
            e = DepartmentGroupEmail.objects.filter(graduation_year=batch).filter(id__in=ids).values('email')
            
            email_on = list(map(lambda x:x['email'], e ))


            return render(request,'app/email_sender.html', {
                                                        'offer':offer, 
                                                        'email_list':email_list,
                                                        'email_on':email_on,
                                                        'domain_name':domain
                                                        })
        

    else:
        return redirect('dashboard')


class CompanyListView(ListView):

    model = Company
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CompanyDetailView(DetailView):

    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicationListView(ListView):

    model = Application
    # paginate_by = 5  # if pagination is desired

    def get_queryset(self):
        qs = super(ApplicationListView, self).get_queryset()
        return qs.filter(student=self.request.user.student).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# class CompanyDetailView(DetailView):

#     model = Company

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

@login_required
def AddApplication(request, id):
    student = request.user.student
    offer = get_object_or_404(Offer, pk=id)
    is_elegible, errors = CheckElegibleForApplication(student, offer)    

    if is_elegible:
        Application.objects.create(student = student,offer = offer)
        messages.info(request, 'Application Sent.')

        return redirect('my_applications')
    else:
        messages.warning(request, 'Not Eligible.')

        return redirect('offer_details', pk=id)



#TODO Add gender in elegibility criteria