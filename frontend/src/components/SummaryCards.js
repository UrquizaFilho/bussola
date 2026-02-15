import React from 'react';
import { TrendingUp, AlertTriangle, Users, FileText } from 'lucide-react';

export const SummaryCards = ({ stats }) => {
  const cards = [
    {
      title: 'Medidas do Mês',
      value: stats?.total_measures_month || 0,
      icon: TrendingUp,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      title: 'Pendentes',
      value: stats?.pending_measures || 0,
      icon: AlertTriangle,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
    },
    {
      title: 'Colaboradores',
      value: stats?.total_employees || 0,
      icon: Users,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50',
    },
    {
      title: 'Advertências',
      value: stats?.measures_by_type?.advertencia || 0,
      icon: FileText,
      color: 'text-slate-600',
      bg: 'bg-slate-50',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" data-testid="summary-cards">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <div key={index} className="summary-card" data-testid={`card-${index}`}>
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-600 mb-1">{card.title}</p>
                <p className="text-3xl font-bold text-slate-900">{card.value}</p>
              </div>
              <div className={`${card.bg} ${card.color} p-3 rounded-lg`}>
                <Icon className="h-6 w-6" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
