import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../templates/MainLayout';
import StatCard from '../atoms/StatCard';
import Button from '../atoms/Button';
import dashboardService from '../../services/dashboardService';

const DashboardPage = () => {
  const { user, tokens } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const token = tokens?.access || JSON.parse(localStorage.getItem('tokens') || '{}').access;
      const data = await dashboardService.getStats(token);
      setStats(data);
      setError(null);
    } catch (err) {
      console.error('Error loading dashboard stats:', err);
      setError('Error al cargar las estadísticas del dashboard');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(value);
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin"></div>
            <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-purple-500 rounded-full animate-spin" style={{ animationDuration: '1.5s' }}></div>
          </div>
          <p className="mt-6 text-slate-400 font-medium">Cargando estadísticas...</p>
        </div>
      </MainLayout>
    );
  }

  if (error) {
    return (
      <MainLayout>
        <div className="flex flex-col items-center justify-center min-h-[400px] bg-[#161B26] rounded-2xl p-8 border border-slate-800/50">
          <div className="w-20 h-20 rounded-full bg-red-500/10 flex items-center justify-center mb-4">
            <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-slate-300 mb-4 text-lg font-medium">{error}</p>
          <Button onClick={loadDashboardStats}>
            Reintentar
          </Button>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">
              Dashboard
            </h1>
            <p className="text-slate-400">
              Monitorea tus métricas en tiempo real
            </p>
          </div>
          <Button onClick={loadDashboardStats} variant="secondary" className="bg-[#161B26] border-slate-800 text-slate-300 hover:bg-[#1a2030] hover:text-white">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </Button>
        </div>

        {/* Main Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          <StatCard
            icon="🏢"
            title="Total Empresas"
            value={stats?.resumen?.total_empresas || 0}
            subtitle="Empresas registradas"
            color="blue"
            trend="+12"
            trendDirection="up"
          />
          <StatCard
            icon="📦"
            title="Total Productos"
            value={stats?.resumen?.total_productos || 0}
            subtitle="Productos en catálogo"
            color="purple"
            trend="+8.2%"
            trendDirection="up"
          />
          <StatCard
            icon="📋"
            title="Items en Inventario"
            value={stats?.resumen?.total_inventario || 0}
            subtitle="Total de registros"
            color="green"
            trend="+21%"
            trendDirection="up"
          />
          <StatCard
            icon="💰"
            title="Valor Total"
            value={formatCurrency(stats?.resumen?.valor_total_cop || 0)}
            subtitle="Inventario en COP"
            color="orange"
            trend="+0.8%"
            trendDirection="up"
          />
        </div>

        {/* Recent Companies */}
        {stats?.empresas_recientes && stats.empresas_recientes.length > 0 && (
          <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 overflow-hidden">
            <div className="p-6 border-b border-slate-800/50">
              <h2 className="text-xl font-bold text-white">Empresas Recientes</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-800/50">
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">NIT</th>
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Nombre</th>
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Dirección</th>
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Teléfono</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.empresas_recientes.map((empresa, index) => (
                    <tr key={empresa.nit} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                      <td className="py-4 px-6">
                        <span className="font-mono text-sm text-blue-400 font-medium">{empresa.nit}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-white font-medium">{empresa.nombre}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-slate-400 text-sm">{empresa.direccion || 'N/A'}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-slate-400 text-sm">{empresa.telefono || 'N/A'}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Top Products */}
        {stats?.productos_top && stats.productos_top.length > 0 && (
          <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 overflow-hidden">
            <div className="p-6 border-b border-slate-800/50">
              <h2 className="text-xl font-bold text-white">Productos Top (por Inventario)</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-800/50">
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Código</th>
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Nombre</th>
                    <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Empresa</th>
                    <th className="text-right py-4 px-6 font-semibold text-slate-400 text-sm">Cantidad</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.productos_top.map((producto, index) => (
                    <tr key={producto.producto__codigo || index} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                      <td className="py-4 px-6">
                        <span className="font-mono text-sm text-blue-400 font-medium">{producto.producto__codigo}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-white font-medium">{producto.producto__nombre}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-slate-400 text-sm">{producto.producto__empresa__nombre}</span>
                      </td>
                      <td className="py-4 px-6 text-right">
                        <span className="inline-flex items-center justify-center px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 font-semibold text-sm">
                          {producto.total_cantidad}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Inventory by Company */}
        {stats?.inventario_por_empresa && stats.inventario_por_empresa.length > 0 && (
          <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 overflow-hidden">
            <div className="p-6 border-b border-slate-800/50">
              <h2 className="text-xl font-bold text-white">Inventario por Empresa</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
              {stats.inventario_por_empresa.map((item, index) => (
                <div 
                  key={item.empresa__nit || index} 
                  className="bg-slate-800/30 rounded-xl p-5 border border-slate-700/50 hover:border-blue-500/50 transition-all hover:-translate-y-1"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                      <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                    </div>
                    <h3 className="text-white font-semibold text-lg">{item.empresa__nombre}</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Items</span>
                      <span className="text-white font-semibold">{item.total_productos || 0}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Cantidad</span>
                      <span className="text-blue-400 font-semibold">{item.total_cantidad || 0}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recent Activity */}
        {stats?.actividad_reciente && stats.actividad_reciente.length > 0 && (
          <div className="bg-[#161B26] rounded-2xl border border-slate-800/50 overflow-hidden">
            <div className="p-6 border-b border-slate-800/50">
              <h2 className="text-xl font-bold text-white">Actividad Reciente</h2>
            </div>
            <div className="p-6 space-y-3">
              {stats.actividad_reciente.map((activity, index) => (
                <div 
                  key={index} 
                  className="flex items-start gap-4 p-4 rounded-lg bg-slate-800/30 border border-slate-700/50 hover:border-blue-500/50 transition-all hover:bg-slate-800/50"
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    activity.tipo === 'empresa' ? 'bg-blue-500/10' : 'bg-purple-500/10'
                  }`}>
                    {activity.tipo === 'empresa' ? (
                      <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <p className="text-white font-medium">
                          {activity.descripcion}
                        </p>
                        <div className="flex items-center gap-2 mt-2 text-sm">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            activity.tipo === 'empresa' ? 'bg-blue-500/10 text-blue-400' : 'bg-purple-500/10 text-purple-400'
                          }`}>
                            {activity.tipo === 'empresa' ? 'Empresa' : 'Producto'}
                          </span>
                          <span className="text-slate-500">•</span>
                          <span className="text-slate-400">
                            {new Date(activity.fecha).toLocaleDateString('es-ES', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
