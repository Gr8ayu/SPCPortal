from app.models import Offer, Department, Application
from django.db.models import Avg, Max, Min, Sum
import random
from django.db.models.functions import Coalesce
# import math


def color(*args):
    return "#%06x" % random.randint(0, 0xFFFFFF)


def pie_dream_open_offer(*args):
    a = (
        Offer.objects.all()
        .values("offer_type")
        .annotate(package=Coalesce(Sum("package"), 0))
    )
    a = list(a)
    dataset = {}

    dataset["labels"] = list(map(lambda x: x["offer_type"], a))
    dataset["data"] = list(map(lambda x: x["package"], a))
    dataset["backgroundColor"] = list(map(color, a))
    chart = {}

    options = {"title": {"display": "true",
                         "text": "Total CTC breakup (in LPA) "}}

    chart = {
        "type": "pie",
        "data": {"datasets": [dataset], "labels": dataset["labels"]},
        "options": options,
    }

    return chart


def pie_branch_offer(*args):
    a = (
        Offer.objects.all()
        .values("eligible_branches")
        .annotate(package=Coalesce(Sum("package"), 0))
    )
    a = list(a)
    dataset = {}

    ids = list(map(lambda x: x["eligible_branches"], a))
    labels = list(Department.objects.filter(
        id__in=ids).order_by("id").values("name"))

    chart = {}

    dataset["labels"] = list(map(lambda x: x["name"], labels))
    dataset["data"] = list(map(lambda x: x["package"], a))
    dataset["backgroundColor"] = list(map(color, a))
    dataset["borderWidth"] = 2
    dataset["hoverBorderWidth"] = 5
    dataset["weight"] = 4
    dataset["borderAlign"] = "inner"

    options = {}
    options["title"] = {
        "display": "true",
        "text": "Department wise volume of CTC (in LPA) ",
    }

    # options['cutoutPercentage'] = 50
    # options['rotation'] = -5 * math.pi
    # options['circumference'] = 5 * math.pi
    options["animation"] = {}
    options["animation"]["animateRotate"] = "true"
    options["animation"]["animateScale"] = "true"

    # chart['options'] = options
    # chart['dataset'] = dataset

    chart = {
        "type": "pie",
        "data": {"datasets": [dataset], "labels": dataset["labels"]},
        "options": options,
    }
    return chart


def department_wise_yearly_stats(dept):

    datasets = []

    data = (
        Application.objects.filter(student__education__department__id=dept)
        .filter(status="ACCEPTED")
        .values_list("offer__required_batch")
        .annotate(sum=Coalesce(Max("offer__package"), 0))
    )
    data = list(data)
    years = list(map(lambda x: x[0], data))
    value = list(map(lambda x: x[1], data))

    data_pt = {
        "data": value,
        "label": "Maximum",
        "borderColor": color(),
        "fill": "false",
    }

    datasets.append(data_pt)

    data = (
        Application.objects.filter(student__education__department__id=dept)
        .filter(status="ACCEPTED")
        .values_list("offer__required_batch")
        .annotate(sum=Coalesce(Avg("offer__package"), 0))
    )
    data = list(data)
    value = list(map(lambda x: x[1], data))

    data_pt = {
        "data": value,
        "label": "Average",
        "borderColor": color(),
        "fill": "false",
    }

    datasets.append(data_pt)

    data = (
        Application.objects.filter(student__education__department__id=dept)
        .filter(status="ACCEPTED")
        .values_list("offer__required_batch")
        .annotate(sum=Coalesce(Min("offer__package"), 0))
    )
    data = list(data)

    value = list(map(lambda x: x[1], data))

    data_pt = {
        "data": value,
        "label": "Minimum",
        "borderColor": color(),
        "fill": "false",
    }

    datasets.append(data_pt)

    options = {}
    options["title"] = {"display": "true",
                        "text": "Yearly performance Statistics "}

    # options['cutoutPercentage'] = 50
    # options['rotation'] = -5 * math.pi
    # options['circumference'] = 5 * math.pi
    options["animation"] = {}
    options["animation"]["animateRotate"] = "true"
    options["animation"]["animateScale"] = "true"

    # chart['options'] = options
    # chart['dataset'] = dataset

    chart = {
        "type": "line",
        "data": {"datasets": datasets, "labels": years},
        "options": options,
    }
    return chart
