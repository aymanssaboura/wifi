from django.shortcuts import render, redirect
from trip.models import Location , Trip 
from company.models  import Company
# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime as dt



def home(request):
        companys = Company.objects.get(pk=1)
        return render(request, 'guest/home.html',{'company':companys,'navbar':"home"})



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
