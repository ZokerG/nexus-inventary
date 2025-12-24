import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../templates/MainLayout';
import ProductoTable from '../organisms/ProductoTable';
import ProductoModal from '../organisms/ProductoModal';
import Button from '../atoms/Button';
import productoService from '../../services/productoService';
import './ProductosPage.css';

const ProductosPage = () => {
  const { tokens } = useAuth();
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProducto, setSelectedProducto] = useState(null);
  const [modalMode, setModalMode] = useState('create');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadProductos();
  }, []);

  const getToken = () => {
    return tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
  };

  const loadProductos = async () => {
    try {
      setLoading(true);
      const token = getToken();
      const data = await productoService.getAll(token);
      // Manejar respuesta paginada o array simple
      const productosArray = Array.isArray(data) ? data : (data.results || []);
      setProductos(productosArray);
      setError(null);
    } catch (err) {
      console.error('Error loading productos:', err);
      setError('Error al cargar los productos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setSelectedProducto(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleEdit = (producto) => {
    setSelectedProducto(producto);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleDelete = async (producto) => {
    const confirmed = window.confirm(
      `¿Estás seguro de que deseas eliminar el producto "${producto.nombre}"?\n\nEsta acción no se puede deshacer.`
    );

    if (!confirmed) return;

    const toastId = toast.loading('Eliminando producto...');

    try {
      const token = getToken();
      await productoService.delete(producto.codigo, token);
      setProductos(productos.filter(p => p.codigo !== producto.codigo));
      toast.success('Producto eliminado exitosamente', {
        id: toastId,
        icon: '🗑️',
      });
    } catch (err) {
      console.error('Error deleting producto:', err);
      const errorMsg = err.response?.data?.error || 'Error al eliminar el producto';
      toast.error(errorMsg, {
        id: toastId,
        icon: '❌',
      });
    }
  };

  const handleSave = async (productoData) => {
    const token = getToken();
    const toastId = toast.loading(modalMode === 'create' ? 'Creando producto...' : 'Actualizando producto...');

    try {
      if (modalMode === 'create') {
        const newProducto = await productoService.create(productoData, token);
        setProductos([...productos, newProducto]);
        toast.success('Producto creado exitosamente', {
          id: toastId,
          icon: '✅',
        });
      } else {
        const updatedProducto = await productoService.update(productoData.codigo, productoData, token);
        setProductos(productos.map(p => p.codigo === updatedProducto.codigo ? updatedProducto : p));
        toast.success('Producto actualizado exitosamente', {
          id: toastId,
          icon: '✅',
        });
      }
    } catch (err) {
      console.error('Error saving producto:', err);
      const errorMsg = err.response?.data?.error || 'Error al guardar el producto';
      toast.error(errorMsg, {
        id: toastId,
        icon: '❌',
      });
      throw err;
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredProductos = Array.isArray(productos)
    ? productos.filter(producto =>
        producto.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        producto.codigo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        producto.caracteristicas?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  return (
    <MainLayout>
      <div className="min-h-screen p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Productos</h1>
            <p className="text-slate-400">
              Gestiona el catálogo de productos y sus precios
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-blue-500/25 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Nuevo Producto
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-red-400">{error}</span>
            </div>
            <button
              onClick={loadProductos}
              className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
            >
              Reintentar
            </button>
          </div>
        )}

        <div className="space-y-6">
          {/* Search Bar */}
          <div className="bg-[#161B26] rounded-xl border border-slate-800/50 p-6">
            <div className="flex items-center gap-4">
              <div className="flex-1 relative">
                <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Buscar por nombre, código o características..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="w-full pl-12 pr-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                />
              </div>
              <div className="px-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg">
                <span className="text-slate-400 text-sm">
                  {filteredProductos.length} {filteredProductos.length === 1 ? 'producto' : 'productos'}
                </span>
              </div>
            </div>
          </div>

          <ProductoTable
            productos={filteredProductos}
            onEdit={handleEdit}
            onDelete={handleDelete}
            loading={loading}
          />
        </div>

        <ProductoModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          producto={selectedProducto}
          mode={modalMode}
        />
      </div>
    </MainLayout>
  );
};

export default ProductosPage;
