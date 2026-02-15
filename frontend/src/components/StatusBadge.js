import React from 'react';
import { AlertTriangle, FileX, CheckCircle, Clock } from 'lucide-react';

const statusConfig = {
  pendente: {
    label: 'Pendente',
    className: 'text-slate-700 bg-slate-50 border-slate-200',
    icon: Clock,
  },
  assinado: {
    label: 'Assinado',
    className: 'text-emerald-700 bg-emerald-50 border-emerald-200',
    icon: CheckCircle,
  },
  cancelado: {
    label: 'Cancelado',
    className: 'text-slate-700 bg-slate-50 border-slate-200',
    icon: FileX,
  },
};

const typeConfig = {
  advertencia: {
    label: 'Advertência',
    className: 'text-amber-700 bg-amber-50 border-amber-200',
    icon: AlertTriangle,
  },
  suspensao: {
    label: 'Suspensão',
    className: 'text-red-700 bg-red-50 border-red-200',
    icon: FileX,
  },
};

export const StatusBadge = ({ status }) => {
  const config = statusConfig[status] || statusConfig.pendente;
  const Icon = config.icon;

  return (
    <span className={`status-badge ${config.className}`} data-testid={`status-${status}`}>
      <Icon className="h-3 w-3 mr-1" />
      {config.label}
    </span>
  );
};

export const MeasureTypeBadge = ({ type }) => {
  const config = typeConfig[type] || typeConfig.advertencia;
  const Icon = config.icon;

  return (
    <span className={`status-badge ${config.className}`} data-testid={`type-${type}`}>
      <Icon className="h-3 w-3 mr-1" />
      {config.label}
    </span>
  );
};
