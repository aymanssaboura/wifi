import json
from django.shortcuts import render,redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView ,DetailView,CreateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.db.models import Q
from django.contrib import messages
from datetime import datetime as dt
from django.contrib.auth.decorators import user_passes_test
from .forms import Post as PostForm,Imagepath as Imagepathform
from .models import Post  ,imagepath 
from trip.models import Location , Trip 
from company.models  import Company

def home(request):
        posts=Post.objects.all()
        companys = Company.objects.get(pk=1)
        return render(request, 'guest/home.html',{'company':companys,'navbar':"home",'posts':posts})



def index(request):
    companys = Company.objects.get(pk=1)
    locations = Location.objects.all()
    return render(request, 'guest/transport.html',{
        'company':companys,'locations':locations,'navbar':"tickit"
    })

def searchLocation(request):
    loc= request.GET.get('fromLoc')
    # print(loc)
    if loc :

        locations = Location.objects.exclude(id=loc)
    else :
        locations = Location.objects.all()
    return render(request, 'guest/locations.html', {
        'locations':locations
    })

# cityFrom
# cityTo
# company  start_time
def searchTrip(request):
    if request.method == "POST":
        fromLoc = get_object_or_404(Location, pk=request.POST['fromLoc'])
        toLoc = get_object_or_404(Location, pk=request.POST['toLoc'])

        Date=request.POST['Date']
        PassengerCount=request.POST['PassengerCount']
        if not Date:
            trips = Trip.objects.filter(
                Q(cityFrom=fromLoc)&
                Q(cityTo=toLoc)&
                Q(start_time__gte=dt.now().date())    )
        else:
            trips = Trip.objects.filter(
                Q(cityFrom=fromLoc)&
                Q(cityTo=toLoc)   &
                Q(start_time__date=Date)    )



        return render(request,'searchTrip_list.html',{'trips':trips})




def trip(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/package.html',{'company':companys,'navbar':"trip"})



def flight(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/flight.html',{'company':companys,'navbar':"tickit"})

def sea(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/sea.html',{'company':companys,'navbar':"tickit"})

def visa(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/visa.html',{'company':companys,'navbar':"visa"})

def hotel(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/hotel.html',{'company':companys,'navbar':"hotel"})

def insurance(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/insurance.html',{'company':companys,'navbar':"insurance"})

def document(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/document.html',{'company':companys,'navbar':"document"})

def shipping(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/shipping.html',{'company':companys,'navbar':"shipping"})

def about(request):
    companys = Company.objects.get(pk=1)
    return render(request, 'guest/about.html',{'company':companys,'navbar':"about"})







@login_required
def add_post(request):
    if not request.user.is_MANAGER:
        return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "postListChanged": None,
            })
        })
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        formimage = Imagepathform(request.POST)
        if request.POST:
         image=request.FILES.get('image')
        print("-------------------------------")
       
        print(image)
       
        if form.is_valid()  :
            
            post = form.save(commit=False)
            post.image = image
            post.save()
           
           
           
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": f"{post.title} added."
                    })
                })
        else:
            return render(request, 'guest/add_post.html', {'form': form,'formimage':formimage})
    else:
        
        form = PostForm()
        formimage = Imagepathform()
       
    return render(request, 'guest/add_post.html', {
        'form': form,'formimage':formimage })

@login_required
def edit_post(request, pk):
    post = get_object_or_404(post, pk=pk)
    imagepath = get_object_or_404(imagepath , pk = pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        formimage = Imagepathform(request.POST, instance=imagepath)
        # print(request.FILES, 'form.is_valid')

        if form.is_valid()and formimage.is_valid():
            Imagepath = imagepathform.save(commit=False)
            Imagepath.company=request.user.company
            Imagepath.author=request.user
            Imagepath.save()

            post = form.save(commit=False)
            post.author=request.user
            post.company=request.user.company
            post.account=account

            post.save()


            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": f"{post.title} updated."
                    })
                }
            )
    else:
        formimage = Imagepathform()
        form = PostForm()
        # print('form   :  ',form)
    return render(request, '/', {
        'form': form,'formimage':formimage,
        'post': post,
    })

@login_required
@ require_POST
def remove_post(request, pk):
    post = get_object_or_404(post, pk=pk)
    imagepath = get_object_or_404(Imagepath , pk = pk)
    imagepath.soft_delete()
    post.soft_delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "postListChanged": None,
                "showMessage": f"{post.title} deleted."
            })
        })


            