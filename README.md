![Tiaas logo, galaxy three bars logo with human icons instead of bars, one bar is yellow and faster looking](./images/tiaas-logo.png)

# Training Infrastructure as a Service (TIaaS)

TIaaS provides a service which Galaxy administrators can deploy, enabling them to easily providing training infrastructure, as a service, to their user community.
We built TIaaS to streamline the process of hosting courses and training events on the Galaxy platform.

It enables:

- Administrators to control who is using their infrastructure for courses
- Teachers to easily request resources
- Teachers to monitor their classes and run efficient trainings
- Administrators to dedicate resources to trainings, enabling them to run smoothly and efficiently.

Once a training request is approved, teachers receive and share with students a URL like https://usegalaxy.eu/join-training/test (this is live, you can test it out!)

Upon visiting, students are automatically added to a group named `training-test` (and
a role automatically created.) It works on the basis of running underneath the
path prefix of Galaxy and so having access to the Galaxy session cookie. This
is decoded into a user id + the part after `/join-training/` decoded into a
group name, and this change is made.

## Features

### Status Page

For teachers giving trainings, we now offer a "status" page where they can see
the training queue of their class, both jobs and workflows.

![Status page showing a series of jobs in green and red (for failing) as well as an overview of how many of which tools have been executed and their current job state](images/queue.png)

### Register

Point your users to this service to register their training

![a registration form](images/register.png)

### Admin Interface

Admins can manage TIaaS courses in their view.

![Administrator View](images/admin.png)

## Documentation

- [Setup TIaaS for a Training Event](https://training.galaxyproject.org/training-material/topics/teaching/tutorials/setup-tiaas-for-training/tutorial.html)
- [Install TIaaS with the ansible role (for admins)](https://training.galaxyproject.org/training-material/topics/admin/tutorials/tiaas/tutorial.html)

## License

AGPL-3.0
