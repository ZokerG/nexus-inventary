import React, { useState, useEffect } from 'react';
import FormField from '../molecules/FormField';
import Button from '../atoms/Button';
import './ProductoModal.css';

const ProductoModal = ({ isOpen, onClose, onSave, producto, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    codigo: '',
    nombre: '',
    caracteristicas: '',
    precios: [
      { moneda: 'COP', precio: '' },
      { moneda: 'USD', precio: '' },
      { moneda: 'EUR', precio: '' }
    ]
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (producto && mode === 'edit') {
      setFormData({
        codigo: producto.codigo || '',
        nombre: producto.nombre || '',
        caracteristicas: producto.caracteristicas || '',
        precios: [
          { 
            moneda: 'COP', 
            precio: producto.precios?.find(p => p.moneda === 'COP')?.precio || '' 
          },
          { 
            moneda: 'USD', 
            precio: producto.precios?.find(p => p.moneda === 'USD')?.precio || '' 
          },
          { 
            moneda: 'EUR', 
            precio: producto.precios?.find(p => p.moneda === 'EUR')?.precio || '' 
          }
        ]
      });
    } else {
      setFormData({
        codigo: '',
        nombre: '',
        caracteristicas: '',
        precios: [
          { moneda: 'COP', precio: '' },
          { moneda: 'USD', precio: '' },
          { moneda: 'EUR', precio: '' }
        ]
      });
    }
    setErrors({});
  }, [producto, mode, isOpen]);

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

  const handlePriceChange = (moneda, value) => {
    setFormData(prev => ({
      ...prev,
      precios: prev.precios.map(p =>
        p.moneda === moneda ? { ...p, precio: value } : p
      )
    }));
    if (errors[`precio_${moneda}`]) {
      setErrors(prev => ({ ...prev, [`precio_${moneda}`]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.codigo) {
      newErrors.codigo = 'El código es requerido';
    } else if (formData.codigo.length < 3) {
      newErrors.codigo = 'El código debe tener al menos 3 caracteres';
    }

    if (!formData.nombre) {
      newErrors.nombre = 'El nombre es requerido';
    } else if (formData.nombre.length < 3) {
      newErrors.nombre = 'El nombre debe tener al menos 3 caracteres';
    }

    if (!formData.caracteristicas) {
      newErrors.caracteristicas = 'Las características son requeridas';
    }

    // Validar que al menos un precio esté ingresado
    const hasPrice = formData.precios.some(p => p.precio && p.precio !== '');
    if (!hasPrice) {
      newErrors.precios = 'Debe ingresar al menos un precio';
    }

    // Validar formato de precios
    formData.precios.forEach(p => {
      if (p.precio && p.precio !== '') {
        const precio = parseFloat(p.precio);
        if (isNaN(precio) || precio <= 0) {
          newErrors[`precio_${p.moneda}`] = 'Precio inválido';
        }
      }
    });

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
      // Filtrar solo los precios que tienen valor
      const dataToSend = {
        ...formData,
        precios: formData.precios
          .filter(p => p.precio && p.precio !== '')
          .map(p => ({
            moneda: p.moneda,
            precio: parseFloat(p.precio)
          }))
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
        setErrors({ general: 'Error al guardar el producto' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      codigo: '',
      nombre: '',
      caracteristicas: '',
      precios: [
        { moneda: 'COP', precio: '' },
        { moneda: 'USD', precio: '' },
        { moneda: 'EUR', precio: '' }
      ]
    });
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={handleClose}>
      <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 w-full max-w-3xl shadow-2xl max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="sticky top-0 bg-[#161B26] flex items-center justify-between p-6 border-b border-slate-800/50 z-10">
          <h2 className="text-2xl font-bold text-white">
            {mode === 'create' ? 'Nuevo Producto' : 'Editar Producto'}
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

          <FormField
            label="Código del Producto"
            name="codigo"
            type="text"
            value={formData.codigo}
            onChange={handleChange}
            placeholder="PROD001"
            required
            error={errors.codigo}
            disabled={mode === 'edit'}
          />

          <FormField
            label="Nombre del Producto"
            name="nombre"
            type="text"
            value={formData.nombre}
            onChange={handleChange}
            placeholder="Laptop HP Pavilion"
            required
            error={errors.nombre}
          />

          <FormField
            label="Características"
            name="caracteristicas"
            type="text"
            value={formData.caracteristicas}
            onChange={handleChange}
            placeholder="Intel Core i5, 8GB RAM, 256GB SSD"
            required
            error={errors.caracteristicas}
          />

          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-lg font-semibold text-white">Precios por Moneda</h3>
            </div>
            {errors.precios && (
              <div className="text-red-400 text-sm">{errors.precios}</div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
                  <span>🇨🇴</span>
                  COP (Pesos)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.precios[0].precio}
                  onChange={(e) => handlePriceChange('COP', e.target.value)}
                  placeholder="1500000.00"
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.precio_COP ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all`}
                />
                {errors.precio_COP && (
                  <span className="text-red-400 text-sm">{errors.precio_COP}</span>
                )}
              </div>

              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
                  <span>🇺🇸</span>
                  USD (Dólares)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.precios[1].precio}
                  onChange={(e) => handlePriceChange('USD', e.target.value)}
                  placeholder="399.99"
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.precio_USD ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all`}
                />
                {errors.precio_USD && (
                  <span className="text-red-400 text-sm">{errors.precio_USD}</span>
                )}
              </div>

              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
                  <span>🇪🇺</span>
                  EUR (Euros)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.precios[2].precio}
                  onChange={(e) => handlePriceChange('EUR', e.target.value)}
                  placeholder="359.99"
                  className={`w-full px-4 py-3 bg-slate-800/30 border ${errors.precio_EUR ? 'border-red-500/50' : 'border-slate-700/50'} rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all`}
                />
                {errors.precio_EUR && (
                  <span className="text-red-400 text-sm">{errors.precio_EUR}</span>
                )}
              </div>
            </div>
          </div>

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
              disabled={loading}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {loading ? 'Guardando...' : mode === 'create' ? 'Crear Producto' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductoModal;
