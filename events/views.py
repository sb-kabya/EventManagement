from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
from .models import Event, Category, RSVP
from .forms import EventForm, SignUpForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activation_link = request.build_absolute_uri(
                f"/activate/{user.id}/"
            )
            # Send email
            send_mail(
                'Activate Your Account',
                f'Click this link to activate your account: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'events/signup_success.html', {'email': user.email})
    else:
        form = SignUpForm()
    return render(request, 'events/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('events:dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'events/login.html')


def logout_view(request):
    logout(request)
    return redirect('events:login')


def activate_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    return render(request, 'events/activation_success.html', {'user': user})


def is_admin(user):
    return user.is_staff


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participant(user):
    return user.groups.filter(name='Participant').exists()


@login_required
def dashboard_redirect(request):
    can_add_event = request.user.is_staff or is_organizer(request.user)

    if request.user.is_staff:
        return redirect('events:admin_dashboard')
    elif is_organizer(request.user):
        return redirect('events:organizer_dashboard')
    else:
        return redirect('events:participant_dashboard')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    today = date.today()
    total_events = Event.objects.count()
    upcoming = Event.objects.filter(date__gte=today).count()
    past = Event.objects.filter(date__lt=today).count()
    total_participants = RSVP.objects.count()
    todays_events = Event.objects.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'upcoming': upcoming,
        'past': past,
        'total_participants': total_participants,
        'todays_events': todays_events,
        'can_add_event': True,
    })


@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):
    today = date.today()
    total_events = Event.objects.filter(organizer=request.user).count()
    upcoming = Event.objects.filter(
        organizer=request.user, date__gte=today).count()
    past = Event.objects.filter(organizer=request.user, date__lt=today).count()
    total_participants = RSVP.objects.filter(
        event__organizer=request.user).count()
    todays_events = Event.objects.filter(organizer=request.user, date=today)
    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'upcoming': upcoming,
        'past': past,
        'total_participants': total_participants,
        'todays_events': todays_events,
        'can_add_event': True,
    })


@login_required
@user_passes_test(is_participant)
def participant_dashboard(request):
    rsvped_events = Event.objects.filter(rsvps__user=request.user)
    return render(request, 'events/dashboard.html', {
        'events': rsvped_events,
        'can_add_event': False,
    })


@login_required
def event_list(request):
    events = Event.objects.select_related(
        'category').annotate(total_rsvps=Count('rsvps'))

    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(
            location__icontains=search_query))

    today = date.today()
    if filter_type == 'upcoming':
        events = events.filter(date__gte=today)
    elif filter_type == 'past':
        events = events.filter(date__lt=today)
    elif filter_type == 'participants':
        events = events.annotate(total_participants=Count(
            'rsvps')).order_by('-total_participants')

    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
@user_passes_test(lambda u: u.is_staff or is_organizer(u))
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            evt = form.save(commit=False)
            if is_organizer(request.user):
                evt.organizer = request.user
            evt.save()
            return redirect('events:event_list')
    else:
        form = EventForm()
    return render(request, 'events/form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff or is_organizer(u))
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff or is_organizer(u))
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events:event_list')
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    RSVP.objects.update_or_create(
        user=request.user, event=event, defaults={'status': 'GOING'}
    )
    return redirect('events:event_detail', pk=pk)
