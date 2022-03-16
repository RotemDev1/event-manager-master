from users.admin import admin_site
from .models import Event
from .models import CancelledEvent
from .models import EventUpdates
from .models import RateEvent
from .models import MyEvent
from .models import EventComment
from .models import EventRecommend
from .models import ReportComment
from .models import ChooseComment

# Register your models here.
admin_site.register(Event)
admin_site.register(CancelledEvent)
admin_site.register(EventUpdates)
admin_site.register(RateEvent)
admin_site.register(MyEvent)
admin_site.register(EventComment)
admin_site.register(EventRecommend)
admin_site.register(ReportComment)
admin_site.register(ChooseComment)
