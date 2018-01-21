from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import DataFeed
from .forms import UserLoginForm,DataFeedForm,UserRegisterForm
from django.core import serializers
from django.contrib import messages
from django.core import serializers
import json
from django.contrib.auth.models import User

from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
def index(request):
	print(request.user.is_authenticated())
	if request.user.is_authenticated():
		return redirect("/home/")
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		user_details = User.objects.get(username=user)
		print(user_details.first_name)
		login(request,user)
		return HttpResponseRedirect('/home/')
	return render(request,"index.html",{'form':form,'title':'Login','btn':'Login'})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")

def home(request):
	form = DataFeedForm(request.POST or None)
	msg = "Successfully Created Waiting For Admin To Publish"
	if form.is_valid():
		instance = form.save(commit=False)
		if request.user.is_authenticated():
			instance.user = request.user
			if request.user.is_staff:
				instance.permission = True
				msg = "Successfully Created"
		else:
			instance.permission = True
			msg = "Successfully Created"
		instance.save()
		messages.success(request,msg)
		return HttpResponseRedirect('/home/')
	return render(request,"home.html",{'form':form,'title':'Home'})

def addemployee(request):
	if not request.user.is_staff:
		return redirect("/")
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		messages.success(request,"Successfully Added Employee")
		return HttpResponseRedirect('/addemployee/')
	return render(request,"index.html",{'form':form,'title':'Register Employees','btn':'Register'})

def input_list(request):
	input_detailsq = None
	if request.user.is_staff or not request.user.is_authenticated():
		input_detailsq = DataFeed.objects.all()
	else:
		input_detailsq = DataFeed.objects.filter(user=request.user,permission=True)
	mp = dict()
	for idd in input_detailsq:
		mp[idd.id] = {'input_text':idd.input_text,'permission':idd.permission}
	# kp = dict()
	# kp['superuser'] = request.user.is_staff
	# kp['details'] = mp
	return render(request,"input_list.html",{'input_details':input_detailsq})


def input_details(request,id=None):
	input_detailsq = None
	if request.user.is_staff or not request.user.is_authenticated():
		input_detailsq = DataFeed.objects.get(id=id)
	else:
		input_detailsq = DataFeed.objects.get(id=id,permission=True)
	return render(request,"input_details.html",{'input_detail':input_detailsq})

def update_permission(request):
	iid = request.POST.get('id')
	kp = dict()
	if iid == None:
		message = 'Sorry Input Text Not Found'
		messages.success(request,message)
		return redirect('/input_list/')
	else:
		inputd = DataFeed.objects.get(id=iid)
		inputd.permission = True
		inputd.save()
		message = 'Permission Updated'
		messages.success(request,message)
	return redirect('/input_list/')

# def api_login(request):
# 	username = request.POST.get('username')
# 	password = request.POST.get('password')
# 	user = authenticate(username=username,password=password)
# 	user_details = User.objects.get(username=user)
# 	dp = dict()
# 	if not user_details:
# 		dp['status'] = False
# 		return HttpResponse(dp)
# 	login(request,user)
# 	dp['status'] = True
# 	return HttpResponse(dp)
# def api_logout(request):
# 	logout(request)
# 	dp['status'] = True
# 	return HttpResponse(dp)

# def api_regemp(request):
# 	email = request.POST.get('email')
# 	username = request.POST.get('username')
# 	password = request.POST.get('password')
# 	first_name = request.POST.get('first_name') 
# 	last_name = request.POST.get('first_name') 
# 	if not request.user.is_staff:
# 		dp = dict()
# 		dp['status'] = False
# 		dp['message'] = 'Only Super User can add employees'
# 		return HttpResponse(dp)
# 	else:
# 		user = User(username=username,email=email,first_name=first_name,last_name=last_name)
# 		user.save(commit=False)
# 		user.set_password(password)
# 		user.save()
# 		dp = dict()
# 		dp['status'] = True
# 		dp['message'] = 'Employee Add Successfully'
# 		return HttpResponse(dp)





