from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, F, Func, Value, QuerySet

# Create your views here.

from ecommerce.models import User, Address, Products, Order, Order_Item, Category, Reviews
from ecommerce.serialisers import AddressSerialiser, ProductSerialiser, CategorySerialiser, ReviewSerialiser
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED
from .serialisers import UserSerialiser
import requests
from django_filters.rest_framework import DjangoFilterBackend
# http://locahost:8000/ecommerce/users?offset=10&limit=10
#limit - how many objects to display
#offset = how many items to start counting from after the last set of pagnigated data
## 10, 0 + 10, 10 -20,
class AddressMixin(ListModelMixin):
    pass


#SRP - Single Responsiblity Principle
#Classes, Modules, Functions, Com

class DoesNotExist(BaseException):
    pass


def create_review(request):
    requests.post("www.localhost:8000/create/reviews", data=request.data)
    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialiser
    filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter
    
    # def get_queryset(self):
    #     queryset = self.get_queryset()
        
    #     user = self.request.query_params.get("user")
        
    #     #Filter
    #     if user:
    #         queryset = queryset.filter(user__icontains=user)
        
    #     return queryset
    

class ReviewViewSet(ModelViewSet):
    # www.localhost:8000/create/reviews

    queryset = Reviews.objects.all()
    serializer_class = ReviewSerialiser
    
    
    def get(self, request, *args, **kwargs):
        queryset = Reviews.objects.all()
        review = self.get_serializer(queryset, many=True)
        
        return Response(review.data, status=200)
  
