# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from Listings.models import Property
# from listings_api.serializers import ListingSerializer
#
#
# # Create your views here.
# class ListingsAllAPIView(APIView):
#     def get(self, request):
#         listings = Property.objects.all()
#         serializer = ListingSerializer(listings, many=True)
#         return Response({"Listings": serializer.data})

from rest_framework import viewsets
from Listings.models import Property
from listings_api.serializers import ListingSerializer
from listings_api.permissions import IsBrokerOwnerOrReadOnly

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsBrokerOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(broker=self.request.user)