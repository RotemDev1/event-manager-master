from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from .models import Event
from .models import CancelledEvent
from .models import EventUpdates
from .models import RateEvent
from .models import MyEvent
from .models import EventComment
from .models import EventRecommend
from .models import ReportComment
from .models import ChooseComment
from .forms import RateEventForm, eventCommentForm, eventRecommendForm


# Create your views here.

example = 123

print(f'hello')

def home(request):
    return render(request, 'event/home.html')


def event_list(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if limit is None:
        limit = 5
    else:
        limit = int(limit)
        if limit < 1 or limit > 20:
            limit = 5

    p = Paginator(Event.objects.all(), limit)
    if page is None:
        page = 1
    else:
        page = int(page)
        if page < 1 or page > p.num_pages:
            page = 1
    context = {
        'page_obj': p.get_page(page),
        'announcements': EventUpdates.objects.all(),
        'cancelled_events': CancelledEvent.objects.all(),
        'site_header': 'Event List',
        'site_subheader': 'Events Of All Times'
    }
    return render(request, 'event/event_list.html', context)


def recommended_event_list(request):
    context = {
        'events': Event.objects.filter(start_date__gte=date.today()),
        'announcements': EventUpdates.objects.all(),
        'cancelled_events': CancelledEvent.objects.all(),
        'recommended_events': EventRecommend.objects.all(),
        'site_header': 'Recommended Events',
        'site_subheader': 'All Of Our Recommendations'
    }
    return render(request, 'event/recommended_event_list.html', context)


def view_event(request, id):

    ratingForm = None
    commentForm = eventCommentForm()
    recommendForm = eventRecommendForm()
    my_rating = None
    my_event = []

    if request.method == 'POST' and 'comment_post' in request.POST:
        commentForm = eventCommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user_id = request.user.id
            comment.EventId = id
            comment.save()
            return redirect('event-view', id=id)

    if request.method == 'POST' and 'recommend_post' in request.POST:
        recommendForm = eventRecommendForm(request.POST)
        if recommendForm.is_valid():
            recommend = recommendForm.save(commit=False)
            recommend.user_id = request.user.id
            recommend.EventId = id
            recommend.save()
            return redirect('event-view', id=id)

    if request.user.id:
        my_event = MyEvent.objects.filter(EventId=id, user=request.user)
        my_rating = (RateEvent.objects.filter(
            user=request.user).filter(EventId=id).first())
        if my_rating is None:
            if request.method == 'POST' and 'rating_post' in request.POST:
                ratingForm = RateEventForm(request.POST)

                if ratingForm.is_valid():
                    rating = ratingForm.save(commit=False)
                    if rating.user_id is None:
                        rating.user_id = request.user.id
                        rating.EventId = id
                    rating.save()
                    my_rating = (RateEvent.objects.filter(
                        user=request.user).filter(EventId=id).first())
            else:
                ratingForm = RateEventForm()

    event = get_object_or_404(Event, id=id)

    reps = ReportComment.objects.filter(EventId=id)
    reports = []
    for rep in reps:
        skip = False
        for rep2 in reports:
            if rep.CommentId == rep2.CommentId:
                skip = True
                break
        if skip:
            continue
        reports.append(rep)

    context = {
        'event': event,
        'announcements': EventUpdates.objects.filter(EventId=id),
        'cancelled_event': CancelledEvent.objects.filter(EventId=id),
        'registered_users': MyEvent.objects.filter(EventId=id).count(),
        'ratings_counts': RateEvent.objects.filter(EventId=id).count(),
        'ratings_avg': RateEvent.objects.filter(EventId=id).aggregate(Avg('rate')),
        'my_rating': my_rating,
        'comments': EventComment.objects.all().filter(EventId=id),
        'recommends': EventRecommend.objects.all().filter(EventId=id),
        'my_event': my_event,
        'ratingForm': ratingForm,
        'commentForm': commentForm,
        'recommendForm': recommendForm,
        'reports': reports,
        'chooseComment': ChooseComment.objects.filter(EventId=id),
        'site_header': event.title,
        'site_subheader': event.description,
        'site_meta': event.start_date,
        'site_header_class': 'post-heading'
    }

    return render(request, 'event/event.html', context)


def top_rated_list(request):

    events = Event.objects.filter(start_date__gte=date.today())
    cancelled_events = CancelledEvent.objects.all()
    rating = MyEvent.objects.values('EventId').annotate(
        aRate=Count('EventId')).order_by('-aRate')

    ev = []
    total = 0
    for e in events:
        cancelled = False
        for can in cancelled_events:
            if e.id == can.EventId:
                cancelled = True
                break
        if cancelled:
            continue
        for r in rating:
            if e.id == r['EventId']:
                ev.append(e)
                total += 1
        if total == 5:
            break

    context = {
        'events': ev,
        'announcements': EventUpdates.objects.all(),
        'events_avg_rating': rating,
        'site_header': 'Top Events',
        'site_subheader': 'Top 5 Trending Events'
    }
    return render(request, 'event/top_rate_list.html', context)


@login_required
def choose_comment(request, id):
    try:
        comment = EventComment.objects.get(id=id)
        EventId = comment.EventId
        if (EventId is not None):
            ChooseComment.objects.create(
                EventId=EventId, CommentId=comment, user=request.user)
            messages.success(
                request, 'LIKE Comment Successful')
    except:
        messages.warning(
            request, 'ERROR - You are already liked this comment')

    return redirect('event-view', id=EventId)


@login_required
def my_events(request):
    if request.method == 'POST':
        eventId = request.POST.get('EventId', None)
        if (eventId is not None):
            MyEvent.objects.create(EventId=eventId, user=request.user)
            messages.success(
                request, 'Event was added to your events successfully')

    context = {
        'events': Event.objects.filter(start_date__gte=date.today()),
        'announcements': EventUpdates.objects.all(),
        'cancelled_events': CancelledEvent.objects.all(),
        'my_events': MyEvent.objects.filter(user_id=request.user.id),
        'site_header': 'My Nearest Events',
        'site_subheader': 'Upcoming Events You Are Going To'
    }
    return render(request, 'event/my_events.html', context)


@login_required
def my_events_past(request):
    context = {
        'events': Event.objects.filter(start_date__lte=date.today()),
        'announcements': EventUpdates.objects.all(),
        'cancelled_events': CancelledEvent.objects.all(),
        'my_events': MyEvent.objects.filter(user_id=request.user.id),
        'site_header': 'My Past Events',
        'site_subheader': 'Events You Already Attended'
    }
    return render(request, 'event/my_events.html', context)


@login_required
def my_events_all(request):
    context = {
        'events': Event.objects.all(),
        'announcements': EventUpdates.objects.all(),
        'cancelled_events': CancelledEvent.objects.all(),
        'my_events': MyEvent.objects.filter(user_id=request.user.id),
        'site_header': 'My Events',
        'site_subheader': 'All Events You Added To Your Event List'
    }
    return render(request, 'event/my_events.html', context)


@login_required
def remove_my_event(request, id):
    if request.method == 'POST':
        myId = request.POST.get('id', None)
        if (myId is not None):
            MyEvent.objects.filter(
                id=myId, user_id=request.user.id, EventId=id).delete()

            messages.success(
                request, 'Event was removed from your events successfully')
            return redirect('event-my_events')
    context = {
        'event': get_object_or_404(Event, id=id),
        'my_events': MyEvent.objects.filter(user_id=request.user.id, EventId=id)
    }
    return render(request, 'event/confirm_remove_my_event.html', context)


@login_required
def delete_comment(request, id):
    comment = EventComment.objects.get(id=id)
    EventId = comment.EventId
    if (id is not None):
        EventComment.objects.filter(
            id=id).delete()

    return redirect('event-view', id=EventId)


@login_required
def report_comment(request, id):
    try:
        comment = EventComment.objects.get(id=id)
        EventId = comment.EventId
        if (EventId is not None):
            ReportComment.objects.create(
                EventId=EventId, CommentId=comment, user=request.user)
            messages.success(
                request, 'Comment Reported Successfully')
    except:
        messages.warning(
            request, 'ERROR - Already Reported?')

    return redirect('event-view', id=EventId)


@login_required
def calendar(request):
    events = Event.objects.filter(
        start_date__gte=date.today()).order_by('start_date')

    my_events = MyEvent.objects.filter(user_id=request.user.id)
    cancelled_events = CancelledEvent.objects.all()

    ev = []
    year_break = []
    month_break = []
    year = 0
    month = 0
    for e in events:
        for my in my_events:
            cancelled = False
            for can in cancelled_events:
                if e.id == can.EventId:
                    cancelled = True
                    break
            if cancelled:
                continue
            if e.id == my.EventId:
                ev.append(e)
                if year != e.start_date.year:
                    year = e.start_date.year
                    year_break.append(e.id)
                    month = 0
                if month != e.start_date.month:
                    breakm = month != 0
                    month = e.start_date.month
                    month_break.append({'id': e.id, 'break': breakm})

    context = {
        'events': ev,
        'year_break': year_break,
        'month_break': month_break,
        'site_header': 'Calendar',
        'site_subheader': ' '
    }
    return render(request, 'event/calendar.html', context)


def users_attend(request, id):
    event = get_object_or_404(Event, id=id)
    context = {
        'event': event,
        'users': MyEvent.objects.filter(EventId=id),
        'site_header': event.title,
        'site_subheader': 'Attendencies'
    }
    return render(request, 'event/users_attend.html', context)
