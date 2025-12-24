import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import empresaService from '../../services/empresaService';
import productoService from '../../services/productoService';

const InventarioModal = ({ isOpen, onClose, onSave, inventario, mode = 'create' }) => {
  const { tokens } = useAuth();
  const [formData, setFormData] = useState({
    empresa: '',
    producto: '',
    cantidad: ''
  });

  const [empresas, setEmpresas] = useState([]);
  const [productos, setProductos] = useState([]);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    if (isOpen) {
      loadInitialData();
    }
  }, [isOpen]);

  useEffect(() => {
    if (inventario && mode === 'edit') {
      setFormData({
        empresa: inventario.empresa || '',
        producto: inventario.producto || '',
        cantidad: inventario.cantidad || ''
      });
    } else {
      setFormData({
        empresa: '',
        producto: '',
        cantidad: ''
      });
    }
    setErrors({});
  }, [inventario, mode, isOpen]);

  const getToken = () => {
    return tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
  };

  const loadInitialData = async () => {
    try {
      setLoadingData(true);
      const token = getToken();
      
      const [empresasData, productosData] = await Promise.all([
        empresaService.getAll(token),
        productoService.getAll(token)
      ]);

      const empresasArray = Array.isArray(empresasData) ? empresasData : (empresasData.results || []);
      const productosArray = Array.isArray(productosData) ? productosData : (productosData.results || []);
      
      setEmpresas(empresasArray);
      setProductos(productosArray);
    } catch (error) {
      console.error('Error loading data:', error);
      setErrors({ general: 'Error al cargar empresas y productos' });
    } finally {
      setLoadingData(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.empresa) {
      newErrors.empresa = 'La empresa es requerida';
    }

    if (!formData.producto) {
      newErrors.producto = 'El producto es requerido';
    }

    if (!formData.cantidad && formData.cantidad !== 0) {
      newErrors.cantidad = 'La cantidad es requerida';
    } else if (parseInt(formData.cantidad) < 0) {
      newErrors.cantidad = 'La cantidad no puede ser negativa';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);

    try {
      const dataToSend = {
        empresa: formData.empresa,
        producto: formData.producto,
        cantidad: parseInt(formData.cantidad)
      };

      await onSave(dataToSend);
      handleClose();
    } catch (error) {
      if (error.response?.data) {
        const apiErrors = {};
        Object.keys(error.response.data).forEach(key => {
          apiErrors[key] = Array.isArray(error.response.data[key])
            ? error.response.data[key][0]
            : error.response.data[key];
        });
        setErrors(apiErrors);
      } else {
        setErrors({ general: 'Error al guardar el registro de inventario' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      empresa: '',
      producto: '',
      cantidad: ''
    });
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={handleClose}>
      <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 w-full max-w-2xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-6 border-b border-slate-800/50">
          <h2 className="text-2xl font-bold text-white">
            {mode === 'create' ? 'Nuevo Registro de Inventario' : 'Editar Inventario'}
          </h2>
          <button 
            className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-800/50 text-slate-400 hover:text-white transition-colors" 
            onClick={handleClose}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {errors.general && (
            <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400">
              {errors.general}
            </div>
          )}

          {loadingData ? (
            <div className="flex items-center justify-center py-8">
              <div className="relative w-12 h-12">
                <div className="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
              </div>
            </div>
          ) : (
            <>
              {/* Empresa Select */}
              <div className="space-y-2">
                <label htmlFor="empresa" className="block text-sm font-medium text-slate-300">
                  Empresa
                  <span className="text-red-400 ml-1">*</span>
                </label>
                <select
                  id="empresa"
                  name="empresa"
                  value={formData.empresa}
                  onChange={handleChange}
                  disabled={mode === 'edit'}
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.empresa ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  <option value="">Seleccionar empresa...</option>
                  {empresas.map((empresa) => (
                    <option key={empresa.nit} value={empresa.nit}>
                      {empresa.nombre} - {empresa.nit}
                    </option>
                  ))}
                </select>
                {errors.empresa && (
                  <p className="text-red-400 text-sm">{errors.empresa}</p>
                )}
              </div>

              {/* Producto Select */}
              <div className="space-y-2">
                <label htmlFor="producto" className="block text-sm font-medium text-slate-300">
                  Producto
                  <span className="text-red-400 ml-1">*</span>
                </label>
                <select
                  id="producto"
                  name="producto"
                  value={formData.producto}
                  onChange={handleChange}
                  disabled={mode === 'edit'}
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.producto ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  <option value="">Seleccionar producto...</option>
                  {productos.map((producto) => (
                    <option key={producto.codigo} value={producto.codigo}>
                      {producto.nombre} - {producto.codigo}
                    </option>
                  ))}
                </select>
                {errors.producto && (
                  <p className="text-red-400 text-sm">{errors.producto}</p>
                )}
              </div>

              {/* Cantidad Input */}
              <div className="space-y-2">
                <label htmlFor="cantidad" className="block text-sm font-medium text-slate-300">
                  Cantidad
                  <span className="text-red-400 ml-1">*</span>
                </label>
                <input
                  id="cantidad"
                  name="cantidad"
                  type="number"
                  min="0"
                  value={formData.cantidad}
                  onChange={handleChange}
                  placeholder="100"
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.cantidad ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all`}
                />
                {errors.cantidad && (
                  <p className="text-red-400 text-sm">{errors.cantidad}</p>
                )}
              </div>
            </>
          )}

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800/50">
            <button
              type="button"
              onClick={handleClose}
              disabled={loading}
              className="px-6 py-3 bg-slate-800/50 hover:bg-slate-800 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading || loadingData}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {loading ? 'Guardando...' : mode === 'create' ? 'Crear Registro' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InventarioModal;
