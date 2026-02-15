import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { employeeApi, measureApi } from '../services/api';
import { RecentMeasuresTable } from '../components/RecentMeasuresTable';
import { Button } from '@/components/ui/button';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus } from 'lucide-react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

export default function EmployeeDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [employee, setEmployee] = useState(null);
  const [measures, setMeasures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      const [empRes, measuresRes] = await Promise.all([
        employeeApi.getById(id),
        measureApi.getByEmployee(id),
      ]);
      
      setEmployee(empRes.data);
      setMeasures(measuresRes.data);
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

  if (!employee) {
    return (
      <MainLayout>
        <div className="text-center py-12">Colaborador não encontrado</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6" data-testid="employee-detail-page">
        <Button
          variant="ghost"
          onClick={() => navigate('/employees')}
          className="mb-6"
          data-testid="back-button"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar
        </Button>

        <div className="bg-white border border-slate-200 rounded-lg p-8">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">{employee.name}</h1>
              <p className="text-slate-600 mt-1">{employee.position} - {employee.department}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <p className="text-sm text-slate-500 mb-1">CPF</p>
              <p className="font-mono text-slate-900">{employee.cpf}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500 mb-1">Data de Admissão</p>
              <p className="text-slate-900">
                {format(new Date(employee.admission_date), 'dd/MM/yyyy', { locale: ptBR })}
              </p>
            </div>
          </div>

          <div className="border-t border-slate-200 pt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-slate-900">Histórico de Medidas</h2>
              <Button
                onClick={() => navigate('/measures/new')}
                size="sm"
                className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                data-testid="new-measure-button"
              >
                <Plus className="h-4 w-4 mr-2" />
                Aplicar Medida
              </Button>
            </div>
            <RecentMeasuresTable measures={measures} showEmployee={false} />
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
