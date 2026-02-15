import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { employeeApi, measureApi } from '../services/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';
import { Alert, AlertDescription } from '@/components/ui/alert';

const INFRACTION_CATEGORIES = [
  { value: 'atraso', label: 'Atraso' },
  { value: 'falta_injustificada', label: 'Falta Injustificada' },
  { value: 'descumprimento_normas', label: 'Descumprimento de Normas' },
  { value: 'insubordinacao', label: 'Insubordinação' },
  { value: 'desrespeito', label: 'Desrespeito' },
  { value: 'negligencia', label: 'Negligência' },
  { value: 'uso_indevido_recursos', label: 'Uso Indevido de Recursos' },
  { value: 'outros', label: 'Outros' },
];

const MEASURE_TYPES = [
  { value: 'advertencia_verbal', label: 'Advertência Verbal' },
  { value: 'advertencia_escrita', label: 'Advertência Escrita' },
  { value: 'suspensao', label: 'Suspensão' },
];

export default function NewMeasurePage() {
  const [employees, setEmployees] = useState([]);
  const [formData, setFormData] = useState({
    employee_id: '',
    measure_type: '',
    infraction_category: '',
    reason: '',
    description: '',
    suspension_days: '',
  });
  const [loading, setLoading] = useState(false);
  const [validationError, setValidationError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const response = await employeeApi.getAll();
      setEmployees(response.data);
    } catch (error) {
      console.error('Erro ao carregar colaboradores:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setValidationError('');

    try {
      const payload = {
        employee_id: formData.employee_id,
        measure_type: formData.measure_type,
        infraction_category: formData.infraction_category,
        reason: formData.reason,
        description: formData.description,
      };

      if (formData.measure_type === 'suspensao' && formData.suspension_days) {
        payload.suspension_days = parseInt(formData.suspension_days);
      }

      await measureApi.create(payload);
      
      toast.success('Medida aplicada com sucesso!');
      navigate('/measures');
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Erro ao aplicar medida';
      setValidationError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="max-w-2xl" data-testid="new-measure-page">
        <Button
          variant="ghost"
          onClick={() => navigate('/measures')}
          className="mb-6"
          data-testid="back-button"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar
        </Button>

        <div className="bg-white border border-slate-200 rounded-lg p-8">
          <h1 className="text-2xl font-bold text-slate-900 mb-6">Aplicar Medida Disciplinar</h1>

          {validationError && (
            <Alert variant="destructive" className="mb-6">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{validationError}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="employee_id">Colaborador *</Label>
              <Select
                value={formData.employee_id}
                onValueChange={(value) => setFormData({ ...formData, employee_id: value })}
                required
              >
                <SelectTrigger data-testid="employee-select" className="h-10">
                  <SelectValue placeholder="Selecione um colaborador" />
                </SelectTrigger>
                <SelectContent>
                  {employees.map((emp) => (
                    <SelectItem key={emp.id} value={emp.id}>
                      {emp.name} - {emp.department}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="infraction_category">Categoria da Infração *</Label>
              <Select
                value={formData.infraction_category}
                onValueChange={(value) => setFormData({ ...formData, infraction_category: value })}
                required
              >
                <SelectTrigger data-testid="infraction-category-select" className="h-10">
                  <SelectValue placeholder="Selecione a categoria" />
                </SelectTrigger>
                <SelectContent>
                  {INFRACTION_CATEGORIES.map((cat) => (
                    <SelectItem key={cat.value} value={cat.value}>
                      {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-slate-500">
                Sistema valida escalonamento: se colaborador já recebeu verbal pela mesma infração, próxima deve ser escrita.
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="measure_type">Tipo de Medida *</Label>
              <Select
                value={formData.measure_type}
                onValueChange={(value) => setFormData({ ...formData, measure_type: value })}
                required
              >
                <SelectTrigger data-testid="measure-type-select" className="h-10">
                  <SelectValue placeholder="Selecione o tipo" />
                </SelectTrigger>
                <SelectContent>
                  {MEASURE_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {formData.measure_type === 'suspensao' && (
              <div className="space-y-2">
                <Label htmlFor="suspension_days">Dias de Suspensão *</Label>
                <Input
                  id="suspension_days"
                  type="number"
                  min="1"
                  value={formData.suspension_days}
                  onChange={(e) => setFormData({ ...formData, suspension_days: e.target.value })}
                  required={formData.measure_type === 'suspensao'}
                  data-testid="suspension-days-input"
                  className="h-10"
                />
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="reason">Motivo *</Label>
              <Input
                id="reason"
                value={formData.reason}
                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                placeholder="Ex: Falta não justificada no dia 15/01"
                required
                data-testid="reason-input"
                className="h-10"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Descrição Detalhada *</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Descreva detalhadamente os fatos que motivaram esta medida..."
                rows={6}
                required
                data-testid="description-input"
              />
            </div>

            <div className="flex gap-4 pt-4">
              <Button
                type="submit"
                className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                disabled={loading}
                data-testid="submit-button"
              >
                {loading ? 'Aplicando...' : 'Aplicar Medida'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate('/measures')}
                data-testid="cancel-button"
              >
                Cancelar
              </Button>
            </div>
          </form>
        </div>
      </div>
    </MainLayout>
  );
}
