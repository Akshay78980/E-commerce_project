from django.shortcuts import render

from rest_framework.views import APIView
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Product, Category

# Create your views here.


class BaseAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



class GetProductsAPI(BaseAPIView):
    def get(self, request, id=None):
        products = Product.objects.all()
        if id is not None:
            try:
                product = Product.objects.get(id=id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Product.DoesNotExist as e:
                return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class CreateProductsAPI(BaseAPIView):
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            product = serializer.save()
            
            created_product = Product.objects.get(id=product.id)
            response_serializer = ProductSerializer(created_product)
            
            return Response({"message":"Product created succesfully.","data":response_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UpdateProductAPI(BaseAPIView):
    def put(self, request,id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product,data=request.data,partial=False)
            if serializer.is_valid():
                serializer.save()
                
                updated_product = Product.objects.get(id=id)
                res_serializer = ProductSerializer(updated_product)

                return Response({"product_detail":res_serializer.data,"message":"Product updated succesfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        


class DeleteProductAPI(BaseAPIView):
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response({"message":"Product deleted."}, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
    

# APIs for Category model

class CategoryListAPI(BaseAPIView):
    def get(self, request, id=None):
        if id:
            try:
                category = Category.objects.get(id=id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateAPI(BaseAPIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data['message'] = 'Category created successfully!'
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CategoryUpdateAPI(BaseAPIView):
    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)



class CategoryDeleteAPI(BaseAPIView):
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
