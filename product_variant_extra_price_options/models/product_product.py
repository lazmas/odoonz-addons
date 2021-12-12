# Copyright 2021 Graeme Gellatly, O4SB Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):

    _inherit = "product.product"

    def _compute_product_price_extra(self):
        """Replaces method to set current_attributes_price_extra
        based on the price_extra methods
        @note: This makes this currently incompatible with price change module
        """
        for product in self:
            ptavs = product.product_template_attribute_value_ids
            product.price_extra = sum(self._compute_price_extra_from_ptavs(ptavs))

    def _compute_price_extra_from_ptavs(self, ptavs):
        """ Computes Price Extra by dispatching to ptavs price_extra_method
        """
        price_extra_dict = {pev.attribute_id.id: pev.price_extra for pev in ptavs}
        for ptav in ptavs:
            try:
                price_extra_dict = getattr(ptav, "_calc_%s" % ptav.price_extra_method)(
                    price_extra_dict
                )
            except AttributeError:
                continue
        return price_extra_dict.values()
