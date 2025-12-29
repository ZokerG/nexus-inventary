"""
Tests para el módulo de Empresas
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Empresa

User = get_user_model()


class EmpresaModelTest(TestCase):
    """Tests para el modelo Empresa"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='externo'
        )
        
        self.empresa = Empresa.objects.create(
            nit='900123456',
            nombre='TechCorp',
            direccion='Calle 123 #45-67',
            telefono='3001234567',
            created_by=self.user
        )
    
    def test_empresa_creation(self):
        """Test: Creación correcta de empresa"""
        self.assertEqual(self.empresa.nit, '900123456')
        self.assertEqual(self.empresa.nombre, 'TechCorp')
        self.assertIsNotNone(self.empresa.created_at)
        self.assertIsNotNone(self.empresa.updated_at)
    
    def test_empresa_str_representation(self):
        """Test: Representación string del modelo"""
        expected = f"TechCorp (900123456)"
        self.assertEqual(str(self.empresa), expected)
    
    def test_empresa_primary_key(self):
        """Test: NIT es la clave primaria"""
        self.assertEqual(self.empresa.pk, '900123456')
    
    def test_empresa_created_by_relationship(self):
        """Test: Relación con usuario creador"""
        self.assertEqual(self.empresa.created_by, self.user)
        self.assertIn(self.empresa, self.user.empresas_creadas.all())


class EmpresaAPITest(APITestCase):
    """Tests para el API de Empresas"""
    
    def setUp(self):
        """Configuración inicial para cada test de API"""
        self.client = APIClient()
        
        # Crear usuarios de prueba
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='administrador'
        )
        
        self.externo_user = User.objects.create_user(
            username='externo',
            email='externo@example.com',
            password='externo123',
            role='externo'
        )
        
        # Crear empresa de prueba
        self.empresa = Empresa.objects.create(
            nit='900111222',
            nombre='Empresa Test',
            direccion='Av. Principal 100',
            telefono='3009876543',
            created_by=self.admin_user
        )
        
        # URL base
        self.list_url = reverse('empresa-list')
        self.detail_url = reverse('empresa-detail', kwargs={'pk': self.empresa.nit})
    
    def test_list_empresas_without_authentication(self):
        """Test: Listar empresas sin autenticación debe fallar"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_empresas_with_authentication(self):
        """Test: Listar empresas con autenticación exitosa"""
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_retrieve_empresa(self):
        """Test: Obtener detalle de una empresa"""
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nit'], self.empresa.nit)
        self.assertEqual(response.data['nombre'], self.empresa.nombre)
    
    def test_create_empresa_as_admin(self):
        """Test: Crear empresa como administrador debe ser exitoso"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nit': '900333444',
            'nombre': 'Nueva Empresa',
            'direccion': 'Calle Nueva 456',
            'telefono': '3101234567'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Empresa.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Nueva Empresa')
    
    def test_create_empresa_as_externo_should_fail(self):
        """Test: Crear empresa como externo debe fallar"""
        self.client.force_authenticate(user=self.externo_user)
        data = {
            'nit': '900555666',
            'nombre': 'Empresa No Permitida',
            'direccion': 'Calle Test',
            'telefono': '3001111111'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_empresa_with_duplicate_nit(self):
        """Test: Crear empresa con NIT duplicado debe fallar"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nit': self.empresa.nit,  # NIT duplicado
            'nombre': 'Empresa Duplicada',
            'direccion': 'Calle Duplicada',
            'telefono': '3002222222'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_empresa_with_invalid_data(self):
        """Test: Crear empresa con datos inválidos debe fallar"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nit': '',  # NIT vacío
            'nombre': '',  # Nombre vacío
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nit', response.data)
        self.assertIn('nombre', response.data)
    
    def test_update_empresa_as_admin(self):
        """Test: Actualizar empresa como administrador"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nit': self.empresa.nit,
            'nombre': 'Empresa Actualizada',
            'direccion': 'Nueva Dirección',
            'telefono': '3009999999'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.empresa.refresh_from_db()
        self.assertEqual(self.empresa.nombre, 'Empresa Actualizada')
    
    def test_partial_update_empresa(self):
        """Test: Actualización parcial de empresa"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'telefono': '3007777777'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.empresa.refresh_from_db()
        self.assertEqual(self.empresa.telefono, '3007777777')
        # Verificar que otros campos no cambiaron
        self.assertEqual(self.empresa.nombre, 'Empresa Test')
    
    def test_update_empresa_as_externo_should_fail(self):
        """Test: Actualizar empresa como externo debe fallar"""
        self.client.force_authenticate(user=self.externo_user)
        data = {
            'nit': self.empresa.nit,
            'nombre': 'No Permitido',
            'direccion': 'Test',
            'telefono': '3000000000'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_empresa_as_admin(self):
        """Test: Eliminar empresa como administrador"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Empresa.objects.count(), 0)
    
    def test_delete_empresa_as_externo_should_fail(self):
        """Test: Eliminar empresa como externo debe fallar"""
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Empresa.objects.count(), 1)
    
    def test_search_empresas_by_nombre(self):
        """Test: Buscar empresas por nombre"""
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_filter_empresas_by_nit(self):
        """Test: Filtrar empresas por NIT"""
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.get(self.list_url, {'nit': self.empresa.nit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nit'], self.empresa.nit)
    
    def test_ordering_empresas(self):
        """Test: Ordenar empresas"""
        # Crear otra empresa para probar el ordenamiento
        Empresa.objects.create(
            nit='900000000',
            nombre='AAA Primera',
            direccion='Test',
            telefono='3000000000',
            created_by=self.admin_user
        )
        
        self.client.force_authenticate(user=self.externo_user)
        response = self.client.get(self.list_url, {'ordering': 'nombre'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que están ordenadas
        nombres = [item['nombre'] for item in response.data['results']]
        self.assertEqual(nombres, sorted(nombres))
    
    def tearDown(self):
        """Limpieza después de cada test"""
        Empresa.objects.all().delete()
        User.objects.all().delete()


class EmpresaPermissionsTest(APITestCase):
    """Tests específicos de permisos"""
    
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='administrador'
        )
        self.externo = User.objects.create_user(
            username='externo',
            email='externo@test.com',
            password='externo123',
            role='externo'
        )
        self.list_url = reverse('empresa-list')
    
    def test_admin_can_create(self):
        """Test: Admin puede crear"""
        self.client.force_authenticate(user=self.admin)
        data = {
            'nit': '900111111',
            'nombre': 'Test',
            'direccion': 'Test',
            'telefono': '3000000000'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_externo_cannot_create(self):
        """Test: Externo no puede crear"""
        self.client.force_authenticate(user=self.externo)
        data = {
            'nit': '900222222',
            'nombre': 'Test',
            'direccion': 'Test',
            'telefono': '3000000000'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_both_can_read(self):
        """Test: Ambos roles pueden leer"""
        # Admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Externo
        self.client.force_authenticate(user=self.externo)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
