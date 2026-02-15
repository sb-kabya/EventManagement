from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Category, Participant
from .forms import EventForm
from datetime import date
# Create your views here.
# EVENT LIST


def event_list(request):
    events = Event.objects.select_related(
        'category').prefetch_related('participants')
    search = request.GET.get('search')
    filter_type = request.GET.get('filter')

    if search:
        events = events.filter(Q(name__icontains=search)
                               | Q(location__icontains=search))

    if filter_type == "upcoming":
        events = events.filter(date__gt=date.today())
    elif filter_type == "past":
        events = events.filter(date__lt=date.today())
    elif filter_type == "participants":
        events = events.annotate(num_participants=Count(
            'participants')).order_by('-num_participants')
    context = {'events': events}
    return render(request, 'events/event_list.html', context)


def add_event(request):

    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('events:event_list')

    else:
        form = EventForm()

    return render(request, 'events/form.html', {'form': form})


def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/form.html', {'form': form})


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()

    return redirect('events:event_list')


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def dashboard(request):
    today = date.today()

    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming = Event.objects.filter(date__gte=today).count()
    past = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.select_related(
        'category').prefetch_related('participants').filter(date=today)

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming': upcoming,
        'past': past,
        'todays_events': todays_events
    }

    return render(request, 'events/dashboard.html', context)
