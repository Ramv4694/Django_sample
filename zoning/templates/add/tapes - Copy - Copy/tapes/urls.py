from django.conf.urls import url,include
from django.contrib import admin
from .import views
from .views import UnidentifiedDatatableView,ManualSavesetDatatableView,MulDatatableView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^$', views.home,name="home"),
    url(r'^report/$',views.report,name='report'),

    url(r'^report/Discarded/', views.Discard,name='Discarded'),



    url(r'^report/(?P<type>[\w-]+)/$',views.type_details,name='volret'),
    url(r'^report/manual/saveset/$',views.manual_saveset, name='manual_saveset'),



    url(r'^mul/(?P<type>[\w-]+)/$',MulDatatableView.as_view(), name='mul_json'),
    url(r'^manual_saveset/$',ManualSavesetDatatableView.as_view(), name='manual_saveset_json'),
    url(r'^unidentified/$',UnidentifiedDatatableView.as_view(), name='unidentified_json'),



    url(r'^download_csv/(?P<type>[\w-]+)/$',views.download_csv, name='download_csv'),
    url(r'^check/$',views.check,name="check")

]

#used to access files in static folder using url 'static/'
urlpatterns += staticfiles_urlpatterns()
