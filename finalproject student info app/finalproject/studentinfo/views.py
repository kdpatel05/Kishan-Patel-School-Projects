from django.shortcuts import render
from django.http import HttpResponse
from studentinfo.models import Studentdetails, Coursedetails, Enrollmentdetails
from django.db import connection
from django.core.paginator import Paginator # Import the Paginator class
from django.contrib.auth.decorators import login_required # Import the login decorator
from django.db.models import F, Avg # Import F expression and the average function

# Create your views here.

# user must be logged in to access the dashboard function
@login_required
# The dashboard function retrieves various data statistics from the Studentdetails, Coursedetails, and Enrollmentdetails tables and returns it to the dashboard.html web page.
def dashboard(request):
    # Django queries to retrieve data statistics for the Overall Statistics section of the dashboard.html web page.
    numstudents = Studentdetails.objects.filter().count()
    numcourses = Coursedetails.objects.filter().count()
    numenrollments = Enrollmentdetails.objects.filter().count()
    avggpa = Studentdetails.objects.aggregate(Average_GPA=Avg('gpa'))
    # Django queries to retrieve the count of students for the Students by Class section of the dashboard.html web page.
    numfreshmen = Studentdetails.objects.filter(year="Freshman").count()
    numsophomores = Studentdetails.objects.filter(year="Sophomore").count()
    numjuniors = Studentdetails.objects.filter(year="Junior").count()
    numseniors = Studentdetails.objects.filter(year="Senior").count()
    # Django query to determine the top classes for the Top Three Enrolled Classes section of the dashboard.html web page.
    topthree = Coursedetails.objects.order_by('-studentsenrolled')[:3]
    # Django queries to retrieve the count of students for the Students by Major section of the dashboard.html web page.
    chemistry = Studentdetails.objects.filter(major="Chemistry").count()
    it = Studentdetails.objects.filter(major="I.T.").count()
    marketing = Studentdetails.objects.filter(major="Marketing").count()
    physics = Studentdetails.objects.filter(major="Physics").count()
    stats = Studentdetails.objects.filter(major="Stats").count()
    # Store the results of the above Django queries in a dictionary called context.
    context = {"numstudents": numstudents, "numcourses": numcourses, "numenrollments": numenrollments, "avggpa": avggpa, "numfreshmen": numfreshmen, "numsophomores": numsophomores, "numjuniors": numjuniors, "numseniors": numseniors, "coursedata": topthree, "chemistry": chemistry, "it": it, "marketing": marketing, "physics": physics, "stats": stats}
    # Return the context dictionary to the dashboard.html web page.
    return render(request, "studentinfo/dashboard.html", context)
    
@login_required
# The enrollment function retrieves the data in the Studentdetails, Coursedetails, and Enrollmentdetails tables and returns it to the enrollment.html web page.
def enrollment(request):
    # Retrieve all data in the Studentdetails table and store in studentdata
    studentdata = Studentdetails.objects.order_by('lastname')
    # Retrieve all data in the Coursedetails table and store in coursedata    
    coursedata = Coursedetails.objects.order_by('coursetitle')
    # Retrieve all data in the Enrollmentdetails table and store it in enrollmentdata
    enrollmentdata = Enrollmentdetails.objects.all() 
    # Create dictionaries for the studentdata, coursedata, and enrollmentdata variables
    context = {'student':studentdata, 'course':coursedata, 'enrollment':enrollmentdata}
    # Return the dictionaries to the enrollment.html web page 
    return render(request, "studentinfo/enrollment.html", context)

# The saveenrollment function enrolls the selected student into the selected class.
def saveenrollment(request):
    # Check to see if the enrollment.html web page has past the selected student and course.
    if("studentdata" in request.GET and "coursedata" in request.GET):
        # Extract the studentdata and coursedata from the request object
        student = request.GET.get("studentdata")
        course = request.GET.get("coursedata")
        # Django query set statement to get the count of rows to determine the number of classes for which the student has already enrolled.
        coursecount = Enrollmentdetails.objects.filter(studentname = student).count()
        # Django query set statement to get the count of rows to determine if the student has already enrolled in the selected class.
        isenrolled = Enrollmentdetails.objects.filter(studentname = student, coursetitle = course).count()
        # Check to see if the student has already enrolled in 3 classes or in the selected class.
        if (coursecount < 3 and isenrolled == 0):
           data = Enrollmentdetails(studentname = student, coursetitle = course)
           # Insert a new row of data into the Enrollmentdetails table.
           data.save()
           # Update the studentsenrolled field in the Coursedetails table.
           Coursedetails.objects.filter(coursetitle = course).update(studentsenrolled = F('studentsenrolled') + 1)
           # Return a success message to the enrollment.html web page.
           return HttpResponse("success")
    # Return an error message to the enrollment.html web page.        
    return HttpResponse("error")
    
# user must be logged in to access the studentdetails function
@login_required    
# The studentdetails function displays student information on the studentdetails.html page
def studentdetails(request):
    # Retrieve all of the records from the Studentdetails table of the finalprojectdb database
    print(request.__dict__)
    data = Studentdetails.objects.all()

    # Creating a paginator object from the Paginator class that displays ten students at a time
    paginator = Paginator(data, 10)
    
    page = request.GET.get('page')
    page_data = paginator.get_page(page)
    
    # Create a dictionary to store the student details and return the dictionary to the studentdetails.html page
    context = {"studentdata": page_data}
    return render(request, "studentinfo/studentdetails.html", context)
    
# user must be logged in to access the coursedetails function
@login_required    
# The coursedetails function displays course information on the coursedetails.html page
def coursedetails(request):
    # Retrieve all of the records from the Coursedetails table of the finalprojectdb database
    print(request.__dict__)
    data = Coursedetails.objects.all()

    # Creating a paginator object from the Paginator class that displays ten courses at a time
    paginator = Paginator(data, 10)
    
    page = request.GET.get('page')
    page_data = paginator.get_page(page)
    
    # Create a dictionary to store the course details and return the dictionary to the coursedetails.html page
    context = {"coursedata": page_data}
    return render(request, "studentinfo/coursedetails.html", context)