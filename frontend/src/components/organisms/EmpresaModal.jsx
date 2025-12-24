import React, { useState, useEffect } from 'react';
import FormField from '../molecules/FormField';
import Button from '../atoms/Button';
import './EmpresaModal.css';

const EmpresaModal = ({ isOpen, onClose, onSave, empresa, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    nit: '',
    nombre: '',
    direccion: '',
    telefono: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (empresa && mode === 'edit') {
      setFormData({
        nit: empresa.nit || '',
        nombre: empresa.nombre || '',
        direccion: empresa.direccion || '',
        telefono: empresa.telefono || ''
      });
    } else {
      setFormData({
        nit: '',
        nombre: '',
        direccion: '',
        telefono: ''
      });
    }
    setErrors({});
  }, [empresa, mode, isOpen]);

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

    if (!formData.nit) {
      newErrors.nit = 'El NIT es requerido';
    } else if (!/^\d{9,10}$/.test(formData.nit)) {
      newErrors.nit = 'El NIT debe tener 9 o 10 dígitos';
    }

    if (!formData.nombre) {
      newErrors.nombre = 'El nombre es requerido';
    } else if (formData.nombre.length < 3) {
      newErrors.nombre = 'El nombre debe tener al menos 3 caracteres';
    }

    if (!formData.direccion) {
      newErrors.direccion = 'La dirección es requerida';
    }

    if (!formData.telefono) {
      newErrors.telefono = 'El teléfono es requerido';
    } else if (!/^\d{7,10}$/.test(formData.telefono)) {
      newErrors.telefono = 'El teléfono debe tener entre 7 y 10 dígitos';
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
      await onSave(formData);
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
        setErrors({ general: 'Error al guardar la empresa' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      nit: '',
      nombre: '',
      direccion: '',
      telefono: ''
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
            {mode === 'create' ? 'Nueva Empresa' : 'Editar Empresa'}
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
            label="NIT"
            name="nit"
            type="text"
            value={formData.nit}
            onChange={handleChange}
            placeholder="123456789"
            required
            error={errors.nit}
            disabled={mode === 'edit'}
          />

          <FormField
            label="Nombre de la Empresa"
            name="nombre"
            type="text"
            value={formData.nombre}
            onChange={handleChange}
            placeholder="Empresa S.A.S"
            required
            error={errors.nombre}
          />

          <FormField
            label="Dirección"
            name="direccion"
            type="text"
            value={formData.direccion}
            onChange={handleChange}
            placeholder="Calle 123 #45-67"
            required
            error={errors.direccion}
          />

          <FormField
            label="Teléfono"
            name="telefono"
            type="tel"
            value={formData.telefono}
            onChange={handleChange}
            placeholder="3001234567"
            required
            error={errors.telefono}
          />

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
              {loading ? 'Guardando...' : mode === 'create' ? 'Crear Empresa' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EmpresaModal;
