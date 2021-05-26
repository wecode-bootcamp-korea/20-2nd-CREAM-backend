from django.db import models

class Brand(models.Model):
    name       = models.CharField(max_length=200)
    logo_image = models.URLField()

    class Meta:
        db_table = "brands"

    def __str__(self):
        return self.name

class Collection(models.Model):
    name  = models.CharField(max_length=200)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)

    class Meta:
        db_table = "collections"

    def __str__(self):
        return self.name

class Product(models.Model):
    korean_name  = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    limited      = models.BooleanField(default=False)
    collection   = models.ForeignKey("Collection", on_delete=models.CASCADE)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.korean_name

class ProductImage(models.Model):
    product   = models.ForeignKey("Product", on_delete=models.CASCADE)
    image_url = models.URLField()

    class Meta:
        db_table = "product_images"

class ProductOption(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size    = models.CharField(max_length=45)

    class Meta:
        db_table = "product_options"