from django.urls import path, include
from rest_framework import routers

# Create a router to generate automatically all paths on de viewset
from orders_app.views import OrdersViewSet, ReportsViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrdersViewSet)
router.register(r'reports', ReportsViewSet)

path('', include(router.urls)),

urlpatterns = [
    # Using include to maintain flexibility to change anytime the path
    path('', include(router.urls)),
]
