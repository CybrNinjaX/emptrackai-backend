import json

from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from admin.views import get_authenticated_admin
from .models import Employee


@csrf_exempt
def create_employee(request):
    admin, error = get_authenticated_admin(request)
    if error:
        return error

    if request.method == 'GET':
        employees = Employee.objects.filter(admin=admin).order_by('-created_at')
        return JsonResponse({'employees': [
            {
                'id': employee.id,
                'admin_id': admin.id,
                'username': employee.username,
                'company_name': employee.company_name,
                'email': employee.email,
                'role': employee.role,
                'created_at': employee.created_at.isoformat(),
            }
            for employee in employees
        ]})
    if request.method != 'POST':
        return JsonResponse({'error': 'Only GET and POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)

    required = ('username', 'email', 'password', 'confirm_password')
    missing = [field for field in required if not data.get(field)]
    if missing:
        return JsonResponse({'error': 'Missing required fields.', 'fields': missing}, status=400)
    if data['password'] != data['confirm_password']:
        return JsonResponse({'error': 'Password and confirm_password do not match.'}, status=400)
    if Employee.objects.filter(admin=admin, email=data['email']).exists():
        return JsonResponse({'error': 'An employee with this email already exists in your company.'}, status=409)

    try:
        with transaction.atomic():
            employee = Employee.objects.create(
                admin=admin,
                username=data['username'],
                email=data['email'],
                company_name=admin.company_name,
                password_hash=make_password(data['password']),
            )
    except IntegrityError:
        return JsonResponse({'error': 'An employee with this email already exists in your company.'}, status=409)

    return JsonResponse({
        'message': 'Employee account created successfully.',
        'employee': {
            'id': employee.id,
            'admin_id': admin.id,
            'username': employee.username,
            'company_name': employee.company_name,
            'email': employee.email,
            'role': employee.role,
        },
    }, status=201)

@csrf_exempt
def login_employee(request):
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Only POST requests are allowed.'
        }, status=405)

    # Read JSON request
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            'error': 'Invalid JSON request.'
        }, status=400)

    if not isinstance(data, dict):
        return JsonResponse({
            'error': 'Request body must be a JSON object.'
        }, status=400)

    # Get email and password
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({
            'error': 'Email and password are required.'
        }, status=400)

    # Find employee using email
    employee = Employee.objects.filter(
        email=email
    ).first()

    if employee is None:
        return JsonResponse({
            'error': 'Invalid email or password.'
        }, status=401)

    # Verify password against stored hash
    if not check_password(password, employee.password_hash):
        return JsonResponse({
            'error': 'Invalid email or password.'
        }, status=401)

    # Login successful
    return JsonResponse({
        'message': 'Employee login successful.',
        'employee': {
            'id': employee.id,
            'username': employee.username,
            'email': employee.email,
            'company_name': employee.company_name,
            'role': employee.role,
        }
    }, status=200)