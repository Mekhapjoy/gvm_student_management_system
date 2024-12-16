# Generated by Django 3.2.25 on 2024-12-13 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_office_staff', models.BooleanField(default=False)),
                ('is_librarian', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=30)),
                ('place', models.CharField(max_length=20)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The group this user belong to.', related_name='accounts_user_groups', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='The permissions this group of user or a particular user have.', related_name='accounts_user_permissions', to='auth.Permission', verbose_name='user_permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchoolStandards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=10)),
                ('division', models.CharField(choices=[('A', 'A'), ('B', 'B')], max_length=1)),
                ('total_students', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('student_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('student_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='student-images/')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('roll_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('guardian_name', models.CharField(max_length=30)),
                ('guardian_phone_number', models.CharField(max_length=15)),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.schoolstandards')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeStaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('about', models.TextField()),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='officestaff-images/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=50)),
                ('borrow_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_library', to='accounts.studentdetails')),
            ],
        ),
        migrations.CreateModel(
            name='LibrarianProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('about', models.TextField()),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='librarian-images/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='librarian', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeesRemarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_type', models.CharField(choices=[('Exam Fees', 'Exam Fees'), ('Tusion Fees', 'Tusion Fees'), ('Tour Fees', 'Tour Fees'), ('Other', 'Other')], max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_fees', to='accounts.studentdetails')),
            ],
        ),
    ]
