import json

from django.db.models.aggregates import Max, Min
from django.db.models            import Q
from django.http                 import JsonResponse
from django.views                import View

from products.models             import Product, ProductOption
from orders.models               import SellingInformation, BuyingInformation, Status, Order

class ProductListView(View):
    def get(self, request):
        brand_id      = request.GET.getlist('brand_id', None)         # 브랜드별 상품 리스트
        collection_id = request.GET.getlist('collection_id', None)    # 컬렉션별 상품 리스트
        size          = request.GET.getlist('size', None)             # 필터링 조건1 - 사이즈
        colors        = request.GET.getlist('color', None)            # 필터링 조건2 - 색상 (상품명 안에 포함되어 있음)
        limited       = request.GET.get('limited', None)              # 필터링 조건3 - 한정판 유무
        search        = request.GET.get('search', None)               # 검색 - 상품명 기준

        q = Q()

        if brand_id:
            q.add(Q(collection__brand_id__in=brand_id), q.AND)
        
        if collection_id:
            q.add(Q(collection_id__in=collection_id), q.AND)

        if colors:
            q_coler = Q()
            for color in colors:
                q_coler.add(Q(english_name__contains=color), q.OR)
            q.add(q_coler, q.AND)
        
        if limited:
            q.add(Q(limited=limited), q.AND)
        
        if search:
            search = (search.lower()).capitalize()
            q.add(Q(korean_name__contains=search) | Q(english_name__contains=search), q.AND)

        products = Product.objects.select_related('collection', 'collection__brand').prefetch_related(
            'productoption_set',
            'productoption_set__sellinginformation_set',
            'productoption_set__buyinginformation_set'
        ).filter(q).distinct()

        total_result = []

        for product in products:
            q_size = Q()
            if size:
                q_size.add(Q(size__in=size), q.AND)
            
            result = [
                {
                    "brand_information"    : {
                                                "brand_id"       : product.collection.brand.id,
                                                "brand_name"     : product.collection.brand.name,
                                                "brand_logo_url" : product.collection.brand.logo_image
                    },
                    "collection_id"        : product.collection.id,
                    "collection_name"      : product.collection.name,
                    "product_id"           : product.id,
                    "product_korean_name"  : product.korean_name,
                    "product_english_name" : product.english_name,
                    "product_limited"      : product.limited,
                    "product_main_image"   : product.productimage_set.all()[0].image_url,
                    "product_options"      : [
                                                {
                                                    "size"       : option.size,
                                                    "buy_price"  : option.sellinginformation_set.filter(product_option_id=option.id).all().order_by('price')[0].price if option.sellinginformation_set.filter(product_option_id=option.id).exists() else None,
                                                    "sell_price" : option.buyinginformation_set.filter(product_option_id=option.id).all().order_by('-price')[0].price if option.buyinginformation_set.filter(product_option_id=option.id).exists() else None
                                                } for option in product.productoption_set.filter(q_size)
                                            ]

                }
            ]
            
            total_result.append(result)
        
        return JsonResponse({'result': total_result}, status=200)
        
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