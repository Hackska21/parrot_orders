from abc import ABC

from rest_framework import serializers

from orders_app.models import Order, Product, OrderProducts


class ProductsSerializer(serializers.Serializer):
    product_name = serializers.CharField(source='product.name')
    unit_price = serializers.DecimalField(decimal_places=2, max_digits=9)
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductsSerializer(required=True, many=True, source='orderproducts_set')

    def create(self, validated_data):
        # print(validated_data)
        products = validated_data.pop('orderproducts_set')
        order = super(OrderSerializer, self).create(validated_data)
        
        # create products
        for product in products:
            product_name = product.pop('product').get('name')
            product_instance, _ = Product.objects.get_or_create(
                name=product_name
            )
            OrderProducts.objects.create(
                product=product_instance,
                **product,
                order=order
            )
        return order
            

    class Meta:
        model = Order
        fields = (
            'created_by',
            'customer_name',
            'price', #
            'created',
            'products'
        )
        read_only_fields = (
            'created',
        )


class ReportSerializer(serializers.Serializer):
    product = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=9, decimal_places=2)
