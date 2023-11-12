from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            new_stockProduct = StockProduct(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
            new_stockProduct.save()
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            if StockProduct.objects.filter(stock=stock, product=position['product']).count() == 0:
                new_stockProduct = StockProduct(
                    stock=stock,
                    product=position['product'],
                    quantity=position['quantity'],
                    price=position['price']
                )
                new_stockProduct.save()
            else:
                stockproducttoupdate = StockProduct.objects.get(stock=stock, product=position['product'])
                stockproducttoupdate.quantity = position['quantity']
                stockproducttoupdate.price = position['price']
                stockproducttoupdate.save()
        return stock
