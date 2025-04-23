from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=10)


class ReceiptSerializer(serializers.Serializer):
        retailer = serializers.CharField()
        purchaseDate = serializers.DateField()
        purchaseTime = serializers.TimeField()
        items = ItemSerializer(many=True)
        total = serializers.DecimalField(decimal_places=2, max_digits=10)
