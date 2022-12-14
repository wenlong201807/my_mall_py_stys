from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from meiduo_admin.home import home_views
from meiduo_admin.user import user_views
from meiduo_admin.sku import sku_views
from meiduo_admin.views import specs, images, skus, orders, permissions, group, admin, spus, options

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),  # 内部对 用户名和密码做了校验
    # 首页
    url(r'^statistical/total_count/$', home_views.UserTotalCountView.as_view()),
    url(r'^statistical/day_active/$', home_views.UserDayActiveView.as_view()),
    url(r'^statistical/day_increment/$', home_views.UserDayIncrementView.as_view()),
    url(r'^statistical/day_orders/$', home_views.UserDayOrdersView.as_view()),
    url(r'^statistical/month_increment/$', home_views.UserMonthIncrementView.as_view()),
    url(r'^statistical/goods_day_views/$', home_views.GoodCategoryDayView.as_view()),
    # 用户管理
    url(r'^users/$', user_views.UserView.as_view()),

    # sku 管理 /categories 对应页面位置: sku管理 -> 添加 -> 分类下拉框
    # url(r'^skus/categories/$', sku_views.SKUCategoryView.as_view()),

    # goods/simple/  对应页面位置: sku管理 -> 添加 -> spu下拉框
    # url(r'^goods/simple/$', sku_views.GoodSimpleView.as_view()),
    # ------------规格路由表-----------两种方式都可以实现
    url(r'^goods/simple/$', specs.SpecsView.as_view({'get': 'simple'})),
    url(r'^goods/specs/simple/$', options.OptionSimple.as_view()),
    # ------------图片路由————————————
    url(r'^skus/simple/$', images.ImagesView.as_view({'get': 'simple'})),

    # ------------sku路由————————————
    # 在 SKUVIew 视图集内 定义的方法 specs 请求方法 get
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SKUVIew.as_view({'get': 'specs'})),
    # url(r'^goods/brands/simple/$', spus.SPUGoodsView.as_view({'get': 'brand'})),
    # url(r'^goods/channel/categories/$', spus.SPUGoodsView.as_view({'get': 'channel'})),
    # url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.SPUGoodsView.as_view({'get': 'channels'})),

    url(r'^goods/brands/simple/$', spus.SPUGoodsView.as_view({'get': 'brand'})),
    url(r'^goods/channel/categories/$', spus.SPUGoodsView.as_view({'get': 'channel'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.SPUGoodsView.as_view({'get': 'channels'})),

    # goods/3/specs/  对应页面位置: sku管理 -> 添加 -> spu下拉框 内容切换后，要调用此接口。
    # 获取子级选项(屏幕尺寸、颜色、版本) 选项类型个数动态化 及其选项列表
    # url(r'^goods/(?P<spu_id>\d+)/specs/$', sku_views.GoodSpecsView.as_view()),

    # --------权限路由--------
    url(r'^permission/content_types/$', permissions.PermissionsView.as_view({'get': 'content_type'})),

    url(r'^permission/simple/$', group.GroupView.as_view({'get': 'simple'})),

    url(r'^permission/groups/simple/$', admin.AdminView.as_view({'get': 'simple'})),

]

# ----------规格表路由------
router = DefaultRouter()
router.register('goods/specs', specs.SpecsView, basename='specs')
urlpatterns += router.urls

# -------图片表路由------
router = DefaultRouter()
router.register('skus/images', images.ImagesView, basename='images')
urlpatterns += router.urls

# 1, skus 对应页面位置: 左侧菜单 -> 商品管理 -> sku管理
router = DefaultRouter()
router.register("skus", skus.SKUVIew, basename="skus")
# router.register("skus", sku_views.SKUModelViewSet, basename="skus")
urlpatterns += router.urls

# --------订单路由--------
router = DefaultRouter()
router.register('orders', orders.OrderView, basename='orders')
urlpatterns += router.urls

# --------权限路由--------
router = DefaultRouter()
router.register('permission/perms', permissions.PermissionsView, basename='perms')
urlpatterns += router.urls

# --------分组路由--------
router = DefaultRouter()
router.register('permission/groups', group.GroupView, basename='groups')
urlpatterns += router.urls

# --------管理员路由--------
router = DefaultRouter()
router.register('permission/admins', admin.AdminView, basename='admin')
# print(router.urls)
urlpatterns += router.urls

router = DefaultRouter()
router.register('specs/options', options.OptionsView, basename='options')
# print(router.urls)
urlpatterns += router.urls

# --------spus路由--------
router = DefaultRouter()
router.register('goods', spus.SPUGoodsView, basename='spus')
# print(router.urls)
urlpatterns += router.urls
