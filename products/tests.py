import json

from .models       import Collection, Product, ProductOption, ProductImage, Brand
from orders.models import SellingInformation, BuyingInformation, Status, Order
from users.models  import User
from django.test   import TestCase
from django.test   import Client

class ProductTest(TestCase):
    def setUp(self):
        user1      = User.objects.create(social_login_id = "noogoo1982", nickname="누구쉰지", email="noogoo1982@gmail.com", point=0)
        user2      = User.objects.create(social_login_id = "noogoo1983", nickname="누구쒼지", email="noogoo1983@gmail.com", point=0)
        brand      = Brand.objects.create(name="나이키", logo_image="aa")
        collection = Collection.objects.create(name="조던조던조던", brand = brand)
        product    = Product.objects.create(id=1,korean_name = "조던", english_name="jordan", limited=True, collection = collection)
        
        ProductImage.objects.create(product = product, image_url = "a")
        ProductImage.objects.create(product = product, image_url = "b")
        
        status         = Status.objects.create(name="입찰대기")
        product_option = ProductOption.objects.create(product = product, size = "250")

        SellingInformation.objects.create(
            price          = 240000,
            status         = status,
            user           = user1,
            product_option = product_option)
        
        SellingInformation.objects.create(
            price          = 340000,
            status         = status,
            user           = user1,
            product_option = product_option
        )

        BuyingInformation.objects.create(
            price          = 200000,
            status         = status,
            user           = user2,
            product_option = product_option
        )

        BuyingInformation.objects.create(
            price          = 190000,
            status         = status,
            user           = user2,
            product_option = product_option
        )

    def tearDown(self):
        Brand.objects.all().delete()
        Collection.objects.all().delete()
        Product.objects.all().delete()
        ProductOption.objects.all().delete()
        ProductImage.objects.all().delete()
        Status.objects.all().delete()
        SellingInformation.objects.all().delete()
        BuyingInformation.objects.all().delete()

    def test_productdetail_get_success(self):
        client   = Client()
        response = client.get('/products/1')

        self.assertEqual(response.json(),{
            "product_information" : {
                "id"           : 1,
                "english_name" : "jordan",
                "korean_name"  : "조던",
                "main_image"   : "a",
                "sub_image"    : "b",
                "option" : [
                    {
                        "size"       : "250",
                        "buy_price"  : "240000.0000",
                        "sell_price" : "200000.0000"
                    }
                ],
                "lately_order" : None,
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_productdetail_get_no_product(self):
        client   = Client()
        response = client.get('/products/2')
        
        self.assertEqual(response.status_code, 400)