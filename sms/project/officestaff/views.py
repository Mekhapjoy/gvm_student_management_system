from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from accounts.models import User, StudentDetails, FeesRemarks, LibraryHistory
from accounts.views import HasPermission, IsOfficeStaff
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from officestaff.serializers import *
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 5


class FeesRemarkCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOfficeStaff]
    pagination_class = Pagination
    def get(self,request):
        data = request.data
        try:
            fees_obj = FeesRemarks.objects.all()
        except Exception as e:
            return Response({
                'error':'No record found. The table is empty.'
                },status=status.HTTP_204_NO_CONTENT)
        serializer = FeesRemarksViewSerializer(fees_obj, many=True)
        data = serializer.data
        response = [{'Office Staff':'Welcome to Office Staff Dashboard'}]
        for i in range(len(data)):
            response.append({
                'student_id':data[i]['student']['student_id'],
                'student name':data[i]['student']['student_name'],
                'fees_type':data[i]['fees_type'],
                'amount':data[i]['amount'],
                'payment_date':data[i]['payment_date']
            })
        paginator = self.pagination_class()
        pagination_queryset = paginator.paginate_queryset(response, request)
        return paginator.get_paginated_response(pagination_queryset)
        
    

    def post(self,request):
        serializer = FeesRemarkSerializer(data = request.data)
        if serializer.is_valid():
            try:
                fees_obj = FeesRemarks.objects.create(
                    student = serializer.validated_data.get('student'),
                    fees_type = serializer.validated_data.get('fees_type'),
                    amount = serializer.validated_data.get('amount'),
                    payment_date = serializer.validated_data.get('payment_date'),
                    remarks = serializer.validated_data.get('remarks')
                )
                response = {
                    'Office Staff':'Welcome to Office Staff Dashboard',
                    'status':'Fees remarks created',
                    'student_id':fees_obj.student.student_id,
                    'student name':fees_obj.student.student_name,
                    'fees_type':fees_obj.fees_type,
                    'amount':fees_obj.amount,
                    'payment_date':fees_obj.payment_date
                }
                return Response(response,status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error':'Invalid Credientials'
                    },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self,request):
        data = request.data
        try:
            fees_obj = FeesRemarks.objects.get(id = data['id'])
        except FeesRemarks.DoesNotExist:
            return Response({'error':'student not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = FeesUpdateSerializer(fees_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_fees = serializer.data
            response = {
                'Office Staff':'Welcome to Office Staff Dashboard',
                'status':'Fees remarks updated',
                'student_id':fees_obj.student.student_id,
                'student name':fees_obj.student.student_name,
                'id':updated_fees['id'],
                'fees_type':updated_fees['fees_type'],
                'amount':updated_fees['amount'],
                'payment_date':updated_fees['payment_date']
                }
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        data = request.data
        try:
            fees_obj = FeesRemarks.objects.get(id = data['id'])

        except User.DoesNotExist:
            return Response({'error':'fees remark of student is not found'},status=status.HTTP_404_NOT_FOUND)
        fees_obj.delete()
        return Response({
            'Office Staff':'Welcome to Office Staff Dashboard',
            'message':'fees remark deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)
    

class CustomSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        return [request.data.get('search','')]
    

class FeesRemarksSearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOfficeStaff]
    pagination_class = Pagination
    queryset = FeesRemarks.objects.all()
    serializer_class = FeesSearchSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student__student_id','fees_type']



class StudentDetailsSearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOfficeStaff]
    pagination_class = Pagination
    queryset = StudentDetails.objects.all()
    serializer_class = StudentSearchSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student_id','standard__class_name']




class StudentDetailsView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOfficeStaff]
    pagination_class = Pagination
    def get(self,request):
        try:
            student_obj = StudentDetails.objects.all()
        except Exception as e:
            return Response({
                'error':'No record found. The table is empty.'
                },status=status.HTTP_204_NO_CONTENT)
        
        serializer = StdentDetailsViewSerializer(student_obj, many=True)
        data = serializer.data
        response = [{'Office Staff':'Welcome to Office Staff Dashboard'}]
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
    permission_classes = [IsAuthenticated, IsOfficeStaff]
    pagination_class = Pagination
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
        response = [{'Office Staff':'Welcome to Office Staff Dashboard'}]
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
        