import json
from django.http import response

from django.test     import TestCase, client
from django.test     import Client

from products.models import Collection, Product, ProductOption, ProductImage, Brand
from orders.models   import SellingInformation, BuyingInformation, Status, Order
from users.models    import User

class ProductListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Brand.objects.create(id=1, name="브랜드", logo_image="brand_logo_image")
        Collection.objects.create(id=1, name="컬렉션", brand_id=1)
        Product.objects.create(id=1,korean_name = "상품", english_name="Product", limited=True, collection_id=1)
        ProductImage.objects.create(id=1, product_id=1, image_url="prdocut_image_url")
        ProductOption.objects.create(id=1, product_id=1, size="250")

    def test_productlist_get_success(self):
        client   = Client()
        response = client.get('/products?collection_id=1')

        self.assertEqual(response.json(), {
            "result" : [
                [
                    {
                        "brand_information"    : {
                                                    "brand_id"       : 1,
                                                    "brand_name"     : "브랜드",
                                                    "brand_logo_url" : "brand_logo_image"
                        },
                        "collection_id"        : 1,
                        "collection_name"      : "컬렉션",
                        "product_id"           : 1,
                        "product_korean_name"  : "상품",
                        "product_english_name" : "Product",
                        "product_limited"      : True,
                        "product_main_image"   : "prdocut_image_url",
                        "product_options"      : [
                                                    {
                                                        "size"       : "250",
                                                        "buy_price"  : None,
                                                        "sell_price" : None
                                                    }
                                                ]

                    }
                ]
            ]
            }
        )
        self.assertEqual(response.status_code, 200)

class ProductTest(TestCase):
    def setUp(self):
        user1      = User.objects.create(social_login_id = "noogoo1982", nickname="누구쉰지", email="noogoo1982@gmail.com", point=0)
        user2      = User.objects.create(social_login_id = "noogoo1983", nickname="누구쒼지", email="noogoo1983@gmail.com", point=0)
        brand      = Brand.objects.create(name="나이키", logo_image="aa")
        collection = Collection.objects.create(id=1, name="조던조던조던", brand = brand)
        
        product    = Product.objects.create(id=1,korean_name = "조던", english_name="jordan", limited=True, collection = collection)      
        ProductImage.objects.create(product = product, image_url = "a")
        ProductImage.objects.create(product = product, image_url = "b")
        
        status         = Status.objects.create(name="입찰대기")
        product_option = ProductOption.objects.create(product = product, size = "250")

        SellingInformation.objects.create(
            id             = 1,
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
            id             = 1,
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

        Order.objects.create(
            id                  = 1,
            selling_information = SellingInformation.objects.get(id=1),
            buying_information  = BuyingInformation.objects.get(id=1)
        )

        product = Product.objects.create(id=2,korean_name = "조던2", english_name="jordan2", limited=True, collection = collection)
        ProductImage.objects.create(product = product, image_url = "a")
        product_option = ProductOption.objects.create(product = product, size = "250")

        SellingInformation.objects.create(
            price          = 240000,
            status         = status,
            user           = user1,
            product_option = product_option)

        product = Product.objects.create(id=3,korean_name = "조던3", english_name="jordan3", limited=True, collection = collection)
        ProductImage.objects.create(product = product, image_url = "a")
        product_option = ProductOption.objects.create(product = product, size = "250")

        SellingInformation.objects.create(
            price          = 340000,
            status         = status,
            user           = user1,
            product_option = product_option)

    def tearDown(self):
        Brand.objects.all().delete()
        Collection.objects.all().delete()
        Product.objects.all().delete()
        ProductOption.objects.all().delete()
        ProductImage.objects.all().delete()
        Status.objects.all().delete()
        SellingInformation.objects.all().delete()
        BuyingInformation.objects.all().delete()
        Order.objects.all().delete()

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
                "lately_order" : "240000.0000",
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_productdetail_get_no_product(self):
        client   = Client()
        response = client.get('/products/30')
        
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json(),{
            "MESSAGE" : "NO_PRODUCT"
        })

    def test_orderhistory_get_success(self):
        client   = Client()
        response = client.get('/products/1/order')

        self.assertEqual(response.json(),{
            "order_list" : [
                {
                    "order_id"   : 1,
                    "size"       : "250",
                    "price"      : "240000.0000",
                    "order_date" : "2021/06/02" 
                    }
            ]
        })

        self.assertEqual(response.status_code, 200)

    def test_orderhistory_get_no_product(self):
        client   = Client()
        response = client.get('/products/10/order')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json(),{
            "MESSAGE" : "NO_PRODUCT"
        })

    def test_biddingsell_get_success(self):
        client   = Client()
        response = client.get('/products/1/sellbidding')

        self.assertEqual(response.json(),{
            "selling_bidding" : [
                {
                    "size" : "250",
                    "price" : "240000.0000"
                    },
                    {"size" : "250",
                    "price" : "340000.0000"
                    }
            ]})

    def test_biddingsell_get_noproduct(self):
        client   = Client()
        response = client.get('/products/6/sellbidding')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json(),{
            "MESSAGE" : "NO_PRODUCT"
        })

    def test_collection_get_success(self):
        client   = Client()
        response = client.get('/products/1/1')

        self.assertEqual(response.json(), {
            "collection_product" : 
            [
                {
                    "english_name" : "jordan2",
                    "buy_price" : "240000.0000",
                    "main_image" : "a"
                    },
                    {
                        "english_name" : "jordan3",
                        "buy_price" : "340000.0000",
                        "main_image" : "a"
                        }
                        ]
                        })

        self.assertEqual(response.status_code, 200)

    def test_collection_get_no_product(self):
        client   = Client()
        response = client.get('/products/10/1')

        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.json(),{
            "MESSAGE" : "NO_PRODUCT"
        })

    def test_biddingbuy_get_success(self):
        client   = Client()
        response = client.get('/products/1/buybidding')

        self.assertEqual(response.json(),{
            "buying_bidding" : [
                {
                    "size" : "250",
                    "price" : "200000.0000"
                    },
                    {"size" : "250",
                    "price" : "190000.0000"
                    }
                    ]})

        self.assertEqual(response.status_code, 200)

    def test_biddingbuy_get_noproduct(self):
        client   = Client()
        response = client.get('/products/6/buybidding')

        self.assertEqual(response.status_code, 400)