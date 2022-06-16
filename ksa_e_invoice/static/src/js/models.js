odoo.define("ksa_e_invoice.models", function (require) {
"use strict";

var models = require('point_of_sale.models');

models.load_fields('res.company', ['street','street2','city','state_id','vat']);
models.load_fields('product.product',['name']);
})

