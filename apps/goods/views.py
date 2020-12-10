from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics


from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .models import Goods, GoodsCategory, Banner

# class GoodsListView(APIView):
#     '''商品列表'''
#     def get(self,request,format=None):
#         goods = Goods.objects.all()
#         goods_serializer = GoodsSerializer(goods,many=True)
#         return Response(goods_serializer.data)


# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     '''商品列表页'''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

from rest_framework.pagination import PageNumberPagination

class GoodsPagination(PageNumberPagination):
    '''商品列表自定义分页'''
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100

#
# class GoodsListView(generics.ListAPIView):
#     '''商品列表页'''
#     pagination_class = GoodsPagination # 分页
#     # 修改路由后必须要定义一个默认的排序，否则会报错
#     queryset = Goods.objects.all().order_by('id')
#     serializer_class = GoodsSerializer

from .filter import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters

# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''商品列表页'''
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''

    # 这里必须要定义一个默认的排序，否则会报错
    # queryset = Goods.objects.all().order_by('id')
    queryset = Goods.objects.all()
    # 分页
    pagination_class = GoodsPagination
    # 序列化
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # drf搜索，=name表示精确搜索，也可以使用各种正则表达式
    # search_fields = ('=name','goods_brief')
    search_fields = ('name','goods_brief','goods_desc')
    # 排序
    # ordering_fields = ('sold_num','add_time')
    ordering_fields = ('sold_num','shop_price')

    # 商品点击数 + 1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    '''
    list:
        商品分类列表数据
        要想获取某一个商品的详情的时候，继承 mixins.RetrieveModelMixin  就可以了品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''首页轮播图'''
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)







