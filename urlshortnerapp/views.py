from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Urlshortner
from django.contrib.auth import login,logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import datetime
from django.utils import timezone
import string
import random

# Create your views here.
BASE_URL="https://shurl-dx9w.onrender.com/"

def signup(request):

    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{'form':form})

def login_fn(request):
    if request.POST:
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('create')
    
    else:
        form = AuthenticationForm()

    return render(request,'login.html',{'form':form})

@login_required(login_url='/login-page/')
def logout_fn(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')
    
    return render('list')

@login_required(login_url='/login-page/')
def create_fn(request):

    req_user = request.user
    shorturl = None
    error = None
    if request.POST:
        url = Urlshortner.objects.filter(user = request.user)
        if url.count() >=10:
            error ='Your limit has been reached.'
            return render(request,'create.html',{'shorturl':shorturl,'error':error})
        else:
            url_obj = Urlshortner()
            print(request.POST)
            title = request.POST.get('title')
            url = request.POST.get('original_url')
            print(url)
            random_char = ''.join(random.choices(string.ascii_lowercase,k = 7))
            if Urlshortner.objects.filter(short_url = f'{BASE_URL}{random_char}').exists():
                random_char = ''.join(random.choices(string.ascii_lowercase,k = 7))
            url_obj.user = request.user
            url_obj.title = title
            url_obj.original_url = url
            url_obj.short_url = f'{BASE_URL}{random_char}'
            url_obj.time = datetime.datetime.now().time()
            url_obj.save()
            shorturl = get_short_url_to_show_add_page(req_user,url) 

    return render(request,'create.html',{'shorturl':shorturl,'error':error})

# The below function used to show the shorten url in create url page

def get_short_url_to_show_add_page(req_user,url):
    try:
        get_url = Urlshortner.objects.get(user = req_user,original_url = url)
    except Urlshortner.DoesNotExist:
        return
    else:
        return get_url.short_url


"""This function that redirect the user to his original url"""

def redirect_to_original(request,rand_char):
    print(request.GET)
    print(rand_char)
    if Urlshortner.objects.filter(short_url = f'{BASE_URL}{rand_char}').exists():
        original_path = Urlshortner.objects.filter(short_url = f'{BASE_URL}{rand_char}').first()
        return redirect(original_path.original_url)
    
    return HttpResponse('Invalid Link')

#Showing List

@login_required(login_url='/login-page/')
def list_fn(request):
    url = Urlshortner.objects.filter(user = request.user)
    paginator = Paginator(url,2)

    page_number = request.GET.get('page') #on click the page number to get
    page_obj = paginator.get_page(page_number)

    return render(request,'list.html',{'page_obj':page_obj})

#Edit url

@login_required(login_url='/login-page/')
def edit_fn(request,pk):
    instObj = Urlshortner.objects.get(pk=pk ,user = request.user)
    if request.POST:
        edited_title = request.POST.get('edited_title')
        edited_url = request.POST.get('edited_url')
        instObj.title = edited_title
        instObj.original_url = edited_url
        instObj.time = datetime.datetime.now().time()
        instObj.save()
        return redirect('list')
    return render(request,'edit.html',{'editObj':instObj})

#Delete url
@login_required(login_url='/login-page/')
def delete_fn(request,pk):
    instObj = Urlshortner.objects.get(pk=pk ,user = request.user)
    if request.method == 'GET':
        instObj.delete()
        return redirect('list')

    return redirect('list')

#Search url
@login_required(login_url='/login-page/')
def search_fn(request):
    recedata = request.GET.get('getdata',"")     #query dict then using "get" method to get data
    print(recedata)

    dataFromDb = Urlshortner.objects.filter(Q(user = request.user) & (Q(title__icontains = recedata) | Q( original_url= recedata) | Q(short_url =recedata ))) # users complete data as a Queryset like this <QuerySet [<Urlshortner: Urlshortner object (1)>, <Urlshortner: Urlshortner object (3)>, <Urlshortner: Urlshortner object (4)>, <Urlshortner: Urlshortner object (5)>]>
    print(dataFromDb)

    filterdata = [{"id":data.id,"title":data.title,'originalurl':data.original_url,'shorturl':data.short_url,'time':data.time.strftime('%I:%M %p')} for data in dataFromDb]
    print(filterdata)

    return JsonResponse(filterdata,safe=False) #safe = false because to pass no-dict values(here a list of dict)
