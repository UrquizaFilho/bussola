import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { employeeApi } from '../services/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Search, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [filteredEmployees, setFilteredEmployees] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadEmployees();
  }, []);

  useEffect(() => {
    if (searchTerm) {
      const filtered = employees.filter(
        (emp) =>
          emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          emp.cpf.includes(searchTerm) ||
          emp.department.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredEmployees(filtered);
    } else {
      setFilteredEmployees(employees);
    }
  }, [searchTerm, employees]);

  const loadEmployees = async () => {
    try {
      const response = await employeeApi.getAll();
      setEmployees(response.data);
      setFilteredEmployees(response.data);
    } catch (error) {
      console.error('Erro ao carregar colaboradores:', error);
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
      <div className="space-y-6" data-testid="employees-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Colaboradores</h1>
            <p className="text-slate-600 mt-1">Gerencie os colaboradores da empresa</p>
          </div>
          <Button
            onClick={() => navigate('/employees/new')}
            className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
            data-testid="new-employee-button"
          >
            <Plus className="h-4 w-4 mr-2" />
            Novo Colaborador
          </Button>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-6">
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                type="text"
                placeholder="Buscar por nome, CPF ou departamento..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 h-10"
                data-testid="search-input"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>CPF</th>
                  <th>Departamento</th>
                  <th>Cargo</th>
                  <th className="text-right">Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredEmployees.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-8 text-slate-500">
                      {searchTerm ? 'Nenhum colaborador encontrado.' : 'Nenhum colaborador cadastrado.'}
                    </td>
                  </tr>
                ) : (
                  filteredEmployees.map((employee) => (
                    <tr key={employee.id} data-testid={`employee-row-${employee.id}`}>
                      <td className="font-medium text-slate-900">{employee.name}</td>
                      <td className="font-mono text-slate-600">{employee.cpf}</td>
                      <td className="text-slate-600">{employee.department}</td>
                      <td className="text-slate-600">{employee.position}</td>
                      <td className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => navigate(`/employees/${employee.id}`)}
                          data-testid={`view-employee-${employee.id}`}
                        >
                          <Eye className="h-4 w-4" />
                        </Button>
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
