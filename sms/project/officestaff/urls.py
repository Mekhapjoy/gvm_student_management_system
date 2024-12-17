from django.urls import path
from officestaff.views import FeesRemarkCreateView, StudentDetailsView, LibraryHistoryView, StudentDetailsSearch, FeesRemarksSearch

urlpatterns = [
    path('officestaff-feesremark/',FeesRemarkCreateView.as_view(),name='officestaff-feesremark'),
    path('officestaff-studentdetails_view/',StudentDetailsView.as_view(),name='officestaff-studentdetails_view'),
    path('officestaff-libraryhistory_view/',LibraryHistoryView.as_view(),name='officestaff-libraryhistory_view'),
    path('officestaff-studentsearch/',StudentDetailsSearch.as_view(),name='officestaff-studentsearch'),
    path('officestaff-feesremark-search/',FeesRemarksSearch.as_view(),name='officestaff-feesremark-search')
]