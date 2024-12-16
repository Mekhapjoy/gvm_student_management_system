from django.contrib import admin
from accounts.models import User, SchoolStandards, StudentDetails, LibraryHistory, FeesRemarks, OfficeStaffProfile, LibrarianProfile
# Register your models here.

admin.site.register(User)
admin.site.register(SchoolStandards)
admin.site.register(StudentDetails)
admin.site.register(LibraryHistory)
admin.site.register(FeesRemarks)
admin.site.register(OfficeStaffProfile)
admin.site.register(LibrarianProfile)