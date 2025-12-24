import React from 'react';
import { useAuth } from '../../context/AuthContext';
import './EmpresaTable.css';

const EmpresaTable = ({ empresas, onEdit, onDelete, loading }) => {
  const { isAdmin } = useAuth();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="relative w-16 h-16">
          <div className="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
        </div>
        <p className="mt-4 text-slate-400">Cargando empresas...</p>
      </div>
    );
  }

  if (!empresas || empresas.length === 0) {
    return (
      <div className="bg-[#161B26] rounded-xl border border-slate-800/50 p-12 text-center">
        <div className="w-20 h-20 mx-auto mb-4 bg-slate-800/50 rounded-full flex items-center justify-center">
          <svg className="w-10 h-10 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">No hay empresas registradas</h3>
        <p className="text-slate-400">Comienza agregando tu primera empresa</p>
      </div>
    );
  }

  return (
    <div className="bg-[#161B26] rounded-xl border border-slate-800/50 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800/50">
              <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">NIT</th>
              <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Nombre</th>
              <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Dirección</th>
              <th className="text-left py-4 px-6 font-semibold text-slate-400 text-sm">Teléfono</th>
              <th className="text-right py-4 px-6 font-semibold text-slate-400 text-sm">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empresas.map((empresa) => (
              <tr key={empresa.nit} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6">
                  <span className="font-mono text-sm text-blue-400 font-medium">{empresa.nit}</span>
                </td>
                <td className="py-4 px-6">
                  <span className="text-white font-medium">{empresa.nombre}</span>
                </td>
                <td className="py-4 px-6">
                  <span className="text-slate-400 text-sm">{empresa.direccion}</span>
                </td>
                <td className="py-4 px-6">
                  <span className="text-slate-400 text-sm">{empresa.telefono}</span>
                </td>
                <td className="py-4 px-6">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => onEdit(empresa)}
                      className="p-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 rounded-lg transition-colors"
                      title="Editar"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    {isAdmin() && (
                      <button
                        onClick={() => onDelete(empresa)}
                        className="p-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors"
                        title="Eliminar"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EmpresaTable;
