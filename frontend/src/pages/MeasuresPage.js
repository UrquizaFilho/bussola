import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { RecentMeasuresTable } from '../components/RecentMeasuresTable';
import { measureApi } from '../services/api';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function MeasuresPage() {
  const [measures, setMeasures] = useState([]);
  const [filteredMeasures, setFilteredMeasures] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadMeasures();
  }, []);

  useEffect(() => {
    if (statusFilter === 'all') {
      setFilteredMeasures(measures);
    } else {
      setFilteredMeasures(measures.filter((m) => m.status === statusFilter));
    }
  }, [statusFilter, measures]);

  const loadMeasures = async () => {
    try {
      const response = await measureApi.getAll();
      setMeasures(response.data);
      setFilteredMeasures(response.data);
    } catch (error) {
      console.error('Erro ao carregar medidas:', error);
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
      <div className="space-y-6" data-testid="measures-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Medidas Disciplinares</h1>
            <p className="text-slate-600 mt-1">Gerencie todas as medidas aplicadas</p>
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

        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <div className="mb-4">
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-48 h-10" data-testid="status-filter">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas</SelectItem>
                <SelectItem value="pendente">Pendentes</SelectItem>
                <SelectItem value="assinado">Assinadas</SelectItem>
                <SelectItem value="cancelado">Canceladas</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <RecentMeasuresTable measures={filteredMeasures} />
        </div>
      </div>
    </MainLayout>
  );
}
