from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from accounts.models import User, OfficeStaffProfile, StudentDetails, FeesRemarks, LibraryHistory
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from schooladmin.serializers import *
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 5

class OfficeStaffCreate(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    def get(self,request):
        try:
            office_staff_obj = OfficeStaffProfile.objects.all()
            print(office_staff_obj)
        except Exception as e:
            return Response({'error':'No record found. The table is empty.'},status=status.HTTP_204_NO_CONTENT)
        
        serializer = OfficeStaffViewSerializer(office_staff_obj, many=True)
        data = serializer.data
        response = [{'School Admin':'Welcome to School Admin Dashboard'}]
        for i in range(len(data)):
            print(data[i]['user']['full_name'],data[i]['employee_id'],data[i]['user']['place'])
            response.append({
                'employee_id': data[i]['employee_id'],
                'full_name': data[i]['user']['full_name'],
                'place': data[i]['user']['place'],
                'is_office_staff': data[i]['user']['is_office_staff'],
                'about' : data[i]['about']
            })
        paginator = self.pagination_class()
        pagination_queryset = paginator.paginate_queryset(response, request)
        return paginator.get_paginated_response(pagination_queryset)
        
        
    def post(self,request):
        serializer = OfficeStaffCreateSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.create(
                    is_office_staff = serializer.validated_data.get('is_office_staff'),
                    full_name = serializer.validated_data.get('full_name'),
                    address = serializer.validated_data.get('address'),
                    place = serializer.validated_data.get('place'),
                    joining_date = serializer.validated_data.get('joining_date'),
                    email = serializer.validated_data.get('email'),
                    phone_number = serializer.validated_data.get('phone_number'),
                )
                user.set_password(password)
                user.save()
                if user.is_office_staff:
                    try:
                        group_office_staff = Group.objects.get(name = 'Office_Staff')
                        user.groups.add(group_office_staff)
                    except Group.DoesNotExist:
                        try:
                            group_office_staff = Group.objects.create(name = 'Office_Staff')
                            studentdetails_content_type = ContentType.objects.get_for_model(StudentDetails)
                            feesremarks_content_type = ContentType.objects.get_for_model(FeesRemarks)
                            libraryhistory_content_type = ContentType.objects.get_for_model(LibraryHistory)
                            std_permission = Permission.objects.get(codename = 'view_studentdetails', content_type = studentdetails_content_type)
                            fees_permission = Permission.objects.filter(content_type = feesremarks_content_type)
                            library_permission = Permission.objects.get(codename = 'view_libraryhistory', content_type = libraryhistory_content_type)
                            list_fees_permissions = list(fees_permission)
                            group_office_staff.permissions.set((list_fees_permissions))
                            group_office_staff.permissions.add(std_permission,library_permission)
                            user.groups.add(group_office_staff)
                        except Exception as e:
                            return Response({'error':'Cannot create object'},status=status.HTTP_400_BAD_REQUEST)

                office_staff = OfficeStaffProfile.objects.create(
                    user = user,
                    about = serializer.validated_data.get('about'),
                    profile_image = serializer.validated_data.get('profile_image'),
                    gender = serializer.validated_data.get('gender'),
                    status = serializer.validated_data.get('status'),
                )

                response = {
                    'School Admin':'Welcome to School Admin Dashboard',
                    'status': 'Office staff created successfully.',
                    'employee_id':office_staff.employee_id,
                    'full_name':user.full_name,
                    'is_office_staff':user.is_office_staff,
                    'is_librarian':user.is_librarian,
                    'is_superuser': user.is_superuser
                }
                return Response(response, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'Email or phone number already exist'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data = request.data
        try:
            office_staff_obj = OfficeStaffProfile.objects.select_related('user').get(employee_id = data['employee_id'])
            user = office_staff_obj.user
        except OfficeStaffProfile.DoesNotExist:
                return Response({'error':'profile not found'},status=status.HTTP_404_NOT_FOUND)
        serializer_profile = OfficeStaffSerializer(office_staff_obj, data=data, partial=True)
        serializer_user = UserSerializer(user, data=data, partial=True)
        if serializer_profile.is_valid() and serializer_user.is_valid():
            serializer_profile.save()
            serializer_user.save()
            profile = serializer_profile.data
            user_data = serializer_user.data
            password = serializer_user.validated_data.get('password')
            if password is not None:
                user.set_password(password)
                user.save()
            response = [{'School Admin':'Welcome to School Admin Dashboard'}]
            response.append({
                'status':'Profile updated successfully.',
                'employee_id': office_staff_obj.employee_id,
                'full_name': user_data['full_name'],
                'address' : user_data['address'],
                'place' : user_data['place'],
                'joining_date': user_data['joining_date'],
                'email': user_data['email'],
                'about': profile['about'],
                'gender': profile['gender'],
                'profile_image': profile['profile_image'],
                'status': profile['status']
            })
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer_profile.errors,serializer_user.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        data = request.data
        try:
            user = User.objects.get(id = data['id'])
        except User.DoesNotExist:
            return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({
            'School Admin':'Welcome to School Admin Dashboard',
            'message':'User deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)

        

class OfficeStaffView(generics.RetrieveAPIView):  
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  
    def post(self,request):
        serializer = EmployeeIdSerializer(data = request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data.get('employee_id')
            try:
                office_staff_obj = OfficeStaffProfile.objects.get(employee_id = employee_id)
            except OfficeStaffProfile.DoesNotExist:
                return Response({'error':'profile not found'},status=status.HTTP_404_NOT_FOUND)
            serializer = OfficeStaffViewSerializer(office_staff_obj)
            data = serializer.data
            response = {
                'School Admin':'Welcome to School Admin Dashboard',
                'employee_id': employee_id,
                'full_name': data['user']['full_name'],
                'place': data['user']['place'],
                'is_office_staff': data['user']['is_office_staff'],
                'about' : data['about']
            }
            return Response(response,status=status.HTTP_200_OK)
            
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

   
            
class LibrarianProfileView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    def get(self,request):
        try:
            librarian_obj = LibrarianProfile.objects.all()
        except Exception as e:
            return Response({'error':'No record found. The table is empty.'},status=status.HTTP_204_NO_CONTENT)
        serializer = LibrarianViewSerializer(librarian_obj, many=True)
        data = serializer.data
        response = [{'School Admin':'Welcome to School Admin Dashboard'}]
        for i in range(len(data)):
            response.append({
                'employee_id': data[i]['employee_id'],
                'full_name': data[i]['user']['full_name'],
                'place': data[i]['user']['place'],
                'is_librarian': data[i]['user']['is_librarian'],
                'is_office_staff':data[i]['user']['is_office_staff'],
                'is_superuser':data[i]['user']['is_superuser'],
                'about' : data[i]['about']
            })
        paginator = self.pagination_class()
        pagination_queryset = paginator.paginate_queryset(response, request)
        return paginator.get_paginated_response(pagination_queryset)

    def post(self,request):
        serializer = LibrarianProfileSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.create(
                    is_librarian = serializer.validated_data.get('is_librarian'),
                    full_name = serializer.validated_data.get('full_name'),
                    address = serializer.validated_data.get('address'),
                    place = serializer.validated_data.get('place'),
                    joining_date = serializer.validated_data.get('joining_date'),
                    email = serializer.validated_data.get('email'),
                    phone_number = serializer.validated_data.get('phone_number'),
                )
                user.set_password(password)
                user.save()
                if user.is_librarian:
                    try:
                        group_librarian = Group.objects.get(name = 'Librarian')
                        user.groups.add(group_librarian)
                    except Group.DoesNotExist:
                        try:
                            group_librarian = Group.objects.create(name = 'Librarian')
                            studentdetails_content_type = ContentType.objects.get_for_model(StudentDetails)
                            libraryhistory_content_type = ContentType.objects.get_for_model(LibraryHistory)
                            std_permission = Permission.objects.get(codename = 'view_studentdetails', content_type = studentdetails_content_type)
                            library_permission = Permission.objects.get(codename = 'view_libraryhistory', content_type = libraryhistory_content_type)
                            group_librarian.permissions.add(std_permission,library_permission)
                            p = group_librarian.permissions.all()
                            user.groups.add(group_librarian)
                        except Exception as e:
                            return Response({'error':'Cannot create group object'},status=status.HTTP_400_BAD_REQUEST)
                librarian = LibrarianProfile.objects.create(
                    user = user,
                    about = serializer.validated_data.get('about'),
                    profile_image = serializer.validated_data.get('profile_image'),
                    gender = serializer.validated_data.get('gender'),
                    status = serializer.validated_data.get('status'),
                )
                response = {
                    'School Admin':'Welcome to School Admin Dashboard',
                    'status': 'Librarian created successfully.',
                    'employee_id':librarian.employee_id,
                    'full_name':user.full_name,
                    'is_librarian':user.is_librarian,
                    'is_office_staff': user.is_office_staff,
                    'is_superuser': user.is_superuser
                }
                return Response(response, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    'Email or phone number already exist'
                    },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data = request.data
        try:
            librarian_obj = LibrarianProfile.objects.get(employee_id = data['employee_id'])
            user = User.objects.get(id = librarian_obj.user.id)
        except OfficeStaffProfile.DoesNotExist:
                return Response({'error':'profile not found'},status=status.HTTP_404_NOT_FOUND)
        serializer_profile = LibrarianSerializer(librarian_obj, data=data, partial=True)
        serializer_user = UserSerializer(user, data=data, partial=True)
        if serializer_profile.is_valid() and serializer_user.is_valid():
            serializer_profile.save()
            serializer_user.save()
            profile = serializer_profile.data
            user_data = serializer_user.data
            password = serializer_user.validated_data.get('password')
            if password is not None:
                user.set_password(password)
                user.save()
            result = {
                'School Admin':'Welcome to School Admin Dashboard',
                'status':'Profile updated successfully.',
                'employee_id': librarian_obj.employee_id,
                'full_name': user_data['full_name'],
                'address' : user_data['address'],
                'place' : user_data['place'],
                'joining_date': user_data['joining_date'],
                'email': user_data['email'],
                'about': profile['about'],
                'gender': profile['gender'],
                'profile_image': profile['profile_image'],
                'status': profile['status']
            }
            return Response(result,status=status.HTTP_200_OK)
        else:
            return Response(serializer_profile.errors,serializer_user.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        data = request.data
        try:
            user = User.objects.get(id = data['id'])
        except User.DoesNotExist:
            return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({
            'School Admin':'Welcome to School Admin Dashboard',
            'message':'User deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)


class CustomSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        return [request.data.get('search','')]


class StudentDetailsSearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    queryset = StudentDetails.objects.all()
    serializer_class = StudentFilterSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student_id','standard__class_name']


class CustomSortFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        sort = request.data.get('sort',None)
        if sort == 'newest':
            return ['-joining_date']
        elif sort == 'oldest':
            return ['joining_date']
        return super().get_ordering(request, queryset, view)
    

class SortStudentDetails(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_class = [IsAdminUser]
    pagination_class = Pagination
    queryset = StudentDetails.objects.select_related('standard').all()
    serializer_class = StudentFilterSerializer
    filter_backends = [CustomSortFilter]
    ordering_fields = ['joining_date']

class StudentDetailsView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    def get(self,request):
        try:
            student_obj = StudentDetails.objects.all()
            print(student_obj)
        except Exception as e:
            return Response({
                'error':'No record found. The table is empty.'
                },status=status.HTTP_204_NO_CONTENT)
        
        serializer = StdentDetailsViewSerializer(student_obj, many=True)
        data = serializer.data
        response = [{'School Admin':'Welcome to School Admin Dashboard'}]
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
        
    
    def post(self,request):
        serializer = StudentDetailsCreateSerializer(data = request.data)
        if serializer.is_valid():
            try:
                student_obj = StudentDetails.objects.create(
                    student_name = serializer.validated_data.get('student_name'),
                    address = serializer.validated_data.get('address'),
                    email = serializer.validated_data.get('email'),
                    student_phone_number = serializer.validated_data.get('student_phone_number'),
                    gender = serializer.validated_data.get('gender'),
                    standard = serializer.validated_data.get('standard'),
                    roll_number = serializer.validated_data.get('roll_number'),
                    guardian_name = serializer.validated_data.get('guardian_name'),
                    guardian_phone_number = serializer.validated_data.get('guardian_phone_number')
                )
            
                response = {
                    'School Admin':'Welcome to School Admin Dashboard',
                    'status':'Student created successfully',
                    'student_id':student_obj.student_id,
                    'student_name':student_obj.student_name,
                    'class':student_obj.standard.class_name,
                    'division':student_obj.standard.division,
                    'roll_number':student_obj.roll_number,
                    'address':student_obj.address,
                    'guardian_name':student_obj.guardian_name,
                    'guardian_phone_number':student_obj.guardian_phone_number
                }
                return Response(response,status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error':'Invalid roll number or integrity error due to similar email.'
                    },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data = request.data
        keys = list(data.keys())
        if 'class_name' in keys and 'division' in keys:
            return Response({
                'error':'Class name and division edit can result in some issue'
                },status=status.HTTP_304_NOT_MODIFIED)
        try:
            student_id = data['student_id']
            student_obj = StudentDetails.objects.get(student_id = student_id)
        except StudentDetails.DoesNotExist:
            return Response({'error':'student not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentUpdateSerializer(student_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_data = serializer.data
            response = {
                'status':'Student details edited successfully',
                'student_id': student_id,
                'student_name':updated_data['student_name'],
                'class':student_obj.standard.class_name,
                'division':student_obj.standard.division,
                'roll_number':updated_data['roll_number'],
                'address':updated_data['address'],
                'guardian_name':updated_data['guardian_name'],
                'guardian_phone_number':updated_data['guardian_phone_number']
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request):
        data = request.data
        try:
            student_obj = StudentDetails.objects.get(student_id = data['student_id'])
        except User.DoesNotExist:
            return Response({'error':'Student detail not found'},status=status.HTTP_404_NOT_FOUND)
        student_obj.delete()
        return Response({
            'School Admin':'Welcome to School Admin Dashboard',
            'message':'User deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)
    

class FeesRemarksSearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    queryset = FeesRemarks.objects.all()
    serializer_class = FeesSearchSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student__student_id','fees_type']



class FeesRemarkView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
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
        response = [{'School Admin':'Welcome to School Admin Dashboard'}]
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
                    'School Admin':'Welcome to School Admin Dashboard',
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
            return Response({'error':'Feesremark instant not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = FeesUpdateSerializer(fees_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_fees = serializer.data
            response = {
                'School Admin':'Welcome to School Admin Dashboard',
                'status':'Fees remarks updated',
                'id':updated_fees['id'],
                'student_id':fees_obj.student.student_id,
                'student name':fees_obj.student.student_name,
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
            'School Admin':'Welcome to School Admin Dashboard',
            'message':'fees remark deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)
    

class LibraryHistorySearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = Pagination
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistoryViewSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['student__student_id','book_name','borrow_date','return_date']


class LibraryHistoryView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
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
        response = [{'School Admin':'Welcome to School Admin Dashboard'}]
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
        
    
    def post(self,request):
        serializer = LibraryHistorySerializer(data = request.data)
        if serializer.is_valid():
            try:
                library_obj =LibraryHistory.objects.create(
                    student = serializer.validated_data.get('student'),
                    book_name = serializer.validated_data.get('book_name'),
                    return_date = serializer.validated_data.get('return_date'),
                    status = serializer.validated_data.get('status')
                )
                response = {
                    'School Admin':'Welcome to School Admin Dashboard',
                    'status':'Library history created',
                    'student_id':library_obj.student.student_id,
                    'student name':library_obj.student.student_name,
                    'book_name':library_obj.book_name,
                    'borrow_date':library_obj.borrow_date,
                    'return_date':library_obj.return_date
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
            library_obj = LibraryHistory.objects.get(id = data['id'])
        except FeesRemarks.DoesNotExist:
            return Response({'error':'student not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = LibraryHistoryUpdateSerializer(library_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_library = serializer.data
            response = [{'School Admin':'Welcome to School Admin Dashboard'}]
            response.append({
                'status':'Library record updated',
                'id':updated_library['id'],
                'student_id':library_obj.student.student_id,
                'student name':library_obj.student.student_name,
                'book_name':updated_library['book_name'],
                'borrow_date':updated_library['borrow_date'],
                'return_date':updated_library['return_date'],
                })
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        data = request.data
        try:
            library_obj = LibraryHistory.objects.get(id = data['id'])
        except User.DoesNotExist:
            return Response({'error':'library record instance is not found'},status=status.HTTP_404_NOT_FOUND)
        library_obj.delete()
        return Response({
            'School Admin':'Welcome to School Admin Dashboard',
            'message':'library record deleted successfully.'
            },status=status.HTTP_204_NO_CONTENT)
    



        
        
    
        


        



        

        
            
