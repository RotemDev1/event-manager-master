from django.test import TestCase
from ..models import ChooseComment, Event, CancelledEvent, EventUpdates, RateEvent, MyEvent, EventComment, ReportComment, EventRecommend
from django.contrib.auth.models import User


class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.
        Event.objects.create(
            title='test1',
            description='test1 desc',
            start_date='1990-01-01 10:00',
            end_date='1990-01-01 12:00',
            capacity=100,
            place='LOL'
        )

    def test_title_max_length(self):
        event = Event.objects.get(id=1)
        length = event._meta.get_field('title').max_length
        self.assertEquals(length, 120)

    def test_place_max_length(self):
        event = Event.objects.get(id=1)
        length = event._meta.get_field('place').max_length
        self.assertEquals(length, 120)

    def test_create_date_auto_now(self):
        event = Event.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class CancelledEventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.
        CancelledEvent.objects.create(
            EventId=2
        )

    def test_EventId_default(self):
        event = CancelledEvent.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)


class EventUpdatesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.
        EventUpdates.objects.create(
            EventId=2,
            announcement='Test me'
        )

    def test_EventId_default(self):
        event = EventUpdates.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        event = EventUpdates.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class EventRateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.

        RateEvent.objects.create(
            EventId=2,
            user=User.objects.create(
                username='test1', email='test@email.com', first_name='Big', last_name='Bob'),
            rate=5

        )

    def test_EventId_default(self):
        event = RateEvent.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        event = RateEvent.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class MyEventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.

        MyEvent.objects.create(
            EventId=2,
            user=User.objects.create(
                username='test1', email='test@email.com', first_name='Big', last_name='Bob'),
        )

    def test_EventId_default(self):
        event = MyEvent.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        event = MyEvent.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class EventCommentTest:
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.

        EventComment.objects.create(
            EventId=2,
            user=User.objects.create(
                username='test1', email='test@email.com', first_name='Big', last_name='Bob'),
            text="testing"

        )

    def test_EventId_default(self):
        event = EventComment.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        event = EventComment.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class EventRecommendTest:
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.

        EventRecommend.objects.create(
            EventId=2,
            user=User.objects.create(
                username='test1', email='test@email.com', first_name='Big', last_name='Bob'),
            text="testing"

        )

    def test_EventId_default(self):
        event = EventRecommend.objects.get(id=1)
        default = event._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        event = EventRecommend.objects.get(id=1)
        auto = event._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class ReportCommentTest:
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.
        user = User.objects.create(
            username='test1', email='test@email.com', first_name='Big', last_name='Bob',),
        ReportComment.objects.create(
            EventId=2,
            user=user,
            CommentId=EventComment.objects.create(
                EventId=2, user=user, text="test")

        )

    def test_EventId_default(self):
        report = ReportComment.objects.get(id=1)
        default = report._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        report = ReportComment.objects.get(id=1)
        auto = report._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)


class ChooseCommentTest:
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Run once to set up non-modified data for all class methods.
        user = User.objects.create(
            username='test1', email='test@email.com', first_name='Big', last_name='Bob',),
        ChooseComment.objects.create(
            EventId=2,
            user=user,
            CommentId=EventComment.objects.create(
                EventId=2, user=user, text="test")

        )

    def test_EventId_default(self):
        choosecomment = ChooseComment.objects.get(id=1)
        default = choosecomment._meta.get_field('EventId').default
        self.assertEquals(default, 0)

    def test_create_date_auto_now(self):
        choosecomment = ChooseComment.objects.get(id=1)
        auto = choosecomment._meta.get_field('create_date').auto_now
        self.assertEquals(auto, True)
