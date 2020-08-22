from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Student, Offer, Application
from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.

def index(request):
    toast = []
    return render(request, 'base.html', context = { 'toast' :toast  } )




class StudentListView(ListView):

    model = Student
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        print(context['now'])
        return context

    def get_queryset(self):
        return Student.objects.filter(is_placed = False)




class StudentDetailView(DetailView):

    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        applications = Application.objects.filter(student = self.object)
        context['applications'] = applications
        # print(context['now'])
        return context

    def get_queryset(self):
        return Student.objects.filter(is_placed = False)

class OfferListView(ListView):

    model = Offer
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ApplicationListView(ListView):

    model = Application
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context




def addOffer(request):    

    #TODO Update this department list
    if request.method == 'GET':
        departments = {}
        departments['ISE'] = "ISE"
        departments['CSE'] = "CSE"
        departments['ECE'] = "ECE"
        departments['EIE'] = "EIE"
        departments['MECH'] = "MECH"
        departments['CIVIL'] = "CIVIL"
        
        students = {}
        for key in departments.keys():
            try:
                stud = Student.objects.filter(department = key)
                students[key] = stud
            except expression as identifier:
                pass

        return render(request, 'portal/new_offer.html', context = { 'departments' : departments, 'students' : students  } )


    # POST data
    else :
        # print(request.__dict__)
    
        data = request.POST
        toast = []
        data = dict(data)
        print(data)
        # print(data.get('department'))
        try:
            company = data['company_name'][0]
            position = data['position'][0]
            link = data['link'][0]
        except Exception as e:
            toast.append( "Form data : "+ str(e))
            company = ''
            position = ''
            link = ''

        try:
            if 'department' in data.keys():
                departments = data['department']
            else :
                departments = []

            if 'open_dream' in data.keys():
                open_dream = True
            else:
                open_dream = False
            
            if 'student' in data.keys():
                students = data['student']
            else:
                students = []

            print(departments, students)
        except Exception as e:
            toast.append("Form info : "+str(e))


        # Creating new offer
        try:
            newOffer = Offer(company_name = company, position= position,link=link, departments= departments , open_dream = open_dream)
            newOffer.save()
        except Exception as e:
            toast.append("creating offer : "+str(e))
            return render(request, 'base.html', context = { 'toast' :toast  } ) 
        
        # Adding student's application to offer
        try:
            applications = []
            for s in students:
                stud = Student.objects.get(id=int(s))
                app = Application(student= stud, offer=newOffer)
                app.save()
                applications.append(app)
            



        except Exception as e:
            toast.append("storing applications : "+str(e))
            

        return render(request, 'base.html', context = { 'toast' :toast  } )

def EditOfferStudents(request, pk):
    toast = []
    #TODO Update this department list
    if request.method == 'GET':
        departments = {}
        departments['ISE'] = "ISE"
        departments['CSE'] = "CSE"
        departments['ECE'] = "ECE"
        departments['EIE'] = "EIE"
        departments['MECH'] = "MECH"
        departments['CIVIL'] = "CIVIL"

        students = {}
        for key in departments.keys():
            try:
                stud = Student.objects.filter(department = key)
                students[key] = stud
            except Exception as e:
                toast.append(e)

        offer = get_object_or_404(Offer,pk=pk)
        applied_students = list( app.student for app in offer.applications.all()  ) 
        

        return render(request, 'portal/edit_offer_students.html', context = { 'toast' :toast, 
            'students':students,
            'offer': offer,
            'applied_students': applied_students
        } )

    else:
        data = request.POST
        toast = []
        data = dict(data)
        print(data)
        
        try:

            offer = Offer.objects.get(pk=int(data['offer'][0]))
            students = data['student']
            applied_students = list( app.student for app in offer.applications.all()  ) 

            for s in students:
                stud = Student.objects.get(pk=int(s))
                if stud in applied_students:
                    pass
                else:
                    app =Application(offer=offer, student=stud)
                    app.save()
            toast.append("added students to "+ str(offer))
        except Exception as e:
            toast.append(str(e))
            







        return render(request, 'base.html', context = { 'toast' :toast  } )



    
