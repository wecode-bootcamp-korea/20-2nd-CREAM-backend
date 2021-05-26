import json

from django.db.models.aggregates import Max, Min
from django.db.models            import Q
from django.http                 import JsonResponse
from django.views                import View

from products.models import Product, ProductOption, ProductImage
from orders.models   import SellingInformation, BuyingInformation, Status, Order


class ProductDetailView(View):
    def get(self, request, product_id):
        if Product.objects.filter(id = product_id).exists():
            product         = Product.objects.get(id = product_id)
            product_image   = product.productimage_set.all()
            product_options = ProductOption.objects.filter(product = product)
            bidding         = Status.objects.get(name="입찰대기")
            q               = Q(selling_information__product_option__product=product)

            option = [
                {
                    'size'       : product_option.size,
                    'buy_price'  : SellingInformation.objects.filter(product_option = product_option, status = bidding).aggregate(Min("price"))["price__min"],
                    "sell_price" : BuyingInformation.objects.filter(product_option = product_option, status = bidding).aggregate(Max("price"))["price__max"],
                    } 
                    for product_option in product_options
                    ]
            
            lately_order = None

            if Order.objects.filter(q).exists():
                lately_order = Order.objects.filter(q).order_by("create_at")[0].selling_information.price

            product_information = {
                "id"           : product.id,
                "english_name" : product.english_name,
                "korean_name"  : product.korean_name,
                "main_image"   : product_image[0].image_url,
                "sub_image"    : product_image[1].image_url,
                "option"       : option,
                'lately_order' : lately_order,
                }

            return JsonResponse({"product_information" : product_information}, status=200)
        
        return JsonResponse({"MESSAGE" : "NO_PRODUCT"}, status = 400)