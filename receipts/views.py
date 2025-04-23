from decimal import Decimal
from datetime import time
from math import ceil
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from receipts.models import Receipt
from receipts.serializers import ReceiptSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

receipt = Receipt()


class ProcessReceiptView(APIView):
    def calculate_alpha_numeric_chars(self, retailer):
        count = 0
        for char in retailer:
            if char.isalnum():
                count = count + 1
        return count

    def calculate_points(self, data):
        points = self.calculate_alpha_numeric_chars(data.get("retailer"))
        # add 50 points if total doesn't have any cents
        points = points + 50 if data.get("total") % 1 == 0 else points
        # add 25 points if total is a multiple of .25
        points = points + 25 if data.get("total") % Decimal("0.25") == 0 else points
        # add 5 points for every pair of 2 items
        points = points + (5 * len(data.get("items")) // 2)
        for item in data.get("items"):
            if len(item.get("shortDescription").strip()) % 3 == 0:
                price = item.get("price") * Decimal("0.2")
                points = points + ceil(price)
        # add 6 points if purchase date is odd
        points = points + 6 if data.get("purchaseDate").day % 2 == 1 else points
        # add 10 points if purchase time is between 2 and 4 pm
        points = points + 10 if time(14, 0) < data.get("purchaseTime") < time(16, 0) else points
        return points

    @swagger_auto_schema(
        request_body=ReceiptSerializer,
        responses={201: openapi.Response('Created', ReceiptSerializer)}
    )
    def post(self, request):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            points = self.calculate_points(data)
            receipt_id = receipt.save_receipt(points)
            return Response({"id": receipt_id}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetReceiptPointsView(APIView):
    def get(self, request, receipt_id):
        points = receipt.get_points(receipt_id)
        if points is not None:
            return Response({"points": points}, status=status.HTTP_200_OK)
        return Response({"error": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)
