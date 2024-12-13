from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Employee, Department, Role
from django.db.models import Q  # Corrected import statement

# Create your views here.
def index(request):
    return render(request, 'index.html')

def view_all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       salary = int(request.POST.get('salary'))
       bonus = int(request.POST.get('bonus'))  
       phone = int(request.POST.get('phone'))
       dept = int(request.POST.get('dept'))
       role = int(request.POST.get('role'))
       new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept, role_id=role, hire_date=datetime.now())
       print(request.POST)      
       new_emp.save()
       return HttpResponse('Employee added Successfully!')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id) 
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully!")
        except Employee.DoesNotExist: 
            return HttpResponse("Invalid Employee ID. Employee does not exist.")
        except Exception as e: 
            return HttpResponse(f"An error occurred: {str(e)}")
    else:
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emp = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emp = emps.filter(dept__name = dept)
        if role:
            emps = emps.filter(role__name = role)
        
        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html',)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Exception Occured")   
    
    return render(request, 'filter_emp.html', context)
