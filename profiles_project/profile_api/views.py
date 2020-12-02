from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from profile_api import serializers
from profile_api.models import UserProfile, ProfileFeedItem
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from profile_api.permissions import UpdateOwnProfile, UpdateOwnStatus
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Create your views here.

class HelloApiView(APIView):
    """Test api view"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """returns a list of apiview features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello', 'an_view':an_apiview})

    def post(self, request):
        """Create hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'Message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSets(viewsets.ViewSet):
    """hello API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a hello message"""

        a_viewset = [
            'Uses action (list, create, reteieve, update, partial_update)',
            'Automatically maps the urls using routers',
            'provide more functionality with less code',
        ]

        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """create a new heelo message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """handle getting an object by it's id"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """handle updating part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """handle removin an object"""
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """hanle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """handles creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileViewSet(viewsets.ModelViewSet):
    """Models creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = (UpdateOwnStatus, IsAuthenticated)
    # permission_classes = (UpdateOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """Sets the user profile to logged in user"""
        serializer.save(user_profile=self.request.user)
