import time
import pytz

from datetime import datetime
from openerp import models, fields, api

def _select_nextval(cr, seq_name,sequence_code,contextID):
    # cr.execute("SELECT nextval('%s')" % seq_name)
    sql = "SELECT cast(substring(MAX(name),11,5) as int)+1 AS NextID FROM %(table_name)s where user_company='%(company)s'" % { "table_name" : sequence_code, "company" : contextID }
    if contextID is None:
        sql = "SELECT nextval('%s')" % seq_name
    print 'qwurerrrrrrrrrrrrrrrrrrr'
    print sql
    cr.execute(sql)
    return cr.fetchone()

class ComputerSequence(models.Model):
    _inherit  = 'ir.sequence'
    # _name = 'comservice.com_sequence'
    @api.model
    def next_by_code(self, sequence_code,contextID=None):
        """ Draw an interpolated string using a sequence with the requested code.
            If several sequences with the correct code are available to the user
            (multi-company cases), the one from the user's current company will
            be used.

            :param dict context: context dictionary may contain a
                ``force_company`` key with the ID of the company to
                use instead of the user's current company for the
                sequence selection. A matching sequence for that
                specific company will get higher priority.
        """
        self.check_access_rights('read')
        company_ids = self.env['res.company'].search([]).ids + [False]
        seq_ids = self.search(['&', ('code', '=', sequence_code), ('company_id', 'in', company_ids)])
        real_tablename = sequence_code.replace(".","_")
        if not seq_ids:
            return False
        force_company = self.env.context.get('force_company')
        if not force_company:
            force_company = self.env.user.company_id.id
        preferred_sequences = [s for s in seq_ids if s.company_id and s.company_id.id == force_company]
        seq_id = preferred_sequences[0] if preferred_sequences else seq_ids[0]
        return seq_id._next(sequence_code=real_tablename,contextID=contextID)

    def _next(self,sequence_code,contextID):
        """ Returns the next number in the preferred sequence in all the ones given in self."""
        if not self.use_date_range:
            return self._next_do(sequence_code=sequence_code,contextID=contextID)
        # date mode
        dt = fields.Date.today()
        if self.env.context.get('ir_sequence_date'):
            dt = self.env.context.get('ir_sequence_date')
        seq_date = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_from', '<=', dt), ('date_to', '>=', dt)], limit=1)
        if not seq_date:
            seq_date = self._create_date_range_seq(dt)
        return seq_date.with_context(ir_sequence_date_range=seq_date.date_from)._next()

    def _next_do(self,sequence_code,contextID):
        if self.implementation == 'standard':
            number_next = _select_nextval(self.env.cr, 'ir_sequence_%03d' % self.id ,sequence_code=sequence_code,contextID=contextID)
            print number_next
            print "fffffffffffff"
            if number_next[0] is None:
                number_next = (1,)
        else:
            number_next = _update_nogap(self, self.number_increment)
        return self.get_next_char(number_next,contextID)

    def get_next_char(self, number_next,context):
        if context is None:
            context = ''
        def _interpolate(s, d):
            if s:
                return s % d
            return ''

        def _interpolation_dict():
            now = range_date = effective_date = datetime.now(pytz.timezone(self.env.context.get('tz') or 'UTC'))
            if self.env.context.get('ir_sequence_date'):
                effective_date = datetime.strptime(self.env.context.get('ir_sequence_date'), '%Y-%m-%d')
            if self.env.context.get('ir_sequence_date_range'):
                range_date = datetime.strptime(self.env.context.get('ir_sequence_date_range'), '%Y-%m-%d')

            sequences = {
                'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
                'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
            }
            res = {}
            for key, sequence in sequences.iteritems():
                res[key] = effective_date.strftime(sequence)
                res['range_' + key] = range_date.strftime(sequence)
                res['current_' + key] = now.strftime(sequence)

            return res

        d = _interpolation_dict()
        try:
            interpolated_prefix = _interpolate(self.prefix, d)
            interpolated_suffix = _interpolate(self.suffix, d)
        except ValueError:
            raise UserError(_('Invalid prefix or suffix for sequence \'%s\'') % (self.get('name')))
        print 'check'
        print interpolated_prefix
        print context
        print self.padding
        print number_next
        print interpolated_suffix
        return interpolated_prefix + context + '%%0%sd' % self.padding % number_next + interpolated_suffix
