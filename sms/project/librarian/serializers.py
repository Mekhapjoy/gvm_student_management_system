from rest_framework import serializers
from accounts.models import SchoolStandards, StudentDetails, LibraryHistory


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStandards
        fields = '__all__'


class StdentDetailsViewSerializer(serializers.ModelSerializer):
    standard = StandardSerializer()
    class Meta:
        model = StudentDetails
        fields = ['student_id','student_name','address','email','student_phone_number','profile_image','gender','standard',
                  'roll_number','guardian_name','guardian_phone_number']
        
class StudentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = ['student_id','student_name']
        

class LibraryHistoryViewSerializer(serializers.ModelSerializer):
    student = StudentViewSerializer()
    class Meta:
        model = LibraryHistory
        fields = '__all__'