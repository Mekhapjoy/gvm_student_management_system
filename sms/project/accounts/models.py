from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.models import Group,Permission
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

GENDER_CHOICES = [
    ('M','Male'),
    ('F','Female'),
    ('O','Other')
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        else:
            email = self.normalize_email(email)

        user = self.model(email = email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if not email:
            raise ValueError("Superuser must have an email address.")
        return self.create_user(email=email, password=password, **extra_fields)
    


class User(AbstractBaseUser,PermissionsMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    is_office_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=30)
    place = models.CharField(max_length=20)
    joining_date = models.DateField(null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=15,unique=True,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='accounts_user_groups',
        blank=True,
        help_text='The group this user belong to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_user_permissions',
        blank=True,
        help_text='The permissions this group of user or a particular user have.',
        verbose_name='user_permissions'
    )


class OfficeStaffProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_staff')
    employee_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    about = models.TextField()
    profile_image = models.ImageField(upload_to='officestaff-images/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'),('Inactive', 'Inactive')])

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f'OFFICESTAFF{self.user.id}'
        super(OfficeStaffProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_id


class LibrarianProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian')
    employee_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    about = models.TextField()
    profile_image = models.ImageField(upload_to='librarian-images/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'),('Inactive', 'Inactive')])

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f'LIBRARIAN{self.user.id}'
        super(LibrarianProfile, self).save(*args, **kwargs)


DIVISION_CHOICES = [
    ('A','A'),
    ('B','B')
]

class SchoolStandards(models.Model):
    class_name = models.CharField(max_length=10)
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES)
    total_students = models.IntegerField()

    def __str__(self):
        return self.class_name
    

class StudentDetails(models.Model):
    student_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    student_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True, blank=True)
    student_phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to='student-images/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    standard = models.ForeignKey(SchoolStandards, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, blank=True)
    guardian_name = models.CharField(max_length=30)
    guardian_phone_number = models.CharField(max_length=15)
    joining_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.student_name} of class {self.standard.class_name} {self.standard.division}'


        
    def save(self, *args, **kwargs):
        if not self.student_id:
            class_name = self.standard.class_name.replace(" ","").upper()
            self.student_id = f'STUD{class_name}{self.standard.division}{self.roll_number}'
        super(StudentDetails, self).save(*args, **kwargs)


class LibraryHistory(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, related_name='student_library')
    book_name = models.CharField(max_length=50)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'),('Inactive', 'Inactive')])

    def __str__(self):
        return f'{self.book_name} borrowed by student of id {self.student.student_id}'
    



FEES_CHOICE = [
    ('Exam Fees','Exam Fees'),
    ('Tusion Fees','Tusion Fees'),
    ('Tour Fees','Tour Fees'),
    ('Other','Other')
]

class FeesRemarks(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, related_name='student_fees')
    fees_type = models.CharField(max_length=15, choices=FEES_CHOICE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.fees_type} payment by student of id {self.student.student_id}'