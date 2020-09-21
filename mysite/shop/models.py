from django.db import models
'''
class Item(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
'''

class myProduct(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to='shop/images', default="")
    price = models.IntegerField(blank=True, default='', null=True)
    date = models.DateField(blank=True, default='', null=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_email = models.CharField(max_length=50)
    c_phone = models.CharField(max_length=12)
    c_query = models.CharField(max_length=500)

    def __str__(self):
        return self.c_name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    o_name = models.CharField(max_length=100)
    o_email = models.CharField(max_length=50)
    o_address = models.CharField(max_length=500)
    o_city = models.CharField(max_length=50)
    o_state = models.CharField(max_length=50)
    o_zip = models.CharField(max_length=10)
    o_phone = models.CharField(max_length=12)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.order_id