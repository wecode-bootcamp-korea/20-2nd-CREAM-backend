from django.test import TestCase

from django.test     import TestCase
from django.test     import Client

from products.models import Collection, Product, ProductOption, ProductImage, Brand
from orders.models   import SellingInformation, BuyingInformation, Status, Order
from users.models    import User


class OrderTest(TestCase):
    def setUp(self):
        user1      = User.objects.create(id=1,social_login_id = "noogoo1982", nickname="누구쉰지", email="noogoo1982@gmail.com", point=0)
        user2      = User.objects.create(id=2,social_login_id = "noogoo1983", nickname="누구쒼지", email="noogoo1983@gmail.com", point=0)
        brand      = Brand.objects.create(name="나이키", logo_image="aa")
        collection = Collection.objects.create(name="조던조던조던", brand = brand)
        product    = Product.objects.create(id=1,korean_name = "조던", english_name="jordan", limited=True, collection = collection)
        
        product2   = Product.objects.create(id=2,korean_name = "조던2", english_name="jordan", limited=True, collection = collection)
        ProductImage.objects.create(product = product, image_url = "a")
        ProductImage.objects.create(product = product2, image_url = "a")
        
        status         = Status.objects.create(name="입찰대기")
        product_option = ProductOption.objects.create(product = product, size = "250")

        ProductOption.objects.create(product = product2, size="250")

        SellingInformation.objects.create(
            id             = 1,
            price          = 240000,
            status         = status,
            user           = user1,
            product_option = product_option)

        BuyingInformation.objects.create(
            id             = 1,
            price          = 200000,
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

    def test_order_buy_get_success(self):
        client   = Client()
        response = client.get('/orders/buy/1?size=250')

        self.assertEqual(response.json(),{
            "product_information" : {
                "korean_name"   : "조던",
                "english_name"  : "jordan",
                "image"         : "a",
                "selling_price" : "200000.0000",
                "selling_user"  : 1,
                "selling_id"    : 1,
                "buying_price"  : "240000.0000",
                "user_point"    : 0,
                "size"          : "250"
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_order_buy_get_success_null(self):
        client   = Client()
        response = client.get('/orders/buy/2?size=250')

        self.assertEqual(response.json(),{
            "product_information" : {
                "korean_name"   : "조던2",
                "english_name"  : "jordan",
                "image"         : "a",
                "selling_price" : None,
                "selling_user"  : None,
                "selling_id"    : None,
                "buying_price"  : None,
                "user_point"    : 0,
                "size"          : "250"
            }
        })
        self.assertEqual(response.status_code, 200)
