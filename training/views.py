import collections
from datetime import date
from django_countries import countries

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


def test(request):
    """Show the specified html page."""
    return render(request, f'training/{request.GET.get("filename")}')


def register(request):
    host = request.META.get("HTTP_HOST", "localhost")
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()

            # TODO: refactor this into forms:
            identifier = form.cleaned_data['training_identifier']
            if settings.TIAAS_SEND_EMAIL_TO:
                send_mail(
                    f"New TIaaS Request ({identifier})",
                    (
                        'A new TIaaS request has been received. View it in the'
                        ' <a href="'
                        f'https://{host}/tiaas/admin/training/training/'
                        '?processed__exact=UN'
                        '">admin dashboard</a>'
                    ),
                    settings.TIAAS_SEND_EMAIL_FROM,
                    [settings.TIAAS_SEND_EMAIL_TO],
                    fail_silently=True,  # TODO should handle and log appropriately
                )
            if settings.TIAAS_SEND_EMAIL_TO_REQUESTER:
                send_mail(
                    f"TIaaS Request confirmation: ({identifier})",
                    (
                        f'Dear {form.cleaned_data["name"]},\n\n'
                        'Thanks for requesting a new TIaaS allocation.\n'
                        'We will contact you to let you know when your request'
                        ' has been reviewed.\n\n'
                        f'Regards,\nThe {settings.TIAAS_OWNER} team'
                    ),
                    settings.TIAAS_SEND_EMAIL_FROM,
                    [form.cleaned_data['email']],
                    fail_silently=True,  # TODO should handle and log appropriately
                )

            return HttpResponseRedirect(reverse("thanks"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm(initial=request.GET.dict())

    return render(request, "training/register.html", {"form": form})


def about(request):
    return render(request, "training/about.html")


def thanks(request):
    return render(request, "training/thanks.html")


def dashboard_example(request):
    """Show the example training dashboard page."""
    return render(request, 'training/dashboard-example.html')


def stats_csv(request):
    data = "name,code,pop\n"
    trainings = (
        Training.objects.exclude(training_identifier="test")
        .filter(processed="AP")
    )
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

    trainings = (
        Training.objects.exclude(training_identifier="test")
        .filter(processed="AP")
    )
    for t in trainings:
        countries = [x.code for x in t.location]
        data += ','.join([
            t.id,
            t.start,
            t.end,
            '|'.join(countries),
            t.use_gtn,
            t.attendance,
        ]) + '\n'

    return HttpResponse(data, content_type="text/csv")


def trainings_for(trainings, year, month, day):
    # find trainings including this given day.
    if day == 0:
        return 0
    if year == 2020 and month == 1:
        print(
            day,
            [
                x for x in trainings
                if x.start <= date(year, month, day) <= x.end
            ]
        )

    return len([
        x for x in trainings
        if x.start <= date(year, month, day) <= x.end
    ])


def calendar_view(request):
    """Display scheduled events in an interactive calendar view."""
    approved_trainings = (
        Training.objects.all()
        .exclude(training_identifier="test")
        .filter(processed="AP")
        .order_by('start')
    )
    return render(
        request,
        "training/calendar.html",
        {
            "events": approved_trainings,
            "admin_user": request.user.is_staff,
            "n_events": approved_trainings.count()
        },
    )


def stats(request):
    trainings = Training.objects.exclude(
        training_identifier="test"
    )  # Exclude the 'test' group from showing up in calendar

    approved = trainings.filter(processed="AP")
    # approved = len([x for x in trainings if x.processed == "AP"])

    waiting = trainings.filter(processed="UN")
    # waiting = len([x for x in trainings if x.processed == "UN"])

    if approved:
        days = sum(
            (end - start).days
            for end, start in
            approved.values_list('end', 'start')
        )
        # days = sum([(x.end - x.start).days for x in trainings])

        students = sum(approved.values_list('attendance', flat=True))
        # students = sum([x.attendance for x in trainings])

        today = date.today()
        current = approved.filter(start__lte=today, end__gte=today)
        # current_trainings = len([
        #     x for x in trainings
        #     if x.start <= date.today() <= x.end
        # ])

        earliest = min(approved.values_list('start', flat=True))
        # earliest = min([x.start for x in trainings])

        countries_lookup = dict(countries)
        locations = collections.Counter()
        for locs in approved.values_list('location', flat=True):
            for loc in locs.split(','):
                locations[countries_lookup[loc]] += 1

        data = {
            "trainings": trainings,
            "waiting": waiting.count(),
            "approved": approved.count(),
            "days": days,
            "students": students,
            "locations": dict(locations.items()),
            "current_trainings": current.count(),
            "earliest": earliest,
        }
    else:
        data = {
            "trainings": trainings,
            "waiting": waiting.count(),
            "approved": 0,
            "days": 0,
            "students": 0,
            "locations": {},
            "current_trainings": 0,
            "earliest": None,
        }

    return render(request, "training/stats.html", data)


def join(request, training_id):
    training_id = training_id.lower()
    trainings = Training.objects.filter(
        training_identifier__iexact=training_id,
        processed='AP',
    )

    # If we don't know this training, reject
    if not trainings.count():
        return render(
            request,
            "training/error.html",
            {
                "message": "Training event does not exist",
            },
        )

    event = trainings.first()

    # If the event has already finished, reject request
    if event.end < date.today():
        return render(
            request,
            "training/error.html",
            {
                "message": (
                    "Sorry, this event finished on"
                    f" {event.end.strftime('%Y-%m-%d')}."
                    " If you think this is a mistake, please contact Galaxy"
                    " support."
                ),
                "host": request.META.get("HTTP_HOST", None),
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
        role_id = [
            x for x in current_roles
            if training_role_name == x["name"]
        ][0]["id"]

    # Create group if need to
    current_groups = list(get_groups())
    group_exists = any([
        training_role_name == x["name"]
        for x in current_groups
    ])
    if not group_exists:
        group_id = create_group(training_role_name, role_id)
    else:
        group_id = [
            x for x in current_groups
            if training_role_name == x["name"]
        ][0]["id"]

    ################
    #  END UNSAFE  #
    ################

    add_group_user(group_id, user)

    return render(
        request,
        "training/join.html",
        {
            "training": event,
            "host": request.META.get("HTTP_HOST", None),
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

    trainings = Training.objects.all().filter(
        training_identifier__iexact=training_id)
    any_approved = any([t.processed == "AP" for t in trainings])

    if len(trainings) == 0 or not any_approved:
        return render(
            request,
            "training/error.html",
            {
                "message": "Training does not exist",
                "host": request.META.get("HTTP_HOST", None),
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
        },
    )
