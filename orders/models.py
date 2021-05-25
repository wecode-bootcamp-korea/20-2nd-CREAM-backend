from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class SellingInformation(models.Model):
    price          = models.DecimalField(max_digits=None, decimal_places=4)
    status         = models.ForeignKey("Status", models.SET_NULL, null=True)
    product_option = models.ForeignKey("products.ProductOption", on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    create_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "selling_informations"

class BuyingInformation(models.Model):
    price          = models.DecimalField(max_digits=None, decimal_places=4)
    status         = models.ForeignKey("Status", models.SET_NULL, null=True)
    product_option = models.ForeignKey("products.ProductOption", on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    create_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "buying_informations"

class Order(models.Model):
    selling_information = models.ForeignKey('SellingInformation', on_delete=models.CASCADE)
    buying_information  = models.ForeignKey('BuyingInformation', on_delete=models.CASCADE)
    create_at           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"