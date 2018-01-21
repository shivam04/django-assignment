from django.conf.urls import url
from django.contrib import admin
from datafeed.views import index,logout_view,home,addemployee,input_list,input_details,update_permission#api_login,api_logout,api_regemp
urlpatterns = [
url(r'^$',index,name="index"),
	#url(r'^api/input_details/(?P<id>\d+)/$',input_details,name="input_details"),
	#url(r'^api/input_list/$',input_list,name="input_list"),
	url(r'^api/update_permission/$',update_permission,name="update_permission"),
	url(r'^input_list/$',input_list,name="input_list"),
	url(r'^input_details/(?P<id>\d+)/$',input_details,name="input_details"),
	# url(r'^api/login/$',api_login,name="api_login"),
	# url(r'^api/logout/$',api_logout,name="api_logout"),
	# url(r'^api/addemployee/$',api_regemp,name="api_regemp"),
    url(r'^logout/$',logout_view,name="logout"),
    url(r'^home/$',home,name="home"),
    url(r'^addemployee/$',addemployee,name="addemployee"),

]