import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { measureApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { MeasureTypeBadge, StatusBadge } from '../components/StatusBadge';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { AlertTriangle, CheckCircle, FileText } from 'lucide-react';
import { toast } from 'sonner';

export default function AcknowledgeMeasurePage() {
  const { user } = useAuth();
  const [measures, setMeasures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPendingMeasures();
  }, []);

  const loadPendingMeasures = async () => {
    try {
      const response = await measureApi.getAll();
      // Filtrar apenas medidas pendentes do colaborador logado
      const pending = response.data.filter(
        (m) => m.status === 'pendente_recebimento'
      );
      setMeasures(pending);
    } catch (error) {
      console.error('Erro ao carregar medidas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (measureId) => {
    try {
      await measureApi.acknowledge(measureId);
      toast.success('Recebimento confirmado com sucesso!');
      loadPendingMeasures();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao confirmar recebimento');
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
      <div className="space-y-6" data-testid="acknowledge-page">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Medidas Pendentes de Recebimento</h1>
          <p className="text-slate-600 mt-1">Confirme o recebimento das medidas aplicadas</p>
        </div>

        {measures.length === 0 ? (
          <Card>
            <CardContent className="pt-12 pb-12 text-center">
              <CheckCircle className="h-12 w-12 text-emerald-500 mx-auto mb-4" />
              <p className="text-slate-600">Nenhuma medida pendente de recebimento.</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            <Alert>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                Você precisa confirmar o recebimento das medidas abaixo. Este ato não significa concordância, apenas que você foi informado.
              </AlertDescription>
            </Alert>

            {measures.map((measure) => (
              <Card key={measure.id} data-testid={`measure-card-${measure.id}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Medida Disciplinar
                      </CardTitle>
                      <CardDescription>
                        Aplicada em {format(new Date(measure.applied_at), 'dd/MM/yyyy HH:mm', { locale: ptBR })}
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      <MeasureTypeBadge type={measure.measure_type} />
                      <StatusBadge status={measure.status} />
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm font-semibold text-slate-700">Motivo:</p>
                    <p className="text-slate-900">{measure.reason}</p>
                  </div>

                  <div>
                    <p className="text-sm font-semibold text-slate-700">Descrição:</p>
                    <p className="text-slate-900 whitespace-pre-wrap">{measure.description}</p>
                  </div>

                  <div>
                    <p className="text-sm text-slate-500">Aplicada por: {measure.applied_by_name}</p>
                  </div>

                  {measure.suspension_days && (
                    <Alert variant="destructive">
                      <AlertDescription>
                        Suspensão de {measure.suspension_days} dia(s)
                      </AlertDescription>
                    </Alert>
                  )}

                  <div className="pt-4 border-t">
                    <Button
                      onClick={() => handleAcknowledge(measure.id)}
                      className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                      data-testid={`acknowledge-button-${measure.id}`}
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Confirmar Recebimento
                    </Button>
                    <p className="text-xs text-slate-500 mt-2">
                      Ao confirmar, você atesta que foi informado sobre esta medida.
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
}
