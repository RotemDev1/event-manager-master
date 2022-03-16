from django.test import TestCase
from django.urls import reverse
from ..models import Event, CancelledEvent, EventUpdates, RateEvent, MyEvent, EventComment, EventRecommend
from django.contrib.auth.models import User


class ViewEventTest(TestCase):
    def setUp(self):
        test_event_1 = Event.objects.create(
            title='Event 1',
            description='Desc 1',
            start_date='2000-01-01 10:00',
            end_date='2000-01-01 12:00',
            capacity=100,
            place='tel-aviv'
        )
        test_event_1.save()

        test_event_2 = Event.objects.create(
            title='Event 2',
            description='Desc 2',
            start_date='2003-01-01 10:00',
            end_date='2003-01-01 12:00',
            capacity=200,
            place='tel-aviv'
        )
        test_event_2.save()
        test_user1 = User.objects.create_user(
            username='testuser1', password='Aa123123')

        test_user1.save()

        CommentId = EventComment.objects.create(
            EventId=2, user=test_user1, text="test")
        CommentId.save()

        CommentToDelete = EventComment.objects.create(
            EventId=1, user=test_user1, text="to delete")
        CommentToDelete.save()

        RecommendId = EventRecommend.objects.create(
            EventId=2, user=test_user1, text="test")
        RecommendId.save()

        test_cancelled_event = CancelledEvent.objects.create(EventId=1)
        test_cancelled_event.save()

        test_rate_event = RateEvent.objects.create(EventId=2, user=User.objects.create(
            username='test1', email='test@email.com', first_name='Big', last_name='Bob'), rate=5)
        test_rate_event.save()

        test_event_update = EventUpdates.objects.create(
            EventId=2, announcement='ann test')
        test_event_update.save()

        test_my_events = MyEvent.objects.create(EventId=2, user=User.objects.create(
            username='test2', email='test2@email.com', first_name='Big2', last_name='Bob2'))
        test_my_events.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('event-view', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('event-view', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event.html')

    def test_view_Event_Top_Rated_url_exists_at_desired_location(self):
        response = self.client.get(reverse('event-top-rated'))
        self.assertEqual(response.status_code, 200)

    def test_view_Event_Top_Rated_uses_correct_template(self):
        response = self.client.get(reverse('event-top-rated'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/top_rate_list.html')

    def test_view_not_found(self):
        response = self.client.get(reverse('event-view', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_report_comment(self):
        self.client.login(username='testuser1', password='Aa123123')
        response = self.client.get(reverse('report_comment', args=[1]))
        self.assertRedirects(response, '/event/2/')

    def test_redirect_if_choose_comment(self):
        self.client.login(username='testuser1', password='Aa123123')
        response = self.client.get(reverse('choose_comment', args=[1]))
        self.assertRedirects(response, '/event/2/')

    def test_redirect_if_report_delete(self):
        self.client.login(username='testuser1', password='Aa123123')
        response = self.client.get(reverse('delete_comment', args=[2]))
        self.assertRedirects(response, '/event/1/')

    def test_delete_comment(self):
        self.client.login(username='testuser1', password='Aa123123')
        self.client.get(reverse('delete_comment', args=[2]))
        comment = EventComment.objects.all().filter(EventId=1)
        self.assertQuerysetEqual(comment, [])


class CalendarTest(TestCase):
    def setUp(self):
        test_event_1 = Event.objects.create(
            title='Event 1',
            description='Desc 1',
            start_date='2000-01-01 10:00',
            end_date='2000-01-01 12:00',
            capacity=100,
            place='tel-aviv'
        )
        test_event_1.save()

        test_event_2 = Event.objects.create(
            title='Event 2',
            description='Desc 2',
            start_date='2003-01-01 10:00',
            end_date='2003-01-01 12:00',
            capacity=200,
            place='tel-aviv'
        )
        test_event_2.save()
        test_user1 = User.objects.create_user(
            username='testuser1', password='Aa123123')

        test_user1.save()

        CommentId = EventComment.objects.create(
            EventId=2, user=test_user1, text="test")
        CommentId.save()

        CommentToDelete = EventComment.objects.create(
            EventId=1, user=test_user1, text="to delete")
        CommentToDelete.save()

        RecommendId = EventRecommend.objects.create(
            EventId=2, user=test_user1, text="test")
        RecommendId.save()

        test_cancelled_event = CancelledEvent.objects.create(EventId=1)
        test_cancelled_event.save()

        test_rate_event = RateEvent.objects.create(EventId=2, user=User.objects.create(
            username='test1', email='test@email.com', first_name='Big', last_name='Bob'), rate=5)
        test_rate_event.save()

        test_event_update = EventUpdates.objects.create(
            EventId=2, announcement='ann test')
        test_event_update.save()

        test_my_events = MyEvent.objects.create(EventId=2, user=User.objects.create(
            username='test2', email='test2@email.com', first_name='Big2', last_name='Bob2'))
        test_my_events.save()

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='Aa123123')
        response = self.client.get(reverse('event-calendar'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='Aa123123')
        response = self.client.get(reverse('event-calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/calendar.html')

    def test_view_url_if_not_logged_in(self):
        response = self.client.get(reverse('event-calendar'))
        self.assertEqual(response.status_code, 302)


class AttendViewTest(TestCase):
    def setUp(self):
        test_event_1 = Event.objects.create(
            title='Event 1',
            description='Desc 1',
            start_date='2000-01-01 10:00',
            end_date='2000-01-01 12:00',
            capacity=100,
            place='tel-aviv'
        )
        test_event_1.save()

        test_event_2 = Event.objects.create(
            title='Event 2',
            description='Desc 2',
            start_date='2003-01-01 10:00',
            end_date='2003-01-01 12:00',
            capacity=200,
            place='tel-aviv'
        )
        test_event_2.save()
        test_user1 = User.objects.create_user(
            username='testuser1', password='Aa123123')

        test_user1.save()

        RecommendId = EventRecommend.objects.create(
            EventId=2, user=test_user1, text="test")
        RecommendId.save()

        test_cancelled_event = CancelledEvent.objects.create(EventId=1)
        test_cancelled_event.save()

        test_event_update = EventUpdates.objects.create(
            EventId=2, announcement='ann test')
        test_event_update.save()

        test_my_events = MyEvent.objects.create(EventId=2, user=User.objects.create(
            username='test2', email='test2@email.com', first_name='Big2', last_name='Bob2'))
        test_my_events.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('event-users', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_url_not_found(self):
        response = self.client.get(reverse('event-users', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('event-users', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/users_attend.html')
