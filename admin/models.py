from django.db import models


class Admin(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50)
	company_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, unique=True)
	password_hash = models.CharField(max_length=255)
	role = models.CharField(max_length=20, default='ADMIN')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'admins'
