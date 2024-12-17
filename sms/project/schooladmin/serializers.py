from rest_framework import serializers
from accounts.models import User, OfficeStaffProfile, LibrarianProfile, SchoolStandards, StudentDetails, FeesRemarks, LibraryHistory


class OfficeStaffCreateSerializer(serializers.ModelSerializer):
    is_office_staff = serializers.BooleanField(default=False)
    full_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=30)
    place = serializers.CharField(max_length=20)
    joining_date = serializers.DateField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 50)
    phone_number = serializers.CharField(max_length=15)
    about = serializers.CharField(max_length = 255)
    profile_image = serializers.ImageField(required = False)
    gender = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=10)

    class Meta:
        model = OfficeStaffProfile
        fields = ['is_office_staff','full_name','address','place','joining_date','email','password','phone_number',
                  'about','profile_image','gender','status']
        

class EmployeeIdSerializer(serializers.Serializer):#use
    employee_id = serializers.CharField(max_length = 20)


class UserSerializer(serializers.ModelSerializer):#use
    class Meta:
        model = User
        fields = ['full_name','address','email','is_office_staff','place',
                  'joining_date','phone_number','password','is_librarian','is_superuser']


class OfficeStaffViewSerializer(serializers.ModelSerializer):#use
    user = UserSerializer()
    class Meta:
        model = OfficeStaffProfile
        fields = ['user','employee_id','about','profile_image','gender','status','profile_image']



class OfficeStaffSerializer(serializers.ModelSerializer):#use
    class Meta:
        model = OfficeStaffProfile
        fields = ['about','profile_image','gender','status']


class LibrarianProfileSerializer(serializers.ModelSerializer):
    is_librarian = serializers.BooleanField(default=False)
    full_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=30)
    place = serializers.CharField(max_length=20)
    joining_date = serializers.DateField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 50)
    phone_number = serializers.CharField(max_length=15)
    about = serializers.CharField(max_length = 255)
    profile_image = serializers.ImageField(required = False)
    gender = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=10)

    class Meta:
        model = LibrarianProfile
        fields = ['is_librarian','full_name','address','place','joining_date','email','password','phone_number',
                  'about','profile_image','gender','status']
        

class LibrarianViewSerializer(serializers.ModelSerializer):#use
    user = UserSerializer()
    class Meta:
        model = LibrarianProfile
        fields = ['user','employee_id','about','profile_image','gender','status','profile_image']


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarianProfile
        fields = ['about','profile_image','gender','status']


class StudentDetailsCreateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(max_length=30)
    address = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    student_phone_number = serializers.CharField(max_length=15)
    profile_image = serializers.ImageField(required=False)
    gender = serializers.CharField(max_length=1)
    standard = serializers.PrimaryKeyRelatedField(queryset = SchoolStandards.objects.all())
    roll_number = serializers.CharField(max_length=20)
    guardian_name = serializers.CharField(max_length=30)
    guardian_phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = StudentDetails
        fields = ['student_name','address','email','student_phone_number','profile_image','gender','standard',
                  'roll_number','guardian_name','guardian_phone_number']
        

    def validate_roll_number(self,value):
        standard = self.initial_data['standard']
        if not standard:
            raise serializers.ValidationError({'error':'standard is a required field.'})
        try:
            obj = SchoolStandards.objects.get(id = standard)
        except SchoolStandards.DoesNotExist:
            raise serializers.ValidationError({'error':'Invalid standard provided.'})
        class_mates = StudentDetails.objects.filter(standard = obj)
        roll_number_list = class_mates.values_list('roll_number',flat=True)
        print(roll_number_list)
        if value in roll_number_list:
            raise serializers.ValidationError({'error':'Duplication of roll number occured.'})
        min_rollno = 1
        max_rollno = obj.total_students
        roll_number = int(value)
        if roll_number < min_rollno or roll_number > max_rollno:
            raise serializers.ValidationError({'error':'Roll number out of limit'})
        return value
     
        
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
        

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = ['student_id','student_name','address','email','student_phone_number','profile_image','gender',
                  'roll_number','guardian_name','guardian_phone_number']


class StandardSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStandards
        fields = ['class_name','division']


class StudentFilterSerializer(serializers.ModelSerializer):
    standard = StandardSearchSerializer()
    class Meta:
        model = StudentDetails
        fields = ['student_id','standard','student_name','address','roll_number','guardian_name','guardian_phone_number','joining_date']
        

class FeesRemarkSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset = StudentDetails.objects.all())
    fees_type = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_date = serializers.DateField()
    remarks = serializers.CharField(max_length=50)
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']

class StudentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = ['student_id','student_name']
        

class FeesRemarksViewSerializer(serializers.ModelSerializer):
    student = StudentUpdateSerializer()
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']


class FeesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesRemarks
        fields = ['id','fees_type','amount','payment_date','remarks']


class LibraryHistorySerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset = StudentDetails.objects.all())
    book_name = serializers.CharField(max_length=50)
    borrow_date = serializers.DateTimeField(required=False)
    return_date = serializers.DateField()
    status = serializers.CharField(max_length=10)

    class Meta:
        model = LibraryHistory
        fields = ['student','book_name','borrow_date','return_date','status']


class LibraryHistoryViewSerializer(serializers.ModelSerializer):
    student = StudentViewSerializer()
    class Meta:
        model = LibraryHistory
        fields = '__all__'

class LibraryHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = ['id','book_name','borrow_date','return_date','status']



class FeesSearchSerializer(serializers.ModelSerializer):
    student = StudentViewSerializer()
    class Meta:
        model = FeesRemarks
        fields = ['student','fees_type','amount','payment_date','remarks']