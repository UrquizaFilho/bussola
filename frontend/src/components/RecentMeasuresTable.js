import React from 'react';
import { StatusBadge, MeasureTypeBadge } from './StatusBadge';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Eye } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';

export const RecentMeasuresTable = ({ measures, showEmployee = true }) => {
  const navigate = useNavigate();

  if (!measures || measures.length === 0) {
    return (
      <div className="text-center py-12 text-slate-500" data-testid="no-measures">
        Nenhuma medida registrada.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto" data-testid="measures-table">
      <table className="data-table">
        <thead>
          <tr>
            {showEmployee && <th>Colaborador</th>}
            <th>Tipo</th>
            <th>Motivo</th>
            <th>Aplicada por</th>
            <th>Data</th>
            <th>Status</th>
            <th className="text-right">Ações</th>
          </tr>
        </thead>
        <tbody>
          {measures.map((measure) => (
            <tr key={measure.id} data-testid={`measure-row-${measure.id}`}>
              {showEmployee && (
                <td className="font-medium text-slate-900">{measure.employee_name}</td>
              )}
              <td>
                <MeasureTypeBadge type={measure.measure_type} />
              </td>
              <td className="text-slate-600 max-w-xs truncate">{measure.reason}</td>
              <td className="text-slate-600">{measure.applied_by_name}</td>
              <td className="text-slate-600">
                {format(new Date(measure.applied_at), 'dd/MM/yyyy', { locale: ptBR })}
              </td>
              <td>
                <StatusBadge status={measure.status} />
              </td>
              <td className="text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate(`/measures/${measure.id}`)}
                  data-testid={`view-measure-${measure.id}`}
                >
                  <Eye className="h-4 w-4" />
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
