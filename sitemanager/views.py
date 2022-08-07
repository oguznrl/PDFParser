from django.shortcuts import  get_object_or_404, render, redirect
from .forms import EditUserForm, NewUserForm,PdfForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
super_user_log=False
def homepage(request):
	return render(request=request, template_name='sitemanager/home.html')

def register_request(request):
	global super_user_log
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			if(super_user_log):
				pass
			else:
				login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("sitemanager:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="sitemanager/register.html", context={"register_form":form})

def login_request(request):
	global super_user_log
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				super_user_log=True
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("sitemanager:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="sitemanager/login.html", context={"login_form":form})

def logout_request(request):
	global super_user_log
	logout(request)
	super_user_log=False
	messages.info(request, "You have successfully logged out.") 
	return redirect("sitemanager:homepage")

def view_users_request(request):
	users=User.objects.all()
	return render(request=request, template_name="sitemanager/users_table.html", context={"users":users})


def update_users_request(request,id):
	if request.method == "POST":
		ex_user=get_object_or_404(User,id=id)
		form = EditUserForm(request.POST,instance=ex_user)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Update successful." )
			return redirect("sitemanager:users")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="sitemanager/update_user.html",context={"update_form":form})

def delete_users_request(request,id):
	ex_user=get_object_or_404(User,id=id)
	ex_user.delete()
	messages.success(request, "Deletion successful." )
	return redirect("sitemanager:users")


def show_pdf_data(request):
	return render(request=request,template_name="sitemanager/data_table.html")

def pdf_data_detail(request):
	return render(request=request,template_name="sitemanager/data_detail.html")

def pdf_upload(request):
	form=PdfForm()
	return render(request=request, template_name="sitemanager/upload_pdf.html", context={"upload_form":form})



