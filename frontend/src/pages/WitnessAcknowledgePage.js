import React, { useState } from 'react';
import { MainLayout } from '../components/Layout';
import { measureApi } from '../services/api';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { ArrowLeft, Users, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';

export default function WitnessAcknowledgePage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const measureId = searchParams.get('measure_id');

  const [formData, setFormData] = useState({
    witness1_email: '',
    witness1_password: '',
    witness2_email: '',
    witness2_password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await measureApi.acknowledgeWithWitnesses({
        measure_id: measureId,
        ...formData,
      });

      toast.success('Recebimento com testemunhas confirmado!');
      navigate('/measures');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao processar recebimento';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (!measureId) {
    return (
      <MainLayout>
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>ID da medida não encontrado.</AlertDescription>
        </Alert>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="max-w-2xl" data-testid="witness-acknowledge-page">
        <Button
          variant="ghost"
          onClick={() => navigate('/measures')}
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-6 w-6" />
              Recebimento com Testemunhas
            </CardTitle>
            <CardDescription>
              Quando o colaborador se recusa a dar recebido, você pode registrar com 2 testemunhas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Alert className="mb-6">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <strong>Requisitos:</strong>
                <ul className="list-disc list-inside mt-2 text-sm">
                  <li>2 testemunhas obrigatórias</li>
                  <li>Testemunhas devem ser Gerente, Coordenador ou Supervisor</li>
                  <li>Login e senha de cada testemunha serão validados</li>
                  <li>Testemunhas devem ser pessoas diferentes</li>
                </ul>
              </AlertDescription>
            </Alert>

            {error && (
              <Alert variant="destructive" className="mb-6">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4 p-4 bg-slate-50 rounded-lg">
                <h3 className="font-semibold text-slate-900">Testemunha 1</h3>
                <div className="space-y-2">
                  <Label htmlFor="witness1_email">Email *</Label>
                  <Input
                    id="witness1_email"
                    type="email"
                    value={formData.witness1_email}
                    onChange={(e) => setFormData({ ...formData, witness1_email: e.target.value })}
                    placeholder="email@empresa.com"
                    required
                    data-testid="witness1-email"
                    className="h-10"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="witness1_password">Senha *</Label>
                  <Input
                    id="witness1_password"
                    type="password"
                    value={formData.witness1_password}
                    onChange={(e) => setFormData({ ...formData, witness1_password: e.target.value })}
                    required
                    data-testid="witness1-password"
                    className="h-10"
                  />
                </div>
              </div>

              <div className="space-y-4 p-4 bg-slate-50 rounded-lg">
                <h3 className="font-semibold text-slate-900">Testemunha 2</h3>
                <div className="space-y-2">
                  <Label htmlFor="witness2_email">Email *</Label>
                  <Input
                    id="witness2_email"
                    type="email"
                    value={formData.witness2_email}
                    onChange={(e) => setFormData({ ...formData, witness2_email: e.target.value })}
                    placeholder="email@empresa.com"
                    required
                    data-testid="witness2-email"
                    className="h-10"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="witness2_password">Senha *</Label>
                  <Input
                    id="witness2_password"
                    type="password"
                    value={formData.witness2_password}
                    onChange={(e) => setFormData({ ...formData, witness2_password: e.target.value })}
                    required
                    data-testid="witness2-password"
                    className="h-10"
                  />
                </div>
              </div>

              <div className="flex gap-4 pt-4">
                <Button
                  type="submit"
                  className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                  disabled={loading}
                  data-testid="submit-button"
                >
                  {loading ? 'Processando...' : 'Confirmar Recebimento'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/measures')}
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
