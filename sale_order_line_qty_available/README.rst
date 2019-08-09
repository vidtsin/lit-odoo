=============================
Sale order line qty available
=============================

This module adds qty available to a sales order lines.


Usage
=====

Warning for salespersons
------------------------
If you want to keep salespersons from concluding sales that you may not be able to deliver,
you may block the quotations using the module sale_exceptions_ .
Once this module is installed, go to "Sales > Configuration > Sales > Exceptions rules" and create a new rule using the following code:

.. code-block:: python

    if line.product_id and line.product_id.type == 'product' and (line.immediately_usable_qty - line.min_stock_qty) > line.product_uom_qty:
        failed=True


.. _sale_exceptions: https://www.odoo.com/apps/modules/8.0/sale_exceptions/


