from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('admin_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password_hash', models.CharField(max_length=255)),
                ('role', models.CharField(default='EMPLOYEE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(
                    db_column='admin_id', on_delete=django.db.models.deletion.CASCADE,
                    related_name='employees', to='admin_api.admin',
                )),
            ],
            options={'db_table': 'employees'},
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.UniqueConstraint(
                fields=('admin', 'email'), name='employee_admin_email_uniq'
            ),
        ),
    ]
