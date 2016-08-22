# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv
from openerp.report import report_sxw
class ComputerSummary(models.TransientModel):
    _name = 'comservice.com_summary'
    requester_ids = fields.Many2many('comservice.requester', string="Requesters")
    # @api.one
    def show_report(self, cr, uid, ids, context=None):
      if context is None:
          context = {}
      res = self.read(cr, uid, ids,['requester_ids'], context=context)
      res = res and res[0] or {}
      datas={'ids': "eeeeeeeeeeeeeeeeee"}
      datas['form'] = res
      datas['ids'] = "222222222222222222222"
    #   print datas['form'][0]['requester_ids'][0]
      print "xxxxxxxxxxxxxxxxxxxxxxxxxxcccccccccccccccccccccccccccccccccccc"
      return self.pool['report'].get_action(cr, uid, [], 'computer_service.report_summary_requester', data=datas, context=context)

class summary_requester(report_sxw.rml_parse):
    def _get_requester_detail(self,requester_ids):
        requester = self.pool.get('comservice.requester')
        requester_list = requester.browse(self.cr, self.uid, requester_ids)
        print requester_list
        print 'get functionnnn'
        # return requester_list
        return ', '.join(map(lambda x: x.name, requester_list ) )
    def _get_requester_list(self,requester_ids):
        requester = self.pool.get('comservice.requester')
        requester_list = requester.browse(self.cr, self.uid, requester_ids)
        return requester_list
    def _get_received_list(self,requester_ids):
        receivedCom = self.pool.get('comservice.com_receive')
        received_ids = receivedCom.search(self.cr, self.uid, [ ('user_request_id','in',requester_ids) ] )
        received_list = receivedCom.browse(self.cr, self.uid, received_ids)
        return received_list
    def _get_returned_forms(self,requester_ids):
        returnedCom = self.pool.get('comservice.com_return')
        returned_ids = returnedCom.search(self.cr, self.uid, [ ('user_request_id','in',requester_ids) ] )
        returned_list = returnedCom.browse(self.cr, self.uid, returned_ids)
        return returned_list
    def __init__(self, cr, uid, name, context):
        super(summary_requester, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'getRequesterDetail': self._get_requester_detail,
            'getRequesterList': self._get_requester_list,
            'getReceivedList': self._get_received_list,
            'getReturnedList': self._get_returned_forms,
        })

class report_summary_requester(osv.AbstractModel):
    _name = 'report.computer_service.report_summary_requester'
    _inherit = 'report.abstract_report'
    _template = 'computer_service.report_summary_requester'
    _wrapped_report_class = summary_requester
