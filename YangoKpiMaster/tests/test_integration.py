import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Agent

@pytest.mark.django_db
def test_landing_page_authenticated(client, django_user_model):
    # Crear un usuario de prueba
    test_user = django_user_model.objects.create_user(
        username="testuser", password="secret", is_staff=True
    )
    # Iniciar sesión
    client.login(username="testuser", password="secret")
    # Obtener la URL de la agents page, que es la landing page o página de redirección tras iniciar sesión
    url = reverse("agents")
    response = client.get(url)
    # Verificar que el status code sea 200
    assert response.status_code == 200
    # Verificar que se muestre el mensaje de bienvenida con el nombre del usuario
    assert b"Bienvenido: testuser" in response.content

@pytest.mark.django_db
def test_agents_view_integration(client, django_user_model):
    # Crear un usuario de prueba
    test_user = django_user_model.objects.create_user(
        username="testuser", password="secret", is_staff=True
    )
    client.login(username="testuser", password="secret")
    
    # Crear un agente para la prueba
    Agent.objects.create(operator_login="op123", agent_name="Agente Prueba", team="Team A")
    
    url = reverse("agents")
    response = client.get(url)
    
    assert response.status_code == 200
    # Verificar que el agente se muestre en la lista
    assert b"Agente Prueba" in response.content
