from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from users import views as user_views
from .views import dashboard
from django.views.generic import TemplateView

urlpatterns =[
    path('i18n/',include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('', include('guest.urls')),
    path('users/', include('users.urls')),
    path('staff/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),

    path('blog', include('blog.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('account/', include('account.urls')),
    path('companys/', include('company.urls')),
    path('expenses/', include('expense.urls')),
    path('employee/', include('employee.urls')),
    path('reservation/', include('reservation.urls')),
    path('passport/', include('passport.urls')),
    path('customer/', include('customer.urls')),
    path('ttrip/', include('trip.urls')),
    path('ked/', include('ked.urls')),
    path('bus/', include('bus.urls')),
    
    # path('driver/', include('bus.urls')),

   )


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
