import React, { useState } from 'react';
import { MainLayout } from '../components/Layout';
import { employeeApi } from '../services/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

export default function NewEmployeePage() {
  const [formData, setFormData] = useState({
    name: '',
    cpf: '',
    department: '',
    position: '',
    admission_date: '',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await employeeApi.create({
        ...formData,
        admission_date: new Date(formData.admission_date).toISOString(),
      });
      
      toast.success('Colaborador cadastrado com sucesso!');
      navigate('/employees');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao cadastrar colaborador');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <MainLayout>
      <div className="max-w-2xl" data-testid="new-employee-page">
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
          <h1 className="text-2xl font-bold text-slate-900 mb-6">Novo Colaborador</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="name">Nome Completo *</Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                data-testid="name-input"
                className="h-10"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="cpf">CPF *</Label>
              <Input
                id="cpf"
                name="cpf"
                value={formData.cpf}
                onChange={handleChange}
                placeholder="000.000.000-00"
                required
                data-testid="cpf-input"
                className="h-10"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="department">Departamento *</Label>
                <Input
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleChange}
                  required
                  data-testid="department-input"
                  className="h-10"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="position">Cargo *</Label>
                <Input
                  id="position"
                  name="position"
                  value={formData.position}
                  onChange={handleChange}
                  required
                  data-testid="position-input"
                  className="h-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="admission_date">Data de Admissão *</Label>
              <Input
                id="admission_date"
                name="admission_date"
                type="date"
                value={formData.admission_date}
                onChange={handleChange}
                required
                data-testid="admission-date-input"
                className="h-10"
              />
            </div>

            <div className="flex gap-4 pt-4">
              <Button
                type="submit"
                className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                disabled={loading}
                data-testid="submit-button"
              >
                {loading ? 'Salvando...' : 'Cadastrar Colaborador'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate('/employees')}
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
