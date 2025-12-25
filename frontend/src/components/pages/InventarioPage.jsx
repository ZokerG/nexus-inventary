import React, { useState, useEffect, useCallback } from 'react';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../templates/MainLayout';
import InventarioTable from '../organisms/InventarioTable';
import InventarioModal from '../organisms/InventarioModal';
import inventarioService from '../../services/inventarioService';
import empresaService from '../../services/empresaService';

const InventarioPage = () => {
  const { tokens } = useAuth();
  const [inventarios, setInventarios] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedInventario, setSelectedInventario] = useState(null);
  const [modalMode, setModalMode] = useState('create');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterEmpresa, setFilterEmpresa] = useState('');
  const [emailModalOpen, setEmailModalOpen] = useState(false);
  const [emailAddress, setEmailAddress] = useState('');
  const [emailLoading, setEmailLoading] = useState(false);

  const getToken = useCallback(() => {
    return tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
  }, [tokens]);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const token = getToken();
      const [inventarioData, empresasData] = await Promise.all([
        inventarioService.getAll(token),
        empresaService.getAll(token)
      ]);
      
      const inventariosArray = Array.isArray(inventarioData) ? inventarioData : (inventarioData.results || []);
      const empresasArray = Array.isArray(empresasData) ? empresasData : (empresasData.results || []);
      
      setInventarios(inventariosArray);
      setEmpresas(empresasArray);
      setError(null);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Error al cargar el inventario');
    } finally {
      setLoading(false);
    }
  }, [getToken]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreate = () => {
    setSelectedInventario(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleEdit = (inventario) => {
    setSelectedInventario(inventario);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleDelete = async (inventario) => {
    const confirmed = window.confirm(
      `¿Estás seguro de que deseas eliminar este registro?\n\n${inventario.empresa_nombre} - ${inventario.producto_nombre}\n\nEsta acción no se puede deshacer.`
    );

    if (!confirmed) return;

    const toastId = toast.loading('Eliminando registro...');

    try {
      const token = getToken();
      await inventarioService.delete(inventario.id, token);
      setInventarios(inventarios.filter(i => i.id !== inventario.id));
      toast.success('Registro eliminado exitosamente', {
        id: toastId,
        icon: '🗑️',
      });
    } catch (err) {
      console.error('Error deleting inventario:', err);
      const errorMsg = err.response?.data?.error || 'Error al eliminar el registro';
      toast.error(errorMsg, {
        id: toastId,
        icon: '❌',
      });
    }
  };

  const handleSave = async (inventarioData) => {
    const token = getToken();
    const toastId = toast.loading(modalMode === 'create' ? 'Creando registro...' : 'Actualizando registro...');

    try {
      if (modalMode === 'create') {
        const newInventario = await inventarioService.create(inventarioData, token);
        setInventarios([...inventarios, newInventario]);
        toast.success('Registro creado exitosamente', {
          id: toastId,
          icon: '✅',
        });
      } else {
        const updatedInventario = await inventarioService.update(selectedInventario.id, inventarioData, token);
        setInventarios(inventarios.map(i => i.id === updatedInventario.id ? updatedInventario : i));
        toast.success('Registro actualizado exitosamente', {
          id: toastId,
          icon: '✅',
        });
      }
    } catch (err) {
      console.error('Error saving inventario:', err);
      const errorMsg = err.response?.data?.error || 'Error al guardar el registro';
      toast.error(errorMsg, {
        id: toastId,
        icon: '❌',
      });
      throw err;
    }
  };

  const handleExportPDF = async () => {
    const toastId = toast.loading('Generando PDF...');
    
    try {
      const token = getToken();
      await inventarioService.exportPDF(filterEmpresa, token);
      toast.success('PDF descargado exitosamente', {
        id: toastId,
        icon: '📄',
      });
    } catch (err) {
      console.error('Error exporting PDF:', err);
      toast.error('Error al exportar PDF', {
        id: toastId,
        icon: '❌',
      });
    }
  };

  const handleSendEmail = async () => {
    if (!emailAddress) {
      toast.error('Por favor ingrese un email', {
        icon: '✉️',
      });
      return;
    }

    const toastId = toast.loading(`Enviando PDF a ${emailAddress}...`);

    try {
      setEmailLoading(true);
      const token = getToken();
      await inventarioService.sendEmail(emailAddress, filterEmpresa, token);
      toast.success(`PDF enviado exitosamente a ${emailAddress}`, {
        id: toastId,
        icon: '✉️',
        duration: 5000,
      });
      setEmailModalOpen(false);
      setEmailAddress('');
    } catch (err) {
      console.error('Error sending email:', err);
      toast.error('Error al enviar el email', {
        id: toastId,
        icon: '❌',
      });
    } finally {
      setEmailLoading(false);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilterEmpresa(e.target.value);
  };

  const filteredInventarios = Array.isArray(inventarios)
    ? inventarios.filter(inventario => {
        const matchesSearch = 
          inventario.empresa_nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          inventario.producto_nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          inventario.producto_codigo?.toLowerCase().includes(searchTerm.toLowerCase());
        
        const matchesFilter = !filterEmpresa || inventario.empresa === filterEmpresa;
        
        return matchesSearch && matchesFilter;
      })
    : [];

  return (
    <MainLayout>
      <div className="min-h-screen p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Inventario</h1>
            <p className="text-slate-400">
              Gestiona el inventario de productos por empresa
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setEmailModalOpen(true)}
              className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-purple-500/25 flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Enviar Email
            </button>
            <button
              onClick={handleExportPDF}
              className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-green-500/25 flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Exportar PDF
            </button>
            <button
              onClick={handleCreate}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-blue-500/25 flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Registro
            </button>
          </div>
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
              onClick={loadData}
              className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
            >
              Reintentar
            </button>
          </div>
        )}

        <div className="space-y-6">
          {/* Search and Filter Bar */}
          <div className="bg-[#161B26] rounded-xl border border-slate-800/50 p-6">
            <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-4">
              <div className="flex-1 relative">
                <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Buscar por empresa, producto o código..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="w-full pl-12 pr-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                />
              </div>
              <div className="lg:w-64">
                <select
                  value={filterEmpresa}
                  onChange={handleFilterChange}
                  className="w-full px-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg text-white focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                >
                  <option value="">Todas las empresas</option>
                  {empresas.map((empresa) => (
                    <option key={empresa.nit} value={empresa.nit}>
                      {empresa.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="px-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg">
                <span className="text-slate-400 text-sm">
                  {filteredInventarios.length} {filteredInventarios.length === 1 ? 'registro' : 'registros'}
                </span>
              </div>
            </div>
          </div>

          <InventarioTable
            inventarios={filteredInventarios}
            onEdit={handleEdit}
            onDelete={handleDelete}
            loading={loading}
          />
        </div>

        <InventarioModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSave}
          inventario={selectedInventario}
          mode={modalMode}
        />

        {/* Email Modal */}
        {emailModalOpen && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setEmailModalOpen(false)}>
            <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 w-full max-w-md shadow-2xl" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between p-6 border-b border-slate-800/50">
                <h2 className="text-2xl font-bold text-white">Enviar PDF por Email</h2>
                <button 
                  className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-800/50 text-slate-400 hover:text-white transition-colors" 
                  onClick={() => setEmailModalOpen(false)}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="p-6 space-y-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-300">
                    Email del destinatario
                  </label>
                  <input
                    type="email"
                    value={emailAddress}
                    onChange={(e) => setEmailAddress(e.target.value)}
                    placeholder="ejemplo@correo.com"
                    className="w-full px-4 py-3 bg-slate-800/30 border border-slate-700/50 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                  />
                </div>
                {filterEmpresa && (
                  <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                    <p className="text-blue-400 text-sm">
                      Se enviará el inventario filtrado por empresa
                    </p>
                  </div>
                )}
                <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800/50">
                  <button
                    onClick={() => setEmailModalOpen(false)}
                    disabled={emailLoading}
                    className="px-6 py-3 bg-slate-800/50 hover:bg-slate-800 text-white font-semibold rounded-xl transition-colors disabled:opacity-50"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleSendEmail}
                    disabled={emailLoading || !emailAddress}
                    className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-semibold rounded-xl transition-all hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
                  >
                    {emailLoading ? 'Enviando...' : 'Enviar Email'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default InventarioPage;
