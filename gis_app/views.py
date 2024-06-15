from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterUserSerializer, LoginUserSerializer, LocationSerializer, BoundarySerializer
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Location, Boundary
from django.contrib.gis.geos import Point, Polygon
import json
from rest_framework.permissions import IsAuthenticated


class RegisterUserView(APIView):
    """
    API view to register a new user.

    POST:
    Registers a new user with a username, email, and password.
    Returns the user's data on success.
    """

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    API view to log in a user.

    POST:
    Authenticates a user with a username and password.
    Returns access and refresh tokens on success.
    """

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
            return Response({"Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationListCreateView(APIView):
    """
    API view to list and create locations.

    GET:
    Returns a list of all locations.

    POST:
    Creates a new location with name, description, and coordinates.
    Returns the created location's data on success.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        location_obj = Location.objects.all()
        serializer = LocationSerializer(location_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationUpdateRetrieveDeleteView(APIView):
    """
    API view to retrieve, update, and delete a location by its ID.

    GET:
    Returns the data of the specified location.

    PUT:
    Updates the specified location with new data.
    Returns the updated location's data on success.

    DELETE:
    Deletes the specified location.
    Returns a success message on deletion.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        location_obj = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        location_obj = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location_obj = get_object_or_404(Location, pk=pk)
        location_obj.delete()
        return Response({"Location deleted"}, status=status.HTTP_204_NO_CONTENT)


class BoundaryListCreateView(APIView):
    """
    API view to list and create boundaries.

    GET:
    Returns a list of all boundaries.

    POST:
    Creates a new boundary with name and area.
    Returns the created boundary's data on success.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        boundary_obj = Boundary.objects.all()
        serializer = BoundarySerializer(boundary_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoundarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoundaryUpdateRetrieveDeleteView(APIView):
    """
    API view to retrieve, update, and delete a boundary by its ID.

    GET:
    Returns the data of the specified boundary.

    PUT:
    Updates the specified boundary with new data.
    Returns the updated boundary's data on success.

    DELETE:
    Deletes the specified boundary.
    Returns a success message on deletion.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        boundary_obj = get_object_or_404(Boundary, pk=pk)
        serializer = BoundarySerializer(boundary_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        boundary_obj = get_object_or_404(Boundary, pk=pk)
        serializer = BoundarySerializer(boundary_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        boundary_obj = get_object_or_404(Boundary, pk=pk)
        boundary_obj.delete()
        return Response({"Boundary deleted"}, status=status.HTTP_204_NO_CONTENT)


class CalculateDistanceView(APIView):
    """
    API view to calculate the distance between two locations.

    POST:
    Calculates the distance between two locations specified by their IDs.
    Returns the distance on success.
    """

    def post(self, request):
        location1_id = request.data.get('location1_id')
        location2_id = request.data.get('location2_id')

        if location1_id and location2_id:
            loc1_obj = get_object_or_404(Location, id=location1_id)
            loc2_obj = get_object_or_404(Location, id=location2_id)
            distance = loc1_obj.coordinates.distance(loc2_obj.coordinates)
            data = {
                'location1_id': location1_id,
                'location2_id': location2_id,
                'distance': distance
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class CheckBoundryView(APIView):
    """
    API view to check if a location is within a boundary.

    POST:
    Checks if the specified location (by ID) is within the specified boundary (by ID).
    Returns a boolean indicating whether the location is within the boundary.
    """

    def post(self, request):
        location_id = request.data.get('location_id')
        boundary_id = request.data.get('boundary_id')
        if location_id and boundary_id:
            loc_obj = get_object_or_404(Location, id=location_id)
            boundary_obj = get_object_or_404(Boundary, id=boundary_id)
            result = boundary_obj.area.contains(loc_obj.coordinates)
            return Response({'is_within': result}, status=status.HTTP_200_OK)
        return Response({'errors': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    """
    Renders the index page with locations and boundaries data.
    """
    permission_classes = [IsAuthenticated]

    location_obj = Location.objects.only('id', 'name', 'description', 'coordinates')
    location_serializer = LocationSerializer(location_obj, many=True)
    boundaries = Boundary.objects.only('id', 'name', 'area')
    boundary_serializer = BoundarySerializer(boundaries, many=True)

    context = {
        'locations': location_serializer.data,
        'boundaries': boundary_serializer.data,
        'locations_json': json.dumps(location_serializer.data),
        'boundaries_json': json.dumps(boundary_serializer.data)
    }
    return render(request, 'gis_app/index.html', context)
