from django.conf.urls import patterns, include, url
from algorithm import views

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'biteit.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	# url(r'^admin/', include(admin.site.urls)),
	# url(r'^$', views.api_root),
	# url(r'^account/$', 
		# views.AccountList.as_view(), 
		# name='account-list'),
	# url(r'^account/(?P<pk>[0-9]+)/$', 
		# views.AccountDetail.as_view(), 
		# name='account-detail'),
	url(r'^route/',
        views.route,
        name='route'),
)

# urlpatterns = format_suffix_patterns(urlpatterns)
