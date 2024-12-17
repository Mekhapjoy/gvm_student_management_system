from django.urls import path
from librarian.views import StudentDetailsView, LibraryHistoryView, SortLibraryHistory, LibraryHistorySearch

urlpatterns = [
    path('librarian-studentdetails_view/',StudentDetailsView.as_view(),name='librarian-studentdetails_view'),
    path('librarian-libraryhistory_view/',LibraryHistoryView.as_view(),name='librarian-libraryhistory_view'),
    path('libraryhistory-sort/',SortLibraryHistory.as_view(),name='libraryhistory-sort'),
    path('libraryhistory_search/',LibraryHistorySearch.as_view(),name='libraryhistory_search')
]
