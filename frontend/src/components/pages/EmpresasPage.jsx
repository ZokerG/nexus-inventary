import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../templates/MainLayout';
import EmpresaTable from '../organisms/EmpresaTable';
import EmpresaModal from '../organisms/EmpresaModal';
import Button from '../atoms/Button';
import empresaService from '../../services/empresaService';
import './EmpresasPage.css';

const EmpresasPage = () => {
  const { tokens, isAdmin } = useAuth();
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEmpresa, setSelectedEmpresa] = useState(null);
  const [modalMode, setModalMode] = useState('create');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadEmpresas();
  }, []);

  const getToken = () => {
    return tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
  };

  const loadEmpresas = async () => {
    try {
      setLoading(true);
      const token = getToken();
      const data = await empresaService.getAll(token);
      // Manejar respuesta paginada o array simple
      const empresasArray = Array.isArray(data) ? data : (data.results || []);
      setEmpresas(empresasArray);
      setError(null);
    } catch (err) {
      console.error('Error loading empresas:', err);
      setError('Error al cargar las empresas');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setSelectedEmpresa(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleEdit = (empresa) => {
    setSelectedEmpresa(empresa);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleDelete = async (empresa) => {
    if (!isAdmin()) {
      toast.error('Solo los administradores pueden eliminar empresas', {
        icon: '🔒',
      });
      return;
    }

    const confirmed = window.confirm(
      `¿Estás seguro de que deseas eliminar la empresa "${empresa.nombre}"?\n\nEsta acción no se puede deshacer.`
    );

    if (!confirmed) return;

    const toastId = toast.loading('Eliminando empresa...');
    
    try {
      const token = getToken();
      await empresaService.delete(empresa.nit, token);
      setEmpresas(empresas.filter(e => e.nit !== empresa.nit));
      toast.success('Empresa eliminada exitosamente', {
        id: toastId,
        icon: '🗑️',
      });
    } catch (err) {
      console.error('Error deleting empresa:', err);
      const errorMsg = err.response?.data?.error || 'Error al eliminar la empresa';
      toast.error(errorMsg, {
        id: toastId,
        icon: '❌',
      });
    }
  };

  const handleSave = async (empresaData) => {
    const token = getToken();
    const toastId = toast.loading(modalMode === 'create' ? 'Creando empresa...' : 'Actualizando empresa...');

    try {
      if (modalMode === 'create') {
        const newEmpresa = await empresaService.create(empresaData, token);
        setEmpresas([...empresas, newEmpresa]);
        toast.success('Empresa creada exitosamente', {
          id: toastId,
          icon: '✅',
        });
      } else {
        const updatedEmpresa = await empresaService.update(empresaData.nit, empresaData, token);
        setEmpresas(empresas.map(e => e.nit === updatedEmpresa.nit ? updatedEmpresa : e));
        toast.success('Empresa actualizada exitosamente', {
          id: toastId,
          icon: '✅',
        });
      }
    } catch (err) {
      console.error('Error saving empresa:', err);
      const errorMsg = err.response?.data?.error || 'Error al guardar la empresa';
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

  const filteredEmpresas = Array.isArray(empresas) 
    ? empresas.filter(empresa =>
        empresa.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        empresa.nit?.includes(searchTerm) ||
        empresa.direccion?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  return (
    <MainLayout>
      <div className="min-h-screen p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Empresas</h1>
            <p className="text-slate-400">
              Gestiona las empresas registradas en el sistema
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-blue-500/25 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Nueva Empresa
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
              onClick={loadEmpresas}
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
                  placeholder="Buscar por nombre, NIT o dirección..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="w-full pl-12 pr-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                />
              </div>
              <div className="px-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg">
                <span className="text-slate-400 text-sm">
                  {filteredEmpresas.length} {filteredEmpresas.length === 1 ? 'empresa' : 'empresas'}
                </span>
              </div>
            </div>
          </div>

          <EmpresaTable
            empresas={filteredEmpresas}
            onEdit={handleEdit}
            onDelete={handleDelete}
            loading={loading}
          />
        </div>

        <EmpresaModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          empresa={selectedEmpresa}
          mode={modalMode}
        />
      </div>
    </MainLayout>
  );
};

export default EmpresasPage;
