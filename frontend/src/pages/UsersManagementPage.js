import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { userApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { UserPlus, Users, Shield, Building2, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';

const USER_ROLES = [
  { value: 'rh', label: 'RH', icon: Shield, color: 'bg-purple-100 text-purple-700' },
  { value: 'juridico', label: 'Jurídico', icon: Shield, color: 'bg-blue-100 text-blue-700' },
  { value: 'gerente', label: 'Gerente', icon: Building2, color: 'bg-emerald-100 text-emerald-700' },
  { value: 'coordenador', label: 'Coordenador', icon: Users, color: 'bg-teal-100 text-teal-700' },
  { value: 'supervisor', label: 'Supervisor', icon: Users, color: 'bg-cyan-100 text-cyan-700' },
  { value: 'colaborador', label: 'Colaborador', icon: Users, color: 'bg-slate-100 text-slate-700' },
];

export default function UsersManagementPage() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: '',
  });
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (user?.role === 'rh') {
      loadUsers();
    }
  }, [user]);

  const loadUsers = async () => {
    try {
      const response = await userApi.getAll();
      setUsers(response.data);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      toast.error('Erro ao carregar usuários');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCreating(true);

    try {
      await userApi.create(formData);
      toast.success('Usuário criado com sucesso!');
      setDialogOpen(false);
      setFormData({ name: '', email: '', password: '', role: '' });
      loadUsers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao criar usuário');
    } finally {
      setCreating(false);
    }
  };

  const getRoleConfig = (role) => {
    return USER_ROLES.find(r => r.value === role) || USER_ROLES[0];
  };

  const getUsersByRole = (role) => {
    return users.filter(u => u.role === role);
  };

  if (user?.role !== 'rh') {
    return (
      <MainLayout>
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Acesso negado. Apenas o RH pode gerenciar usuários.
          </AlertDescription>
        </Alert>
      </MainLayout>
    );
  }

  if (loading) {
    return (
      <MainLayout>
        <div className="text-center py-12">Carregando...</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6" data-testid="users-management-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Gestão de Usuários</h1>
            <p className="text-slate-600 mt-1">
              Apenas o RH pode criar e gerenciar contas de acesso ao sistema
            </p>
          </div>

          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button
                className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                data-testid="new-user-button"
              >
                <UserPlus className="h-4 w-4 mr-2" />
                Novo Usuário
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Criar Novo Usuário</DialogTitle>
                <DialogDescription>
                  Crie contas para Gerentes, Coordenadores, Supervisores, Colaboradores ou Jurídico
                </DialogDescription>
              </DialogHeader>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Nome Completo *</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Ex: João Silva"
                    required
                    data-testid="user-name-input"
                    className="h-10"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="joao.silva@empresa.com"
                    required
                    data-testid="user-email-input"
                    className="h-10"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Senha *</Label>
                  <Input
                    id="password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    placeholder="Mínimo 6 caracteres"
                    minLength={6}
                    required
                    data-testid="user-password-input"
                    className="h-10"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="role">Perfil/Função *</Label>
                  <Select
                    value={formData.role}
                    onValueChange={(value) => setFormData({ ...formData, role: value })}
                    required
                  >
                    <SelectTrigger data-testid="user-role-select" className="h-10">
                      <SelectValue placeholder="Selecione o perfil" />
                    </SelectTrigger>
                    <SelectContent>
                      {USER_ROLES.map((role) => (
                        <SelectItem key={role.value} value={role.value}>
                          {role.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button
                    type="submit"
                    disabled={creating}
                    className="flex-1 bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                    data-testid="submit-user-button"
                  >
                    {creating ? 'Criando...' : 'Criar Usuário'}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setDialogOpen(false)}
                  >
                    Cancelar
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <Alert className="bg-purple-50 border-purple-200">
          <Shield className="h-4 w-4 text-purple-600" />
          <AlertDescription className="text-purple-900">
            <strong>Privilégio Exclusivo do RH:</strong> Você é o único perfil autorizado a criar 
            novos usuários no sistema. Isso garante controle centralizado sobre os acessos.
          </AlertDescription>
        </Alert>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {USER_ROLES.map((roleConfig) => {
            const roleUsers = getUsersByRole(roleConfig.value);
            const Icon = roleConfig.icon;

            return (
              <Card key={roleConfig.value} data-testid={`role-card-${roleConfig.value}`}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className={`p-2 rounded-lg ${roleConfig.color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    {roleConfig.label}
                  </CardTitle>
                  <CardDescription>
                    {roleUsers.length} usuário(s) cadastrado(s)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {roleUsers.length === 0 ? (
                    <p className="text-sm text-slate-500">Nenhum usuário</p>
                  ) : (
                    <div className="space-y-2">
                      {roleUsers.map((u) => (
                        <div
                          key={u.id}
                          className="p-3 bg-slate-50 rounded-md"
                          data-testid={`user-item-${u.id}`}
                        >
                          <p className="font-medium text-slate-900 text-sm">{u.name}</p>
                          <p className="text-xs text-slate-600">{u.email}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Resumo de Acessos</CardTitle>
            <CardDescription>Total de {users.length} usuários cadastrados no sistema</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-md">
                <span className="font-medium">Administrativo (RH + Jurídico):</span>
                <span className="font-bold text-[#1B2A4E]">
                  {getUsersByRole('rh').length + getUsersByRole('juridico').length}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-md">
                <span className="font-medium">Gestão (Gerente + Coordenador + Supervisor):</span>
                <span className="font-bold text-[#1B2A4E]">
                  {getUsersByRole('gerente').length + 
                   getUsersByRole('coordenador').length + 
                   getUsersByRole('supervisor').length}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-md">
                <span className="font-medium">Operacional (Colaboradores):</span>
                <span className="font-bold text-[#1B2A4E]">
                  {getUsersByRole('colaborador').length}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
