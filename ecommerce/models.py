import uuid
from cuid import cuid, CuidGenerator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# class Entrolment(models.Model):
    
#     PAYMENT_COMPLETED = "C"
#     PAYMENT_DENIED = "D"
#     PAYMENT_PENDING = "P"
        
#     PAYMENT_STATUS = [
  
#         (PAYMENT_COMPLETED, "Completed"),
#         (PAYMENT_DENIED, "Denied"),
#         (PAYMENT_PENDING, "Pending")
        
#     ]
    
    
#     course = models.ForeignKey("Course", on_delete=models.CASCADE) #1-m
#     student = models.ForeignKey("Student", on_delete=models.CASCADE)# 1-m
    
#     order = models.ForeignKey("Order", on_delete=models.CASCADE)
    
#     class Meta: 
#         unique_together = ("course", "student") #composite primary structure
    
class User(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    address = models.OneToOneField("Address", on_delete=models.CASCADE)
   
    def __str__(self):
       return self.email
   
    class Meta:
        ordering = ["-email"]
   
   
    
    
class Address(models.Model):
    post_Code = models.CharField(max_length=255, null=True)
    door_No = models.PositiveIntegerField()
    road_name = models.CharField(max_length=255)
    
    
class Promotions(models.Model):
    
    code = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    ##Many to Many Field has no on_delete
    #Django is going to create "through table" - Two differnt models with primary keys 
    ##promotions_products
    #Deletion is models.CASCADE 

    
# 100 Entries in Our DB 100 = Instance of Product Class
class Session(models.Model):
    pass
    # we do not use Intergeers for projects primarily
    # CUID - Collision Resistant ID - None colllision resistant for a SINGLE SYSTEM - CUID is supposed to humanly readable as possible
    # UUID - Unviersal Collision Resistant ID - Global Distrubted system that need uniquness across contients
    # A-Z, a-z, 0.9
    #password of 8 character
    # 8^52 
    #     id = models.CharField(primary_key=True, default=cuid.cuid, max_length=8)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid5, max_length=24, editable=False)
    
class Products(models.Model):

    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(null=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT) #models.CASCADE - IF WE DELETE A CATEOGRY IT WILL DIELETE ALL THE PRODUCTS ASSOICATED TO CATEGORY
    # Brand Parent - One side, #Products - Child Class
    # category = models.ForeignKey("Category", on_delete=models.PROTECT, default=1)
    
    def __str__(self): 
        return self.item

class Category(models.Model):
   
    name = models.CharField(max_length=255)
    metatag = models.CharField(max_length=255)
   
class Session(models.Model):
   pass
   
    
    
class Order(models.Model):
    
    PAYMENT_COMPLETED = "C"
    PAYMENT_DENIED = "D"
    PAYMENT_PENDING = "P"
        
    PAYMENT_STATUS = [
  
        (PAYMENT_COMPLETED, "Completed"),
        (PAYMENT_DENIED, "Denied"),
        (PAYMENT_PENDING, "Pending")
        
    ]
    
    
    order_number = models.PositiveIntegerField()
    time_of_order = models.DateTimeField()
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
    customer = models.ForeignKey(User, on_delete=models.CASCADE) #User = Parent, Orders = Children
    
class Order_Item(models.Model):
    # How many order items with the of product id are in the a single
    
    # product =  models.OneToOneField(Products)
    amount = models.PositiveIntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    


    
##5.8 --> 6 for float
##5.8 --> 5.8 for decimal
class Brand(models.Model):
    
    
    
    name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    ##Number of rating = 500
    ##average by adding all the rating of the users / number of rating = 4.27 ---> 4.3 (4.27 as decimal ), 4.55 --> 5, 4.6
    address = models.CharField(max_length=255)
    followers = models.PositiveBigIntegerField()
    description = models.TextField(max_length=255)
    logo = models.TextField(max_length=255)
   
    

class Reviews(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    product_rating = models.FloatField(max_length=255)
    date = models.DateField(auto_now=True)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user

# REPL - Read-Evaluate-Print-Loop