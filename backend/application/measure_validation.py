from domain.entities import MeasureType, InfractionCategory
from typing import List

class MeasureEscalationValidator:
    """
    Valida o escalonamento progressivo de medidas disciplinares.
    Regra: Se colaborador já recebeu advertência verbal pela mesma infração,
    próxima medida deve ser advertência escrita (ou mais grave).
    """
    
    @staticmethod
    def validate_measure_escalation(
        previous_measures: List[dict],
        infraction_category: InfractionCategory,
        proposed_measure_type: MeasureType
    ) -> tuple[bool, str]:
        """
        Retorna (is_valid, error_message)
        """
        # Filtrar medidas da mesma categoria de infração
        same_infraction_measures = [
            m for m in previous_measures 
            if m.get('infraction_category') == infraction_category.value
            and m.get('status') != 'cancelado'
        ]
        
        if not same_infraction_measures:
            # Primeira infração desta categoria - qualquer medida é válida
            return True, ""
        
        # Ordenar por data (mais recente primeiro)
        same_infraction_measures.sort(
            key=lambda x: x.get('applied_at', ''), 
            reverse=True
        )
        
        most_recent = same_infraction_measures[0]
        previous_type = most_recent.get('measure_type')
        
        # Regras de escalonamento
        escalation_order = {
            MeasureType.ADVERTENCIA_VERBAL.value: 0,
            MeasureType.ADVERTENCIA_ESCRITA.value: 1,
            MeasureType.SUSPENSAO.value: 2
        }
        
        previous_level = escalation_order.get(previous_type, -1)
        proposed_level = escalation_order.get(proposed_measure_type.value, -1)
        
        if previous_level == -1 or proposed_level == -1:
            return True, ""
        
        # Validar que a nova medida não é menos grave que a anterior
        if proposed_level < previous_level:
            return False, (
                f"Colaborador já recebeu {previous_type.replace('_', ' ').title()} "
                f"pela infração '{infraction_category.value.replace('_', ' ').title()}'. "
                f"Nova medida deve ser igual ou mais grave (mínimo: "
                f"{MeasureType(list(escalation_order.keys())[previous_level]).value.replace('_', ' ').title()})."
            )
        
        # Se já recebeu advertência verbal, não pode receber outra verbal
        if (previous_type == MeasureType.ADVERTENCIA_VERBAL.value and 
            proposed_measure_type == MeasureType.ADVERTENCIA_VERBAL):
            return False, (
                f"Colaborador já recebeu Advertência Verbal pela infração "
                f"'{infraction_category.value.replace('_', ' ').title()}'. "
                f"Próxima medida deve ser Advertência Escrita ou Suspensão."
            )
        
        return True, ""
    
    @staticmethod
    def get_suggested_measure(
        previous_measures: List[dict],
        infraction_category: InfractionCategory
    ) -> MeasureType:
        """
        Sugere a próxima medida apropriada baseada no histórico.
        """
        same_infraction_measures = [
            m for m in previous_measures 
            if m.get('infraction_category') == infraction_category.value
            and m.get('status') != 'cancelado'
        ]
        
        if not same_infraction_measures:
            return MeasureType.ADVERTENCIA_VERBAL
        
        # Verificar a medida mais grave já aplicada
        has_suspension = any(
            m.get('measure_type') == MeasureType.SUSPENSAO.value 
            for m in same_infraction_measures
        )
        has_written = any(
            m.get('measure_type') == MeasureType.ADVERTENCIA_ESCRITA.value 
            for m in same_infraction_measures
        )
        has_verbal = any(
            m.get('measure_type') == MeasureType.ADVERTENCIA_VERBAL.value 
            for m in same_infraction_measures
        )
        
        if has_suspension:
            return MeasureType.SUSPENSAO
        elif has_written:
            return MeasureType.SUSPENSAO
        elif has_verbal:
            return MeasureType.ADVERTENCIA_ESCRITA
        else:
            return MeasureType.ADVERTENCIA_VERBAL
