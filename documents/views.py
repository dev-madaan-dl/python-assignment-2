from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from .models import Document, QueryLog, UserSession
from .serializers import DocumentSerializer, QueryLogSerializer, RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            UserSession.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            UserSession.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class DocumentListCreateView(APIView):

    def get(self, request):
        documents = Document.objects.filter(user=request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(documents, request)
        serializer = DocumentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):

    def get_object(self, pk, user):
        try:
            return Document.objects.get(pk=pk, user=user)
        except Document.DoesNotExist:
            return None

    def get(self, request, pk):
        document = self.get_object(pk, request.user)
        if not document:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def delete(self, request, pk):
        document = self.get_object(pk, request.user)
        if not document:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QueryView(APIView):

    def post(self, request):
        query_text = request.data.get('query', '')
        documents = Document.objects.filter(title__icontains=query_text).order_by('-created_at')
        result_ids = list(documents.values_list('id', flat=True))
        QueryLog.objects.create(
            user=request.user,
            query_text=query_text,
            results=result_ids,
        )
        serializer = DocumentSerializer(documents, many=True)
        return Response({
            'query': query_text,
            'count': len(result_ids),
            'results': serializer.data,
        })


class QueryHistoryView(APIView):

    def get(self, request):
        queries = QueryLog.objects.filter(user=request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queries, request)
        serializer = QueryLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
