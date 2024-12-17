from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from accounts.models import StudentDetails, LibraryHistory
from accounts.views import IsLibrarian
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from librarian.serializers import *
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 5 


class StudentDetailsView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLibrarian]
    pagination_class = CustomPagination
    def get(self,request):
        try:
            student_obj = StudentDetails.objects.all()
        except Exception as e:
            return Response({
                'error':'No record found. The table is empty.'
                },status=status.HTTP_204_NO_CONTENT)
        
        serializer = StdentDetailsViewSerializer(student_obj, many=True)
        data = serializer.data
        response = [{'Librarian':'Welcome to Librarian Dashboard'}]
        for i in range(len(data)):
            response.append({
                'student_id':data[i]['student_id'],
                'student_name':data[i]['student_name'],
                'class':data[i]['standard']['class_name'],
                'division':data[i]['standard']['division'],
                'roll_number':data[i]['roll_number'],
                'address':data[i]['address'],
                'guardian_name':data[i]['guardian_name'],
                'guardian_phone_number':data[i]['guardian_phone_number']
            })
        paginator = self.pagination_class()
        pagination_queryset = paginator.paginate_queryset(response, request)
        return paginator.get_paginated_response(pagination_queryset)

 


class LibraryHistoryView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLibrarian]
    pagination_class = CustomPagination
    def get(self,request):
        data = request.data
        try:
            library_obj = LibraryHistory.objects.all()
        except Exception as e:
            return Response({
                'error':'No record found. The table is empty.'
                },status=status.HTTP_204_NO_CONTENT)
        serializer = LibraryHistoryViewSerializer(library_obj, many=True)
        data = serializer.data
        response = [{'Librarian':'Welcome to Librarian Dashboard'}]
        for i in range(len(data)):
            response.append({
                'student_id':data[i]['student']['student_id'],
                'student name':data[i]['student']['student_name'],
                'book_name':data[i]['book_name'],
                'borrow_date':data[i]['borrow_date'],
                'retun_date':data[i]['return_date']
            })
        paginator = self.pagination_class()
        pagination_queryset = paginator.paginate_queryset(response, request)
        return paginator.get_paginated_response(pagination_queryset)
    

class CustomSortFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        sort = request.data.get('sort',None)
        if sort == 'newest':
            return ['-borrow_date']
        elif sort == 'oldest':
            return ['borrow_date']
        return super().get_ordering(request, queryset, view)
    

class SortLibraryHistory(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_class = [IsAuthenticated, IsLibrarian]
    pagination_class = CustomPagination
    queryset = LibraryHistory.objects.select_related('student').all()
    serializer_class = LibraryHistoryViewSerializer
    filter_backends = [CustomSortFilter]
    ordering_fields = ['borrow_date']


class CustomSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        return [request.data.get('search','')]
    

class LibraryHistorySearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistoryViewSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student__student_id','book_name','borrow_date','return_date']