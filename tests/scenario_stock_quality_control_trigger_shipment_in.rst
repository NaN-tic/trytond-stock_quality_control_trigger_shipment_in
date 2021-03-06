==================================================================
Quality Control Trigger by Shipment on Supplier Shipments Scenario
==================================================================

=============
General Setup
=============

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date.today()

Install stock_quality_control_trigger_shipment_in::

    >>> config = activate_modules('stock_quality_control_trigger_shipment_in')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create supplier and customer::

    >>> Party = Model.get('party.party')
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()
    >>> customer = Party(name='Customer')
    >>> customer.save()

Create products::

    >>> ProductUom = Model.get('product.uom')
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> product1 = Product()
    >>> template1 = ProductTemplate()
    >>> template1.name = 'Product 1'
    >>> template1.default_uom = unit
    >>> template1.type = 'goods'
    >>> template1.list_price = Decimal('20')
    >>> template1.save()
    >>> product1.template = template1
    >>> product1.save()
    >>> product2 = Product()
    >>> template2 = ProductTemplate()
    >>> template2.name = 'Product 2'
    >>> template2.default_uom = unit
    >>> template2.type = 'goods'
    >>> template2.list_price = Decimal('20')
    >>> template2.save()
    >>> product2.template = template2
    >>> product2.save()

Create Quality Configuration::

    >>> Sequence = Model.get('ir.sequence')
    >>> Configuration = Model.get('quality.configuration')
    >>> ConfigLine = Model.get('quality.configuration.line')
    >>> IrModel = Model.get('ir.model')
    >>> sequence = Sequence.find([('code','=','quality.test')])[0]
    >>> product_model, = IrModel.find([('model','=','product.product')])
    >>> shipment_in_model, = IrModel.find([('model','=','stock.shipment.in')])
    >>> configuration = Configuration()
    >>> product_config_line = ConfigLine()
    >>> configuration.allowed_documents.append(product_config_line)
    >>> product_config_line.quality_sequence = sequence
    >>> product_config_line.document = product_model
    >>> shipment_in_config_line = ConfigLine()
    >>> configuration.allowed_documents.append(shipment_in_config_line)
    >>> shipment_in_config_line.quality_sequence = sequence
    >>> shipment_in_config_line.document = shipment_in_model
    >>> configuration.save()

Create Templates related to Product 1 with Shipments as Trigger model and
Generated model::

    >>> Template = Model.get('quality.template')
    >>> template = Template()
    >>> template.name = 'Template Supplier Shipments'
    >>> template.document = product1
    >>> template.internal_description='Quality Control on Supplier Shipments'
    >>> template.external_description='External description'
    >>> template.trigger_model = 'stock.shipment.in'
    >>> template.trigger_generation_model = 'stock.shipment.in'
    >>> template.save()

Get stock locations and create new internal location::

    >>> Location = Model.get('stock.location')
    >>> warehouse_loc, = Location.find([('code', '=', 'WH')])
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])
    >>> input_loc, = Location.find([('code', '=', 'IN')])
    >>> output_loc, = Location.find([('code', '=', 'OUT')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])
    >>> internal_loc = Location()
    >>> internal_loc.name = 'Internal Location'
    >>> internal_loc.code = 'INT'
    >>> internal_loc.type = 'storage'
    >>> internal_loc.parent = storage_loc
    >>> internal_loc.save()

Create Shipment In::

    >>> ShipmentIn = Model.get('stock.shipment.in')
    >>> shipment_in = ShipmentIn()
    >>> shipment_in.planned_date = today
    >>> shipment_in.supplier = supplier
    >>> shipment_in.warehouse = warehouse_loc

Add three shipment lines of product 1 and one of product 2::

    >>> StockMove = Model.get('stock.move')
    >>> shipment_in.incoming_moves.extend([StockMove(), StockMove(),
    ...         StockMove()])
    >>> for move in shipment_in.incoming_moves:
    ...     move.product = product1
    ...     move.uom = unit
    ...     move.quantity = 1
    ...     move.from_location = supplier_loc
    ...     move.to_location = input_loc
    ...     move.unit_price = Decimal('1')
    >>> move = StockMove()
    >>> shipment_in.incoming_moves.append(move)
    >>> move.product = product2
    >>> move.uom = unit
    >>> move.quantity = 3
    >>> move.from_location = supplier_loc
    >>> move.to_location = input_loc
    >>> move.unit_price = Decimal('1')
    >>> shipment_in.save()

Receive products::

    >>> ShipmentIn.receive([shipment_in.id], config.context)
    >>> shipment_in.reload()
    >>> shipment_in.state
    'received'
    >>> list(set([m.state for m in shipment_in.incoming_moves]))
    ['done']

Check the created Quality Tests::

    >>> QualityTest = Model.get('quality.test')
    >>> tests_in, = QualityTest.find([])
    >>> tests_in.document == shipment_in
    True
