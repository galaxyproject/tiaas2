from django.shortcuts import render
import re
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Training
from django.urls import reverse
from .galaxy import (
    get_roles,
    create_role,
    get_groups,
    create_group,
    add_group_user,
    get_jobs,
    get_users,
    authenticate,
)
from .forms import TrainingForm


def register(request):
    host = request.META.get("HTTP_HOST", "localhost")
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            safe_id = form.cleaned_data["training_identifier"].lower()
            safe_id = re.sub(r"[^a-z0-9_-]*", "", safe_id)

            form.cleaned_data["training_identifier"] = safe_id
            form.save()

            if settings.TIAAS_SEND_EMAIL_TO:
                send_mail(
                    "New TIaaS Request (%s)" % safe_id,
                    'We received a new tiaas request. View it in the <a href="https://%s/tiaas/admin/training/training/?processed__exact=UN">admin dashboard</a>'
                    % host,
                    settings.TIAAS_SEND_EMAIL_FROM,
                    [settings.TIAAS_SEND_EMAIL_TO],
                    fail_silently=True,  # on the fence about this one.
                )
            return HttpResponseRedirect(reverse("thanks"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(
        request, "training/register.html", {"form": form, "settings": settings}
    )


def thanks(request):
    return render(request, "training/thanks.html")


def stats(request):
    trainings = Training.objects.all()
    return render(request, "training/stats.html", {"trainings": trainings})


def join(request, training_id):
    try:
        training = Training.objects.get(training_identifier=training_id.lower())
    except Training.DoesNotExist:
        return render(
            request,
            "training/error.html",
            {
                "message": "Training does not exist",
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

    # If we don't know this training, reject
    if training.processed != "AP":
        return render(
            request,
            "training/error.html",
            {
                "message": "Training is not active",
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
        {"training": training, "host": request.META.get("HTTP_HOST", None)},
    )


def status(request, training_id):
    try:
        training = Training.objects.get(training_identifier=training_id)
    except Training.DoesNotExist:
        return render(
            request,
            "training/error.html",
            {
                "message": "Training does not exist",
                "host": request.META.get("HTTP_HOST", None),
            },
        )

    # hours param
    hours = int(request.GET.get("hours", 3))
    if hours > 64:
        hours = 64
    elif hours < 1:
        hours = 1

    jobs = list(get_jobs(training_id, hours))
    users = list(get_users(training_id))
    jobs_overview = {}
    state_summary = {}
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

        if job["state"] not in state_summary:
            state_summary[job["state"]] = 0
        if "__total__" not in state_summary:
            # div 0
            state_summary["__total__"] = 1

        state_summary[job["state"]] += 1
        state_summary["__total__"] += 1

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
            "training": training,
            "jobs": jobs,
            "jobs_overview": jobs_overview,
            "users": users,
            "state": state_summary,
        },
    )
