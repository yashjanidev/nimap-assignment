from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated

class ClientListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            clients = Client.objects.all().order_by('-created_at')
            data = ClientSerializer(clients, many=True)

            return Response({
                'success': True,
                'status': 200,
                'message': 'Clients Fetched Successfully',
                'count': len(data.data),
                'data': data.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return Response(response, status=response['status'])

    def post(self, request):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response({
                    'success': True,
                    'status': 201,
                    'message': 'Client Created Successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'success': False,
                'status': 400,
                'message': 'Validation Error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return Response(response, status=response['status'])


class ClientDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, client_id):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            client = get_object_or_404(Client, id=client_id)
            data = ClientSerializer(client)

            return Response({
                'success': True,
                'status': 200,
                'message': 'Client Fetched Successfully',
                'data': data.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        return Response(response, status=response['status'])

    def put(self, request, client_id):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            client = get_object_or_404(Client, id=client_id)
            serializer = ClientSerializer(client, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'status': 200,
                    'message': 'Client Updated Successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'success': False,
                'status': 400,
                'message': 'Validation Error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        return Response(response, status=response['status'])

    def delete(self, request, client_id):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            client = get_object_or_404(Client, id=client_id)
            client.delete()

            return Response({
                'success': True,
                'status': 200,
                'message': 'Client Deleted Successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        return Response(response, status=response['status'])

class UserProjectsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)

            return Response({
                'success': True,
                'status': 200,
                'message': 'Projects Fetched Successfully',
                'count': len(serializer.data),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return Response(response, status=response['status'])


class ProjectCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, client_id):
        response = {}
        try:
            if not request.user.is_authenticated:
                return Response({'success': False, "status": 401, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            client = get_object_or_404(Client, id=client_id)
            serializer = ProjectSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                project = serializer.save(created_by=request.user, client=client)
                return Response({
                    'success': True,
                    'status': 201,
                    'message': 'Project Created Successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'success': False,
                'status': 400,
                'message': 'Validation Error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return Response(response, status=response['status'])
