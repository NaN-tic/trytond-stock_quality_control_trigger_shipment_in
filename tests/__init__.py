# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.stock_quality_control_trigger_shipment_in.tests.test_stock_quality_control_trigger_shipment_in import suite
except ImportError:
    from .test_stock_quality_control_trigger_shipment_in import suite

__all__ = ['suite']
