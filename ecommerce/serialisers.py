from rest_framework import serializers
from decimal import Decimal
from .models import Products, Category, Session, Address, User, Reviews
from time import time, time_ns



class CategorySerialiser(serializers.ModelSerializer):
    
    class Meta:
        fields = ['name', 'metatag']
    
    
    

class ReviewSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Reviews
        fields = ['user', 'title', 'product_rating', 'date']
    
    


class AddressSerialiser(serializers.Serializer):
    # Creatis a python dictionary
    # Internal Representation of Model
    # External Rpreseneation of Model 
    post_Code = serializers.CharField(max_length=255)
    door_No = serializers.IntegerField()
    
    
    # def validate(self, data):
    #       if data["email"] != data["confirm_email"]:
    #             print("Emails don't match!")
    #             return serializers.ValidationError("Emails don't match")
            
    #       return data 
    

class SessionSerialiser(serializers.ModelSerializer):
    class Meta:
        fields = ["access_token", "session_token", "session_time", "session_id"]
        
    measure_session_tile = serializers.SerializerMethodField(method_name="measure_time")
    
    
    def measure_time(self, obj):
       time_diff_in_secs =  time.time() - obj["session_time"]
       return time_diff_in_secs
    
    
    returning_token = serializers.SerializerMethodField(method_name="return_access_token")
    
    
    def return_access_token(self, obj):
        token = obj["access_token"]
        return token
    
    def create(self, validated_data):
        session = Session(**validated_data)
        session.time_stamp = time.time() #new key-value added to the dictionary
        session.save()
        return session
    
    returning_session = serializers.SerializerMethodField(method_name="return_session")
    
    def return_session(self, obj):
        sessionToken = obj["session_token"]
        return sessionToken
        
        # write our fields 
class BrandSerialiser(serializers.Serializer):
    
    name = serializers.CharField(max_length=255)
    rating = serializers.DecimalField(max_digits=4, decimal_places=2)
    description = serializers.CharField(max_length=255)
    logo = serializers.CharField(max_length=255)
    reviews = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    
    
   
class UserSerialiser(serializers.Serializer):
    
    id = serializers.IntegerField()
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=22)
    address = serializers.HyperlinkedRelatedField(queryset=Address.objects.all(), view_name="address_detail")
    
    address_id = serializers.StringRelatedField()

    
# seralizer vs seralizerModel
#serializer - Unmapped Serializer
#serialzerModel - Mapped Serializer - automatic validation logic and field generate

# class PracticeSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
#     class Meta: 
#         fields = ["id", "name", "price", "stock", "price"]
#         model = Products
#         #[{id, name, price},]


class MathOperations:
    
    calculated_value = 0
    
    @classmethod
    def add(self, val1, val2):
        return val1 + val2

calculate_values = MathOperations()    
calculate_values.add(20, 20)


class ProductSerialiser(serializers.Serializer):
   
    item = serializers.CharField(max_length=255, default="item")
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    description = serializers.CharField()
    stock = serializers.IntegerField()
    # category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
     # utility field
    price_with_vat = serializers.SerializerMethodField(method_name="calculate_vat")
    
    def calculate_vat(self, product):
        return product.price * Decimal(1.2)
    
    def current_stock_data(self, obj):
        request = self.context.get("request")
        if request and request.product.is_in_stock:
            return obj == request # Evaluate to false 
        return False
    
    #Conditional render different fields
    def data_representation(self, instance):
        # {name: Keyboard, product_id: 10, stock_amount: 30}
        rep = super().to_representation(instance)
        
        if self.context.get("seller_email"):
            rep["email"] = instance.email
            
        else:
            rep.pop("email", None)
        return rep

    



# class VatSerialiser(serializers.Serializer):
    
#     item = serializers.CharField(max_length=255, default="item")
#     price = serializers.DecimalField(max_digits=5, decimal_places=2)
#     description = serializers.CharField()
#     stock = serializers.IntegerField()
   
    
#     #PrimaryKeyRelatedField(queryset-model.object.all(_))
    
#     # utility field
#     price_with_vat = serializers.SerializerMethodField(method_name="calculate_vat")
    
#     def calculate_vat(self, product):
#         return product.price * Decimal(1.2)  
    
    
    

# class CategorySerialiser(serializers.Serializer):
    
#     name = serializers.CharField()


  