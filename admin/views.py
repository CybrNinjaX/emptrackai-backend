import json

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .models import Admin


@csrf_exempt
def register_admin(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)

    required_fields = ('username', 'company_name', 'email', 'password', 'confirm_password')
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return JsonResponse(
            {'error': 'Missing required fields.', 'fields': missing_fields},
            status=400,
        )

    if data['password'] != data['confirm_password']:
        return JsonResponse({'error': 'Password and confirm_password do not match.'}, status=400)

    if Admin.objects.filter(email=data['email']).exists():
        return JsonResponse({'error': 'An admin with this email already exists.'}, status=409)

    admin = Admin.objects.create(
        username=data['username'],
        company_name=data['company_name'],
        email=data['email'],
        password_hash=make_password(data['password']),
    )

    return JsonResponse(
        {
            'message': 'Admin registered successfully.',
            'admin': {
                'id': admin.id,
                'username': admin.username,
                'company_name': admin.company_name,
                'email': admin.email,
                'role': admin.role,
            },
        },
        status=201,
    )


@csrf_exempt
def login_admin(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)

    required_fields = ('email', 'password')
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return JsonResponse(
            {'error': 'Missing required fields.', 'fields': missing_fields},
            status=400,
        )

    try:
        admin = Admin.objects.get(email=data['email'])
    except Admin.DoesNotExist:
        return JsonResponse({'error': 'Invalid email or password.'}, status=401)

    if not check_password(data['password'], admin.password_hash):
        return JsonResponse({'error': 'Invalid email or password.'}, status=401)

    refresh = RefreshToken()
    refresh['admin_id'] = admin.id
    refresh['email'] = admin.email
    refresh['username'] = admin.username
    refresh['role'] = admin.role

    return JsonResponse(
        {
            'message': 'Login successful.',
            'admin': {
                'id': admin.id,
                'username': admin.username,
                'company_name': admin.company_name,
                'email': admin.email,
                'role': admin.role,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        status=200,
    )


def get_authenticated_admin(request):
    """Return the admin represented by a valid SimpleJWT access token."""
    authorization = request.headers.get('Authorization', '')
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None, JsonResponse({'error': 'A Bearer access token is required.'}, status=401)

    try:
        token = AccessToken(parts[1])
        admin_id = token.get('admin_id')
        if admin_id is not None:
            admin = Admin.objects.get(pk=admin_id)
        else:
            # Tokens issued before admin_id was added can still resolve by email.
            admin = Admin.objects.get(email=token.get('email'))
    except (TokenError, Admin.DoesNotExist, TypeError, ValueError):
        return None, JsonResponse({'error': 'Invalid or expired access token.'}, status=401)

    if admin.role != 'ADMIN':
        return None, JsonResponse({'error': 'Admin access is required.'}, status=403)
    return admin, None


@csrf_exempt
def admin_profile(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)
    admin, error = get_authenticated_admin(request)
    if error:
        return error
    return JsonResponse({'admin': {
        'id': admin.id,
        'username': admin.username,
        'company_name': admin.company_name,
        'email': admin.email,
        'role': admin.role,
        'created_at': admin.created_at.isoformat(),
    }})

