from django.shortcuts import render

# Create your views here.
import json
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
