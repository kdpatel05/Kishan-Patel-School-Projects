from django.db import models

# Create your models here.

# Define the studentdetails class to store the data from the student data file in the finalprojectdb database.
class Studentdetails(models.Model):
    studentid = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    major = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    gpa = models.DecimalField(decimal_places=2, max_digits=3)
    
# Define the coursedetails class to store the data from the course data file in the finalprojectdb database.
class Coursedetails(models.Model):
    courseid = models.IntegerField(primary_key=True)
    coursetitle = models.CharField(max_length=100)
    coursename = models.CharField(max_length=100)
    studentsenrolled = models.IntegerField()
    coursedept = models.CharField(max_length=100)
    instructorname = models.CharField(max_length=100)
    
# Define the enrollmentdetails class to store the course enrollments for each student in the finalprojectdb database.
class Enrollmentdetails(models.Model):
    studentname = models.CharField(max_length=100)
    coursetitle = models.CharField(max_length=100)