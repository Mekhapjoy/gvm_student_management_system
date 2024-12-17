from django.urls import path
from schooladmin.views import OfficeStaffCreate, OfficeStaffView, LibrarianProfileView, StudentDetailsView, FeesRemarkView, LibraryHistoryView, StudentDetailsSearch, FeesRemarksSearch, LibraryHistorySearch, SortStudentDetails 

urlpatterns = [
    path('admin_officestaffprofile/',OfficeStaffCreate.as_view(),name='admin_officestaffprofile'),
    path('Office_staff_view/',OfficeStaffView.as_view(),name='Office_staff_view'),
    path('admin_librarianprofile/',LibrarianProfileView.as_view(),name='admin_librarianprofile'),
    path('admin_schooldetails/',StudentDetailsView.as_view(),name='admin_schooldetails'),
    path('admin_feesremarks/',FeesRemarkView.as_view(),name='admin_feesremarks'),
    path('admin_librarianhistory/',LibraryHistoryView.as_view(),name='admin_librarianhistory'),
    path('admin_student_search/',StudentDetailsSearch.as_view(),name='admin_student_search'),
    path('admin-studentdetails_sort/',SortStudentDetails.as_view(),name='admin-studentdetails_sort'),
    path('admin_fees_search/',FeesRemarksSearch.as_view(),name='admin_fees_search'),
    path('admin_library_search/',LibraryHistorySearch.as_view(),name='admin_library_search'),
]