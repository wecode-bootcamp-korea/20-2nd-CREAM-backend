import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Min, Max, Q

from orders.models   import BuyingInformation, SellingInformation, Status, Order
from products.models import ProductImage, ProductOption, Product
from users.models    import User
from users.utils     import login_confirm

class BuyView(View):
    @login_confirm
    def get(self, request, product_id):
        user           = request.user
        size           = request.GET.get("size", None)
        status         = Status.objects.get(name = "입찰대기")
        product        = Product.objects.prefetch_related("productimage_set", "productoption_set").get(id = product_id)
        product_option = product.productoption_set.get(size=size)
        selling        = SellingInformation.objects.filter(Q(product_option = product_option, status = status))

        buying_price   = selling.aggregate(Min("price"))["price__min"]
        selling_user   = selling.filter(price = buying_price).order_by("-create_at")[0].user.id if selling.exists() else None
        selling_id     = selling.filter(price = buying_price).order_by("-create_at")[0].id if selling.exists() else None

        selling_price  = BuyingInformation.objects.filter(product_option = product_option, status = status).aggregate(Max("price"))["price__max"]\
                         if BuyingInformation.objects.filter(product_option = product_option, status = status).exists() else None

        product_information = {
            "korean_name"   : product.korean_name,
            "english_name"  : product.english_name,
            "image"         : product.productimage_set.all()[0].image_url,
            "selling_price" : selling_price,
            "selling_user"  : selling_user,
            "selling_id"    : selling_id,
            "buying_price"  : buying_price,
            "user_point"    : user.point,
            "size"          : size
        }
        return JsonResponse({"product_information" : product_information}, status=200)

    @login_confirm
    def post(self, request, product_id):
        data    = json.loads(request.body)
        buy     = request.GET.get("buy", None)
        user    = request.user
        product = Product.objects.get(id = product_id)

        
        if buy == "buying":
            if user.point < SellingInformation.objects.get(id = data["selling_id"]).price:
                return JsonResponse({"MESSAGE" : "INSUFFICIENT_POINT"}, status = 400)

            status              = Status.objects.get(name="거래완료")
            sell_user           = User.objects.get(id = data["sell_user"])
            sell_product        = SellingInformation.objects.get(id = data["selling_id"])
            sell_product.status = status
            sell_product.save()

            buy_product  = BuyingInformation.objects.create(
                user           = user,
                status         = status,
                price          = sell_product.price,
                product_option = sell_product.product_option
                )

            Order.objects.create(selling_information = sell_product, buying_information = buy_product)

            user.point = user.point - int(sell_product.price)
            user.save()

            sell_user.point = sell_user.point + int(sell_product.price)
            sell_user.save()

            return JsonResponse({"MESSAGE" : "ORDER_SUCCESS"}, status=201)

        if user.point < int(data["price"]):
            return JsonResponse({"MESSAGE" : "INSUFFICIENT_POINT"}, status=400)

        status         = Status.objects.get(name="입찰대기")
        product_option = ProductOption.objects.get(product = product, size=data["size"])

        BuyingInformation.objects.create(
            user           = user,
            price          = data["price"],
            status         = status,
            product_option = product_option
            )           
        return JsonResponse({"MESSAGE" : "BIDDING_SUCCESS"}, status=201)

class SellView(View):
    @login_confirm
    def get(self, request, product_id):
        user           = request.user
        size           = request.GET.get("size", None)
        status         = Status.objects.get(name = "입찰대기")
        product        = Product.objects.prefetch_related('productimage_set', 'productoption_set').get(id=product_id)
        product_option = product.productoption_set.get(size=size)
        buying         = BuyingInformation.objects.filter(Q(product_option = product_option, status = status))
        
        selling_price  = buying.aggregate(Max("price"))["price__max"] if buying.exists() else None
        buying_user    = buying.filter(price = selling_price).order_by("-create_at")[0].user.id if buying.exists() else None
        buying_id      = buying.filter(price = selling_price).order_by("-create_at")[0].id if buying.exists() else None
        
        buying_price   = SellingInformation.objects.filter(product_option = product_option, status = status).aggregate(Min("price"))["price__min"]\
                         if SellingInformation.objects.filter(product_option = product_option, status = status).exists() else None
            
        product_information = {
            "korean_name"   : product.korean_name,
            "english_name"  : product.english_name,
            "image"         : product.productimage_set.all()[0].image_url,
            "selling_price" : selling_price,
            "buying_price"  : buying_price,
            "buying_user"   : buying_user,
            "buying_id"     : buying_id,
            "user_point"    : user.point,
            "size"          : size
        }

        return JsonResponse({"product_information" : product_information}, status=200)
