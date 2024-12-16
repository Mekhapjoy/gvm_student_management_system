from django.urls import path
from schooladmin.views import OfficeStaffCreate, OfficeStaffView, LibrarianProfileView, StudentDetailsView, FeesRemarkView, LibraryHistoryView
urlpatterns = [
    path('admin_officestaffprofile/',OfficeStaffCreate.as_view(),name='admin_officestaffprofile'),
    path('Office_staff_view/',OfficeStaffView.as_view(),name='Office_staff_view'),
    path('admin_librarianprofile/',LibrarianProfileView.as_view(),name='admin_librarianprofile'),
    path('admin_schooldetails/',StudentDetailsView.as_view(),name='admin_schooldetails'),
    path('admin_feesremarks/',FeesRemarkView.as_view(),name='admin_feesremarks'),
    path('admin_librarianhistory/',LibraryHistoryView.as_view(),name='admin_librarianhistory'),
]