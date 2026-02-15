import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { auditApi } from '../services/api';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

export default function AuditPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const response = await auditApi.getLogs();
      setLogs(response.data);
    } catch (error) {
      console.error('Erro ao carregar logs:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="text-center py-12">Carregando...</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6" data-testid="audit-page">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Auditoria</h1>
          <p className="text-slate-600 mt-1">Histórico de ações no sistema</p>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Data/Hora</th>
                  <th>Usuário</th>
                  <th>Perfil</th>
                  <th>Ação</th>
                  <th>Detalhes</th>
                </tr>
              </thead>
              <tbody>
                {logs.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-8 text-slate-500">
                      Nenhum log de auditoria.
                    </td>
                  </tr>
                ) : (
                  logs.map((log) => (
                    <tr key={log.id} data-testid={`log-row-${log.id}`}>
                      <td className="font-mono text-slate-600 text-sm">
                        {format(new Date(log.timestamp), 'dd/MM/yyyy HH:mm:ss', { locale: ptBR })}
                      </td>
                      <td className="text-slate-900">{log.user_name}</td>
                      <td className="text-slate-600 capitalize">{log.user_role}</td>
                      <td className="font-medium text-slate-900">{log.action}</td>
                      <td className="text-slate-600 text-sm">
                        {JSON.stringify(log.details)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
