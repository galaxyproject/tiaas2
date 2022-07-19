import calendar
import collections
import re
from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TrainingForm
from .galaxy import (
    add_group_user,
    authenticate,
    create_group,
    create_role,
    get_groups,
    get_jobs,
    get_roles,
    get_users,
    get_workflow_invocations,
)

from .models import Training


def register(request):
    if request.method != "POST":
        # if a GET (or any other method) we'll create a blank form
        form = TrainingForm(initial=request.GET.dict())
        return render(
            request, "training/register.html", {"form": form, "settings": settings}
        )

    # create a form instance and populate it with data from the request:
    form = TrainingForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        form.save()
        if settings.TIAAS_SEND_EMAIL_FROM:
            identifier = form.cleaned_data["training_identifier"]
            host = request.META.get("HTTP_HOST", "localhost")
            send_mail(
                "New TIaaS Request (%s)" % identifier,
                "We received a new tiaas request. View it in the"
                '<a href="https://%s/tiaas/admin/training/training/?processed__exact=UN">admin dashboard</a>'  # noqa: E501
                % host,
                settings.TIAAS_SEND_EMAIL_FROM,
                [settings.TIAAS_SEND_EMAIL_TO],
                fail_silently=True,  # on the fence about this one. (Same. TODO)
            )

            send_mail(
                "TIaaS Request Submitted (%s)" % identifier,
                "We received a new tiaas request and will process it as quickly as possible, considering weekends and public holidays.",
                settings.TIAAS_SEND_EMAIL_FROM,
                [form.cleaned_data['email']],
                fail_silently=True,
            )
        return HttpResponseRedirect(reverse("thanks"))
    else:
        return render(
            request, "training/register.html", {"form": form, "settings": settings}
        )

def about(request):
    return render(request, "training/about.html", {"settings": settings})


def thanks(request):
    return render(request, "training/thanks.html", {"settings": settings})


def stats_csv(request):
    data = "name,code,pop\n"

    trainings = Training.objects.all().exclude(training_identifier="test").filter(processed="AP")
    locations = collections.Counter()
    codes = {}

    for t in trainings:
        for loc in t.location:
            locations[loc.alpha3] += 1
            codes[loc.alpha3] = loc.name

    for k, v in locations.items():
        data += f"{codes[k]},{k},{v}\n"

    return HttpResponse(data, content_type="text/csv")


def numbers_csv(request):
    data = "id,start,end,location,use_gtn,attendance\n"

    trainings = Training.objects.all().exclude(training_identifier="test").filter(processed="AP")
    for t in trainings:
        countries = [x.code for x in t.location]
        data += f"{t.id},{t.start},{t.end},{'|'.join(countries)},{t.use_gtn},{t.attendance}\n"

    return HttpResponse(data, content_type="text/csv")


def trainings_for(trainings, year, month, day):
    # find trainings including this given day.
    if day == 0:
        return 0
    if year == 2020 and month == 1:
        print(day, [x for x in trainings if x.start <= date(year, month, day) <= x.end])

    return len([x for x in trainings if x.start <= date(year, month, day) <= x.end])


def calendar_view(request):
    trainings = Training.objects.all().exclude(
        training_identifier="test"
    )  # Exclude the 'test' group from showing up in calendar
    approved_trainings = [x for x in trainings if x.processed == "AP"]
    approved = len(approved_trainings)
    start = min([x.start for x in approved_trainings])
    end = max([x.end for x in approved_trainings])
    years = list(range(start.year, end.year + 1))[::-1]

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    max_value = 0

    days = {}
    for year in years:
        for idx, month in enumerate(months):
            if year not in days:
                days[year] = {}

            days_au = calendar.monthcalendar(year, idx + 1)
            days_fix = []
            for row in days_au:
                new_row = [
                    (x, trainings_for(approved_trainings, year, idx + 1, x))
                    for x in row
                ]
                m = max([x[1] for x in new_row])
                if m > max_value:
                    max_value = m
                days_fix.append(new_row)

            days[year][month] = days_fix

    return render(
        request,
        "training/calendar.html",
        {
            "trainings": approved,
            "start": start,
            "end": end,
            "years": years,
            "months": months,
            "days": days,
            "max_value": max_value,
            "settings": settings,
        },
    )


