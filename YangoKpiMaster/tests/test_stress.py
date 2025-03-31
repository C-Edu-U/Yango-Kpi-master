import pytest
import time
from django.urls import reverse

@pytest.mark.django_db
def test_stress_agents_view(client, django_user_model):
    # Crear un usuario de prueba y autenticarlo (se requiere que sea staff para acceder a la vista)
    user = django_user_model.objects.create_user(username="stressuser", password="stresspass", is_staff=True)
    client.login(username="stressuser", password="stresspass")
    
    # Definir la URL de la vista (en este caso usamos 'agents' como landing page)
    url = reverse("agents")
    
    # Número de solicitudes para el test de estrés
    num_requests = 500
    
    start_time = time.time()
    
    for _ in range(num_requests):
        response = client.get(url)
        assert response.status_code == 200  # Verifica que la respuesta sea correcta
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_requests
    
    print(f"Stress test: {num_requests} requests took {total_time:.2f} seconds, average response time: {avg_time:.4f} seconds")
