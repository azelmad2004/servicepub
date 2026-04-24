import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicepub.settings')
django.setup()

from accounts.models import User, Citoyen, AgentAdministratif
from django.contrib.auth.hashers import make_password

# Create Superuser
if not User.objects.filter(username='admin@servicepub.ma').exists():
    admin = User.objects.create_superuser(
        username='admin@servicepub.ma',
        email='admin@servicepub.ma',
        password='adminpassword123',
        first_name='Admin',
        last_name='System',
        role='admin'
    )
    print("Superuser created: admin@servicepub.ma / adminpassword123")
else:
    print("Superuser already exists.")

# Create Test Citoyen
if not User.objects.filter(username='citoyen@test.ma').exists():
    user_citoyen = User.objects.create_user(
        username='citoyen@test.ma',
        email='citoyen@test.ma',
        password='testpassword123',
        first_name='Ali',
        last_name='Citoyen',
        role='citoyen'
    )
    Citoyen.objects.create(
        user=user_citoyen,
        CINE='GA123456',
        date_naissance='1990-01-01',
        lieu_naissance='Khénifra'
    )
    print("Test Citoyen created: citoyen@test.ma / testpassword123")
else:
    print("Test Citoyen already exists.")

# Create Test Agent
if not User.objects.filter(username='agent@test.ma').exists():
    user_agent = User.objects.create_user(
        username='agent@test.ma',
        email='agent@test.ma',
        password='agentpassword123',
        first_name='Hamza',
        last_name='Agent',
        role='agent'
    )
    AgentAdministratif.objects.create(
        user=user_agent,
        administration='Commune de Khénifra',
        code_acces='AGENT001'
    )
    print("Test Agent created: agent@test.ma / agentpassword123")
else:
    print("Test Agent already exists.")
