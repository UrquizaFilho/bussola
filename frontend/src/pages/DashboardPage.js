import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { SummaryCards } from '../components/SummaryCards';
import { RecentMeasuresTable } from '../components/RecentMeasuresTable';
import { measureApi } from '../services/api';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [recentMeasures, setRecentMeasures] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, measuresRes] = await Promise.all([
        measureApi.getDashboardStats(),
        measureApi.getAll(),
      ]);
      
      setStats(statsRes.data);
      setRecentMeasures(measuresRes.data.slice(0, 5));
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
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
      <div className="space-y-8" data-testid="dashboard-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
            <p className="text-slate-600 mt-1">Visão geral das medidas disciplinares</p>
          </div>
          <Button
            onClick={() => navigate('/measures/new')}
            className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
            data-testid="new-measure-button"
          >
            <Plus className="h-4 w-4 mr-2" />
            Nova Medida
          </Button>
        </div>

        <SummaryCards stats={stats} />

        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Medidas Recentes</h2>
          <RecentMeasuresTable measures={recentMeasures} />
        </div>
      </div>
    </MainLayout>
  );
}