def stats(request):
    # Exclude the 'test' group from showing up in calendar
    trainings = Training.objects.all().exclude(training_identifier="test")
    approved = len([x for x in trainings if x.processed == "AP"])
    waiting = len([x for x in trainings if x.processed == "UN"])
    days = sum([(x.end - x.start).days for x in trainings])
    students = sum([x.attendance for x in trainings])

    current_trainings = len([x for x in trainings if x.start <= date.today() <= x.end])
    earliest = min([x.start for x in trainings])

    locations = collections.Counter()
    for t in trainings:
        for loc in t.location:
            locations[loc.name] += 1

    return render(
        request,
        "training/stats.html",
        {
            "trainings": trainings,
            "waiting": waiting,
            "approved": approved,
            "days": days,
            "students": students,
            "locations": dict(locations.items()),
            "current_trainings": current_trainings,
            "earliest": earliest,
            "settings": settings,
        },
    )


def join(request, training_id):
    training_id = training_id.lower()

    trainings = Training.objects.all().filter(training_identifier__iexact=training_id)
    any_approved = any([t.processed == "AP" for t in trainings])

    # If we don't know this training, reject
    if len(trainings) == 0 or not any_approved:
        return render(
            request,
            "training/error.html",
            {
                "message": "Training does not exist",
                "host": request.META.get("HTTP_HOST", None),
                "settings": settings,
            },
        )

    user = authenticate(request)
    if not user:
        return render(
            request,
            "training/error.html",
            {
                "message": "Please login to Galaxy first!",
                "host": request.META.get("HTTP_HOST", None),
                "settings": settings,
            },
        )

    training_role_name = "training-%s" % training_id
    # Otherwise, training is OK + they are a valid user.
    # We need to add them to the role

    ################
    # BEGIN UNSAFE #
    ################
    # Create role if need to.
    current_roles = list(get_roles())
    role_exists = any([training_role_name == x["name"] for x in current_roles])

    if not role_exists:
        role_id = create_role(training_role_name)
    else:
        role_id = [x for x in current_roles if training_role_name == x["name"]][0]["id"]

    # Create group if need to.
    current_groups = list(get_groups())
    group_exists = any([training_role_name == x["name"] for x in current_groups])
    if not group_exists:
        group_id = create_group(training_role_name, role_id)
    else:
        group_id = [x for x in current_groups if training_role_name == x["name"]][0][
            "id"
        ]

    ################
    #  END UNSAFE  #
    ################

    add_group_user(group_id, user)

    return render(
        request,
        "training/join.html",
        {
            "training": trainings[0],
            "host": request.META.get("HTTP_HOST", None),
            "settings": settings,
        },
    )


def _summarize(d):
    state_summary = {}
    for item in d:
        if item["state"] not in state_summary:
            state_summary[item["state"]] = 0
        if "__total__" not in state_summary:
            # div 0
            state_summary["__total__"] = 1

        state_summary[item["state"]] += 1
        state_summary["__total__"] += 1
    return state_summary


def status(request, training_id):
    training_id = training_id.lower()

    trainings = Training.objects.all().filter(training_identifier__iexact=training_id)
    any_approved = any([t.processed == "AP" for t in trainings])

    if len(trainings) == 0 or not any_approved:
        return render(
            request,
            "training/error.html",
            {
                "message": "Training does not exist",
                "host": request.META.get("HTTP_HOST", None),
                "settings": settings,
            },
        )

    refresh = request.GET.get("refresh", False) is not False
    # hours param
    hours = int(request.GET.get("hours", 3))
    if hours > 64:
        hours = 64
    elif hours < 1:
        hours = 1

    jobs = list(get_jobs(training_id, hours))
    wfs = list(get_workflow_invocations(training_id, hours))
    users = list(get_users(training_id))
    jobs_overview = {}
    for job in jobs:
        tool_id = job["tool_id"]
        if tool_id not in jobs_overview:
            jobs_overview[tool_id] = {
                "ok": 0,
                "new": 0,
                "error": 0,
                "queued": 0,
                "running": 0,
                # prevent div 0
                "__total__": 1,
            }

        if job["state"] in ("ok", "new", "error", "queued", "running"):
            jobs_overview[tool_id][job["state"]] += 1
            jobs_overview[tool_id]["__total__"] += 1

    state_summary = _summarize(jobs)
    wf_state_summary = _summarize(wfs)

    for job, data in jobs_overview.items():
        data["ok_percent"] = data["ok"] / len(jobs)
        data["new_percent"] = data["new"] / len(jobs)
        data["error_percent"] = data["error"] / len(jobs)
        data["queued_percent"] = data["queued"] / len(jobs)
        data["running_percent"] = data["running"] / len(jobs)

    return render(
        request,
        "training/status.html",
        {
            "training": trainings[0],
            "jobs": jobs,
            "wfs": wfs,
            "jobs_overview": jobs_overview,
            "users": users,
            "state": state_summary,
            "wf_state": wf_state_summary,
            "refresh": refresh,
            "settings": settings,
        },
    )