class UserViewSet(ModelViewSet):
     queryset = User.objects.select_related("address").all()
     serializer_class = UserSerialiser
     pagination_class = PageNumberPagination()
    
     
    #  def get_serializer_context(self, request):
    #      return {"request": request}
    
    
    
     def list(self, request):
         queryset = self.get_queryset()
         user = UserSerialiser(queryset, many=True)
         return Response(user.data, status=200) 


     def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.id > 0:
            return Response({"error": "User cannot be deleted"})
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
     def update(self, req, id):
        user_profile = User.objects.get(pk=id)
        serialiser = UserSerialiser(user_profile, data=req.data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        return Response(serialiser.data)
    
    
    

    
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerialiser
    queryset = Products.objects.all()
    lookup_field = "pk"
    # pagination_class = PageNumberPagination # Pagingation for this class only 


#queryset = products.objects
    def retrieve(self, request, pk):
        user_lookup = pk
        try: 
            item = self.queryset.get(pk=pk)
        except:
            raise NotFound(detail=f"Item with id of {user_lookup} does not exist")
            
    
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=HTTP_200_OK)
            
            
            
            
     
    
    def list(self, request, *args, **kwargs):
       queryset = self.filter_queryset(self.get_queryset()) 
       
       # pagnigation 
       # search params criteria
       filter_req = request.query_params.get("search", None)
       if filter_req:
           queryset = self.queryset.filter(
               Q(colour__icontains=filter_req)
           )
           
       # Pagination
        #Throughout - Is how many request can be handled per second r/s req/s request/second
        #Latency - Speed of at whcih a response is returned from a request
       page = self.paginate_queryset(queryset)
       if page is not None:
           serialiser = self.get_serializer(page, many=True)
           return self.get_paginated_response(serialiser.data)
          
       serialiser = self.get_serializer(queryset, many=True)
       return Response(serialiser.data)
       
    #Without method = just the queryset
    #With method = conditional logic before queryset

    def create(self, request):
        serialiser = self.serializer_class(data=request.data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        
        return Response(serialiser.data, status=HTTP_201_CREATED)
    
    
    #list = get requests for all data or a filtered data set

    
    # @action(detail=False, method=["get"], url_path="retreive_product")
    def get(self, request, *args, **kwargs):
        

        if instance.is_admin and request.user.is_admin:
            raise PermissionDenied("You do have the permissions to access this area!")
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        data["formatted_date"] = instance.created_at.strftime("%Y-%m-%d %H:%M:%s")
        
        return Response(data)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serialiser = self.serializer_class(instance, data=request.data)
        serialiser.is_valid(raise_exception=True)
        
        self.perform_update(serialiser)
        
        return Response(serialiser.data)
        
    def perform_update(self, serialiser):
        serialiser.save()
    #retreive = get a single data obkect by the pricvate
    # def retrieve(self, request, pk):
        
    #     serialiser = self.get_serializer_class
    #     print("This the serialiser object", serialiser)
    #     product = get_object_or_404(serialiser, pk)
    #     print(product)
    #     return Response("This it the product object", product)
        
        
    
     
        
         
    
    
        
       
    
        
@api_view()
def address_detail(request, pk): 
    address = get_object_or_404(Address, pk=pk)
    serialiser = AddressSerialiser(address)
    return Response(serialiser.data)      
#N + 1 - For each relation connected to the model you are querying you will have an addition query
##e.g. user.objects.all() = 1000 users 
### for user it will do one additional query per address

##select_related = one to one relationships, foreign keys where the id the focus on a single foreign key
#prefetch_related - many to many relationships, reverse foreign key 
#multiple related objects
    

class HandleUserAuth(APIView):
    def post(self, req):
        queryset = User.objects.filter(Q(username=req.username) & Q(password=req.password))


        
# request handler
def send_message(req):
    return HttpResponse("Message Sent")


def vereification(req):
    return HttpResponse("Verification Submited")


def welcome(req):
    return HttpResponse("Welcome To Ashan's Page")


def tester(req, data):
    
    if isinstance(data, str):
        users_schema_object = User.objects

        filtered = users_schema_object.filter(username__istartswith="P")

        user_qs = users_schema_object.count()
        name = "James"

        # [A-Z^a-z^0-9]

        get_by_id = users_schema_object.get(pk=1)

        # transformed_query = list(user)
        # If we return more one item the we return QuerySet Object
        # QuerySET ---> list, loop over
        return render(
            req,
            "test.html",
            {"name": "Philip", "user_count": user_qs, "user_data": filtered},
        )


def get_users(req):
    # $desc $asc
    # Q - Query Object - Conditional and Multiple Checks
    # F - Filter Object - Comparing Field For Fields
    # return function(*args, **kwargs)

    users = User.objects
    users_value = users.values("username").distinct()
    count = users.count()
    return render(req, "usertest.html", {"users": users_value, "count": count})


def create_test(request):
    user = User.objects

    # Aggregate
    aggregate = user.aggregate()
    # Limting Data
    user_data = user.values("username").distinct()[:20]

    return render(request, "userinfo.html", {"user_info_data": list(user_data)})


def randomtest(request):
    post = Address.objects

    post_data = post.values("post_Code").distinct()[:20]

    return render(request, "userpost.html", {"user_post_data": list(post_data)})


@api_view()
# Seralize Model - Model instance is converted in a dictionaryh
def api_caller(request):
    return Response("This is a test")
    # http Response
    # HTTP Request
    # REST
    # R - Resources - Data
    # S - Stateless Communcation
    # HTTP Methods
    # Resource Formats
    #


@api_view()
def uerser_info(request):
    users = User.objects.all()
    return Response("users", status=200)


# http://localhost:9000/api/postcode/<id>
@api_view()
def postcode(request, address):
    # 1. Query based on the door_no
    user_address = User.objects.get(door_No=address)
    # 2. Get the serialiser to receive the query object /// Object => JSON object
    serialiser = AddressSerialiser(user_address)
    # 3. Provide the seralised version of data to the user
    return Response(serialiser._data)


@api_view()
def get_user_by_id(request, id):

    users = User.objects.get(pk=id)
    return Response(users)


@api_view()
def get_user(request, id):
    user = get_object_or_404(User, pk=id)
    serializer = UserSerialiser(user)
    return Response(serializer.data)
    # try:
    #     user = User.objects.get(pk=id)
    #     serializer = UserSerialiser(user)
    #     return Response(serializer.data)

    # #Does Not Exist = 404
    # except User.DoesNotExist as error:
    #     print(error)
    #     return Response(status=HTTP_404_NOT_FOUND)


@api_view()
def get_all_users(request):

    # ID Range 0 and 100
    # Query users that that an id between 1 to 100 and startwith =";"
    user = User.objects.filter(pk__lte=20)
    queryset = get_object_or_404(user)
    serializer = UserSerialiser(queryset, many=True)
    
    # xargs = one variable that can stre a varying number of values
    return Response(serializer.data)



@api_view()
def get_vat_prices(request, id):
    
   
    product = get_object_or_404(Products, pk=id)
    serialiser = ProductSerialiser(product)
    return Response(serialiser.data)



@api_view()
def get_all_products(request):
    
    queryset = Products.objects.all()
    serialiser = ProductSerialiser(queryset, many=True)
    return Response(serialiser.data)



@api_view()
def products_starting_with_a(request):
    
    letterfilter = Products.objects.filter(item__istartswith="a")
    serialiser = ProductSerialiser(letterfilter, many=True)
    return Response(serialiser.data)

@api_view
def create_order(request):
    
    global order_number
    order = Order.objects.create()
    order_number = order.pk
    return Response(order)
    
    
def send_email(message):
    

    @api_view()
    def check_order_state(request):
        order = Order.objects.get(pk=order_number)
        if(order.status == "P"):
            pass
        if(order.status == "C"):
            pass
        if(order.status == "D"):
            pass
        
    
@api_view(http_method_names=["GET"])
def get_item_by_category(request, category):
    
    queryset = Products.objects.filter(category__name=category)
    sereialiser = ProductSerialiser(queryset, many=True)
    
    return Response(sereialiser.data)


@api_view()
def get_all_product(request):
    
    #Select related before all
    ## Create JOIN in our SQL Query Statement
    #OneToOne and OneToMany
    #ManyToMany = prefetch_related()
    queryset = Products.objects.select_related("category").all()
    serialiser = ProductSerialiser(queryset, many=True)    
    
    return Response(serialiser.data)

# @api_view(["GET", "POST"])
# def get_user_by_address_id(request, address_id):
#     # GET LOGIC
#     request.get
    
#     #POST LOGIC
#     if request.post: 


##1. Find address by door_No

@api_view(["GET", "POST"])
def get_address_by_door_no(request, _door_No):
    
    if request.method == "GET":
        door_no_cov = int(_door_No)
 
    
        queryset = Address.objects.filter(Q(door_No=door_no_cov) & Q(post_Code__isnull=True))
        serialiser = AddressSerialiser(queryset, many=True)
    
    
        return Response(serialiser.data)
    elif request.method == "POST":
        # 
        serialiser = AddressSerialiser(data=request.data)
        if serialiser.is_valid(raise_exception=True):
            serialiser.validated_data
            return Response("OK", status=HTTP_200_OK)
        else:
            return Response(serialiser.errors, status=HTTP_400_BAD_REQUEST)

# api_view(["POST"])
# def reduce_stock(product_id):
    
#     Products.objects.filter(pk=product_id).update(stock=F("stock") -  1)

# def format_data():
#     captailsed_data = Address.objects.annotate(road_name=Func(F("road_name"), function="UPPER"))
    

##2. Find address by road_name

@api_view()
def  find_address_by_road(request, user_road_name):
    
    queryset = Address.objects.filter(road_name=user_road_name)
    serialiser = AddressSerialiser(queryset, many=True)
    
    return Response(serialiser.data)
    

##3. Find address by id

@api_view(["GET", "POST", "DELETE", "PUT"])
def find_address_by_id(request, id):
   address = get_object_or_404(Address, pk=id) # Return an address object based on it's ID

   if request.method == "GET": 
       serialiser = AddressSerialiser(address)
       return Response(serialiser.data)
   
   
   

   elif request.method == "PUT":
       update_field = AddressSerialiser(address, data=request.data)
       update_field.is_valid(raise_exception=True)
       update_field.save()
       
    #    update_field.update(request.data, update_field.validated_data)
       
    #    update_field.save()
       
       return Response(update_field.data, status=200)
       
       
											
           

   elif request.method == "POST":

        serialiser = AddressSerialiser(data=request.data)
        serialiser.is_valid(raise_exception=True)
   
        # requests.post("endpoint of backserver or cloud archechure",  serialiser)
        serialiser.save()
        return Response("Address added", status=201)

   elif request.method =="DELETE":
       address = get_object_or_404(Address, pk=id)
       
       deleted_address = address.delete()
       if not deleted_address:
           return Response({"Address cannot be deleted"},status=HTTP_405_METHOD_NOT_ALLOWED)
       return Response("Data has been successfully removed", status=HTTP_204_NO_CONTENT)
   
       
 
#    return Response("Succesfully added a new address", status=201)
        
        

##4. Find user by address id
##5. find a user id by address data i