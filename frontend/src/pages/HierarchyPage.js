import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { userApi } from '../services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, TrendingDown, Building2 } from 'lucide-react';

export default function HierarchyPage() {
  const [hierarchy, setHierarchy] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHierarchy();
  }, []);

  const loadHierarchy = async () => {
    try {
      const response = await userApi.getHierarchy();
      setHierarchy(response.data);
    } catch (error) {
      console.error('Erro ao carregar hierarquia:', error);
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
      <div className="space-y-6" data-testid="hierarchy-page">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Minha Hierarquia</h1>
          <p className="text-slate-600 mt-1">Visualize sua equipe e subordinados diretos</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Subordinados Diretos
              </CardTitle>
              <CardDescription>
                Pessoas que reportam diretamente a você
              </CardDescription>
            </CardHeader>
            <CardContent>
              {hierarchy?.direct_reports?.length === 0 ? (
                <p className="text-slate-500 text-sm">Nenhum subordinado direto</p>
              ) : (
                <div className="space-y-2">
                  {hierarchy?.direct_reports?.map((person) => (
                    <div key={person.id} className="p-3 bg-slate-50 rounded-md">
                      <p className="font-medium text-slate-900">{person.name}</p>
                      <p className="text-sm text-slate-600 capitalize">{person.role}</p>
                      <p className="text-xs text-slate-500">{person.email}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building2 className="h-5 w-5" />
                Minhas Equipes
              </CardTitle>
              <CardDescription>
                Equipes que você gerencia
              </CardDescription>
            </CardHeader>
            <CardContent>
              {hierarchy?.teams?.length === 0 ? (
                <p className="text-slate-500 text-sm">Nenhuma equipe gerenciada</p>
              ) : (
                <div className="space-y-2">
                  {hierarchy?.teams?.map((team) => (
                    <div key={team.id} className="p-3 bg-slate-50 rounded-md">
                      <p className="font-medium text-slate-900">{team.name}</p>
                      <p className="text-sm text-slate-600 capitalize">{team.level}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingDown className="h-5 w-5" />
              Estrutura Organizacional
            </CardTitle>
            <CardDescription>
              Sua posição na hierarquia da empresa
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="p-6 bg-slate-50 rounded-lg">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 bg-[#1B2A4E] rounded-full flex items-center justify-center text-white font-bold">
                    G
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">Gerente</p>
                    <p className="text-sm text-slate-600">Gerencia coordenadores</p>
                  </div>
                </div>
                <div className="ml-6 border-l-2 border-slate-300 pl-6 space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 bg-slate-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      C
                    </div>
                    <div>
                      <p className="font-semibold text-slate-900">Coordenador</p>
                      <p className="text-sm text-slate-600">Gerencia supervisores</p>
                    </div>
                  </div>
                  <div className="ml-6 border-l-2 border-slate-300 pl-6 space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="h-8 w-8 bg-slate-400 rounded-full flex items-center justify-center text-white font-bold text-xs">
                        S
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900">Supervisor</p>
                        <p className="text-sm text-slate-600">Gerencia colaboradores</p>
                      </div>
                    </div>
                    <div className="ml-6 border-l-2 border-slate-300 pl-6">
                      <div className="flex items-center gap-3">
                        <div className="h-6 w-6 bg-slate-300 rounded-full flex items-center justify-center text-slate-700 font-bold text-xs">
                          C
                        </div>
                        <div>
                          <p className="text-sm text-slate-900">Colaboradores</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
