from django.db.models import Sum, F
from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from orders_app.filters import FilterUser, FilterDateLte, FilterDateGte
from orders_app.models import Order, Product, OrderProducts
from orders_app.serializers import OrderSerializer, ReportSerializer


class OrdersViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ReportsViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    queryset = OrderProducts.objects.all()
    filter_backends = [
        FilterUser,
        FilterDateLte,
        FilterDateGte,
    ]
    serializer_class = ReportSerializer

    def filter_queryset(self, queryset: 'QuerySet[OrderProducts]'):
        queryset = super(ReportsViewSet, self).filter_queryset(queryset)
        # adding extra info
        return queryset.values('product').annotate(
            total_quantity=Sum('quantity'),
            total_price=Sum(
                F('unit_price') * F('quantity'))
        ).order_by('-total_price')
