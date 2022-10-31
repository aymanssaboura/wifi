from django.db import models
from company.models import Company
from customer.models import Customer
from django.conf import settings
from trip.models import Trip,Location
from coin.models import Coin
from passport.models import Passport, Passenger
from common.models import BaseModel, SoftDeleteModel


class Reservation(models.Model):
    title      = models.CharField(max_length=255,null=True,blank=True)
    Date       = models.DateTimeField( blank=True)
    customer   = models.ForeignKey(Customer, null=True,blank=True, on_delete=models.SET_NULL ,related_name='CustomerCompany')
    
    def __str__(self):
        return f'{self.title}'

class Airport (models.Model):
    airportcode =models.CharField(max_length=10,null=True,blank=True)
    aurport_city =models.CharField(max_length=50,null=True,blank=True)
    aurport_country =models.CharField(max_length=50,null=True,blank=True)


class MotherCompany (models.Model):
    CompanyName =models.CharField(max_length=50,null=True,blank=True)
    category     = models.CharField(max_length=2, choices=(('1','Airline'),('2','Transport'),('3','Farry'),
                                                           ('4','Hotel'),('5','Visa'),
                                                           ('6','Insurance'),('7','Shipping')), default=1)

class SubReservation(models.Model):
    reservationID =          models.ForeignKey(Reservation,on_delete=models.CASCADE )
    reservation_type     =   models.PositiveIntegerField(choices=(('1','Airline'),('2','Transport'),('3','Farry'),
                                                                 ('4','Hotel'),('5','Visa'),('6','Insurance'),('7','Shipping'),
                                                                 ('8','Package'),('9','Document'),('10','Commition')), default=1)
    Itemscount           =  models.PositiveSmallIntegerField( null=True,blank=True,default=1)
    private_no1   =                  models.CharField(max_length=25, blank=True,null=True   )
    private_no2   =                  models.CharField(max_length=25, blank=True,null=True   )
    departure_date  = models.DateTimeField( blank=True,null=True ,help_text="تاريخ المغادرة " )
    return_date     = models.DateTimeField(  blank=True,null=True, help_text="تاريخ العودة ")
    mother_company   = models.ForeignKey(MotherCompany,null=True, on_delete=models.SET_NULL,related_name= 'Airlinecompany' )
    flight_no        = models.CharField(max_length=25,blank=True,null=True)
    city1= models.ForeignKey(Airport,null=True, on_delete=models.SET_NULL,related_name= 'departure' )
    city2= models.ForeignKey(Airport,null=True, on_delete=models.SET_NULL,related_name= 'arrival' )
    roundtrip       = models.BooleanField(default=False,help_text="ذهاب وعودة ")
    trip_type = models.CharField(max_length=3, choices=(('1','Economy Class'),('2','Business Class'),('3','First Class'))  )
    supplier   = models.ForeignKey(Customer, null=True,blank=True, on_delete=models.SET_NULL ,related_name='suppliersCompany')   
    pay_price  = models.PositiveIntegerField(default=0)
    pay_coin   = models.ForeignKey(Coin, null=True ,on_delete=models.SET_NULL,related_name= 'payCoin' )
    sell_price = models.PositiveIntegerField(default=0)
    sell_coin  = models.ForeignKey(Coin, null=True ,on_delete=models.SET_NULL,related_name='sellCoin' )
    status     = models.CharField(max_length=2, choices=(('1','Active'),('2','Cancelled'),('3','pending'),), default=1)

class ItemReservation(models.Model):
    subreservation =          models.ForeignKey(SubReservation,on_delete=models.CASCADE )
    Passport =          models.ForeignKey(Passport,on_delete=models.SET_NULL,null=True,blank=True )

class Goods (models.Model):
     subreservation =          models.ForeignKey(SubReservation,on_delete=models.CASCADE )
     goodstype =      models.PositiveIntegerField(choices=(('1','Box'),('2','Envelope'),('3','Bag'),('4','Other')),default=1)  
     goodscount =      models.PositiveIntegerField(default=1,blank=True,null=True)  
     goodswight=  models.FloatField(default=1,blank=True,null=True)
