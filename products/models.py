from django.db import models

from cryptography.fernet import Fernet

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class EncryptedPriceField(models.CharField):
    _encryption_key = None

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if not EncryptedPriceField._encryption_key:
            EncryptedPriceField._encryption_key = Fernet.generate_key()
        self.fernet = Fernet(EncryptedPriceField._encryption_key)

    def pre_save(self,instance, add):
        field_val = getattr(instance,self.name)
        if field_val:
            encrypted_value = self.fernet.encrypt(field_val.encode())
            setattr(instance,self.name, encrypted_value)
        return field_val
    
    def get_field_value(self, instance):
        encrypted_value = super().get_field_value(instance)
        if encrypted_value:
            decrypted_value = self.fernet.decrypt(encrypted_value.encode()).decode()
            return decrypted_value
        return True



class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    price = EncryptedPriceField(max_length=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name