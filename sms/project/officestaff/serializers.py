from rest_framework import serializers
from accounts.models import FeesRemarks, StudentDetails, SchoolStandards, LibraryHistory

class FeesRemarkSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset = StudentDetails.objects.all())
    fees_type = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_date = serializers.DateField()
    remarks = serializers.CharField(max_length=50)
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = ['student_id','student_name','address','email','student_phone_number','profile_image','gender',
                  'roll_number','guardian_name','guardian_phone_number']


class FeesRemarksViewSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']


class FeesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesRemarks
        fields = ['id','fees_type','amount','payment_date','remarks']


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStandards
        fields = ['class_name','division']


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


class StudentSearchSerializer(serializers.ModelSerializer):
    standard = StandardSerializer()
    class Meta:
        model = StudentDetails
        fields = ['student_id','standard','student_name','address','roll_number','guardian_name','guardian_phone_number']


class FeesSearchSerializer(serializers.ModelSerializer):
    student = StudentViewSerializer()
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']