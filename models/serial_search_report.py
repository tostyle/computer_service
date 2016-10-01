# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv
from openerp.report import report_sxw
class ComputerSerialSearch(models.TransientModel):
    _name = 'comservice.com_serial_search'
    serial_search = fields.Char(string="Serial No")

    def show_report(self, cr, uid, ids, context=None):
      if context is None:
          context = {}
      res = self.read(cr, uid, ids,['serial_search'], context=context)
      res = res and res[0] or {}
      datas = {}
      datas['form'] = res
      return self.pool['report'].get_action(cr, uid, [], 'computer_service.report_summary_serial', data=datas, context=context)

class summary_serial(report_sxw.rml_parse):
    def _get_com_request_by_serial(self,search_serialNo):
        request_equipment = self.pool.get('comservice.com_request_equipment')
        equipments = request_equipment.search(self.cr, self.uid, [ ('serial','=',search_serialNo) ] )
        equipment_list = request_equipment.browse(self.cr, self.uid, equipments)
        return equipment_list
    # def _get_com_receive_by_serial(self,search_serialNo):
    def __init__(self, cr, uid, name, context):
        super(summary_serial, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'getComRequestBySerial': self._get_com_request_by_serial,
        })

class report_summary_serial(osv.AbstractModel):
    _name = 'report.computer_service.report_summary_serial'
    _inherit = 'report.abstract_report'
    _template = 'computer_service.report_summary_serial'
    _wrapped_report_class = summary_serial
