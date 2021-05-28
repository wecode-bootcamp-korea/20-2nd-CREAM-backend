import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cream.settings")
django.setup()

from products.models import *

CSV_PATH_PRODUCTS = './cream.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    # image = "https://i.postimg.cc/TYppDGt9/shoes1.png"
    # for i in range(1, 26):
    #     ProductImage.objects.create(product_id=i, image_url=image)

    # for i in range(1, 26):
    #     for j in ["250", "260", "270", "280", "290"]:
    #         ProductOption.objects.create(product_id=i, size=j)

    for row in data_reader:
        # Brand.objects.create(name=row[0], logo_image=row[1])

        # brand_name = row[0]
        # brand_id = Brand.objects.get(name=brand_name).id
        # Collection.objects.create(name=row[1], brand_id=brand_id)

        # Product.objects.create(collection_id=row[0], english_name=row[1], korean_name=row[2], limited=row[3])