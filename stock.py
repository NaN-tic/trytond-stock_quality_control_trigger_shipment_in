# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

from trytond.modules.quality_control_trigger.quality import (
    QualityControlTriggerMixin)

__all__ = ['QualityTemplate', 'ShipmentIn']


class QualityTemplate(metaclass=PoolMeta):
    __name__ = 'quality.template'

    @classmethod
    def _get_trigger_generation_models_by_trigger_models(cls):
        models = super(QualityTemplate,
            cls)._get_trigger_generation_models_by_trigger_models()
        generated_models = models.setdefault('stock.shipment.in', [])
        if 'stock.shipment.in' not in generated_models:
            generated_models.append('stock.shipment.in')
        return models


class ShipmentIn(QualityControlTriggerMixin, object, metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    @classmethod
    def receive(cls, shipments):
        super(ShipmentIn, cls).receive(shipments)
        cls.create_quality_tests(shipments, 'stock.shipment.in')

    def _get_quality_trigger_generation_instances(self, template):
        if template.trigger_generation_model == 'stock.shipment.in':
            return [self]
        return super(ShipmentIn,
            self)._get_quality_trigger_generation_instances(template)
