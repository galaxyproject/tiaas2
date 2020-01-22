from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import Http404
from .models import Training
from django.urls import reverse
from .galaxy import get_roles, create_role, get_groups, create_group, add_group_user, get_jobs, get_users, authenticate
from .forms import TrainingForm

def register(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.cleaned_data['training_identifier'] = form.cleaned_data['training_identifier'].lower()
            form.save()
            return HttpResponseRedirect(reverse('thanks'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, "training/register.html", {"form": form})

def thanks(request):
    return render(request, "training/thanks.html")

def stats(request):
    trainings = Training.objects.all()
    return render(request, "training/stats.html", {'trainings': trainings})

def join(request, training_id):
    try:
        training = Training.objects.get(training_identifier=training_id.lower())
    except Training.DoesNotExist:
        raise Http404("Training does not exist")

    user = authenticate(request)
    if not user:
        raise HttpResponseForbidden()

    # If we don't know this training, reject
    if training.processed != 'AP':
        raise Http404("Training is not active")

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
        raise Http404("Training does not exist")

    # hours param
    hours = int(request.GET.get('hours', 3))
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
        data['ok_percent'] = data['ok'] / len(jobs)
        data['new_percent'] = data['new'] / len(jobs)
        data['error_percent'] = data['error'] / len(jobs)
        data['queued_percent'] = data['queued'] / len(jobs)
        data['running_percent'] = data['running'] / len(jobs)

    return render(request, "training/status.html", {"training": training, 'jobs': jobs, 'jobs_overview': jobs_overview, 'users': users, 'state': state_summary})
