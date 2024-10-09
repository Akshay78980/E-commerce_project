from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
    


class ProductSerializer(serializers.ModelSerializer):

    category_details = CategorySerializer(source='category',read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','name','description','price','category','category_details']


    
