from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        'admin_api.Admin',
        on_delete=models.CASCADE,
        related_name='employees',
        db_column='admin_id',
    )
    username = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='EMPLOYEE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'
        constraints = [
            models.UniqueConstraint(
                fields=('admin', 'email'), name='employee_admin_email_uniq'
            ),
        ]

    def __str__(self):
        return f'{self.username} ({self.company_name})'
