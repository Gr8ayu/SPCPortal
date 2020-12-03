from app.models import *
from django.db.models import Avg, Max, Min, Sum
import random
from django.db.models.functions import Coalesce
import math


def color(*args):
    return ("#%06x" % random.randint(0, 0xFFFFFF))


def pie_dream_open_offer(*args):
    a = Offer.objects.all().values('offer_type').annotate(package = Coalesce(Sum('package'), 0))
    a = list(a)
    dataset = {}

    dataset['labels'] = list(map(lambda x : x['offer_type'], a))
    dataset['data'] = list(map(lambda x : x['package'], a))
    dataset['backgroundColor'] = list(map(color, a))
    chart = {}
    chart['dataset'] = dataset
    chart['options'] = {
                      'title': {
                        'display': 'true',
                        'text': 'Total CTC breakup (in LPA) '
                      }
                    }

    return chart


def pie_branch_offer(*args):
    a = Offer.objects.all().values('eligible_branches').annotate(package = Coalesce(Sum('package'), 0))
    a = list(a)
    dataset = {}

    ids = list(map(lambda x : x['eligible_branches'], a))
    labels = list(Department.objects.filter(id__in=ids).order_by('id').values('name'))
    
    chart = {}


    dataset['labels'] = list(map(lambda x:x['name'], labels))
    dataset['data'] = list(map(lambda x : x['package'], a))
    dataset['backgroundColor'] = list(map(color, a))
    dataset['borderWidth'] = 2
    dataset['hoverBorderWidth'] = 5
    dataset['weight'] = 4
    dataset['borderAlign'] = 'inner'


    options = {}
    options['title'] = {
                        'display': 'true',
                        'text': 'Department wise volume of CTC (in LPA) '
                      }

    # options['cutoutPercentage'] = 50
    # options['rotation'] = -5 * math.pi
    # options['circumference'] = 5 * math.pi
    options['animation'] = {} 
    options['animation']['animateRotate'] = 'true'  
    options['animation']['animateScale'] = 'true'  



    chart['options'] = options
    chart['dataset'] = dataset
    return chart


def offers_by_companies_count(*args):
    
    # Department wise offers made 
    # Application.objects.filter(status="ACCEPTED").values('student__education__department').annotate(count = Count('id'))
    # Application.objects.filter(status="ACCEPTED").values('student__education__department__name').annotate(count = Count('id'))
    # Application.objects.filter(status="ACCEPTED", offer__date__year=2019).values('student__education__department__name').annotate(count = Count('id'))


    # company wise offers made
    # Application.objects.filter(status="ACCEPTED").values('offer__company').annotate(count = Count('id'))
    # Application.objects.filter(status="ACCEPTED").values('offer__company__name').annotate(count = Count('id'))


    # No of offers made/Visited by company yearwise
    # Offer.objects.all().values('date__year',).annotate(count=Count('date__year')) 
    # Application.objects.filter(status="ACCEPTED").values('offer__date__year',).annotate(count=Count('id'))


    # Max, Avg, Min offers made each year
    # Offer.objects.filter(applications__status="ACCEPTED").values('date__year', 'company__name').annotate(count=Avg('package'))



    pass


def emails():
    Offer.objects.all()[6].eligible_branches.all().values('id')
    Offer.objects.all()[6].required_batch
    list(map(lambda x:x['id'], branches ))
    DepartmentGroupEmail.objects.filter(graduation_year=2022).filter(id__in=blist).values('email')
    
    list(map(lambda x:x['email'], e ))
