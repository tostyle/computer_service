# -*- coding: utf-8 -*-
from openerp import http

# class ComputerService(http.Controller):
#     @http.route('/computer_service/computer_service/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/computer_service/computer_service/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('computer_service.listing', {
#             'root': '/computer_service/computer_service',
#             'objects': http.request.env['computer_service.computer_service'].search([]),
#         })

#     @http.route('/computer_service/computer_service/objects/<model("computer_service.computer_service"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('computer_service.object', {
#             'object': obj
#         })