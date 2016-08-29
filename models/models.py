# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Requester(models.Model):
    _name = 'comservice.requester'

    name = fields.Char(string="Fullname")
    # user_request = fields.Char(string="Request By")
    user_code = fields.Char(string="Employee Code")
    user_tel = fields.Char(string="Internal Tel.")
    user_company = fields.Char(string="Company")
    user_division = fields.Char(string="Division")
    user_section = fields.Char(string="Section")

class ComputerRequest(models.Model):
    _name = 'comservice.com_request'

    name = fields.Char()
    remark = fields.Char()
    user_request = fields.Char(string="Request By")
    user_company = fields.Char(string="Company",required=True)
    description = fields.Text(string="Description")
    user_request_id = fields.Many2one('comservice.requester',
        ondelete='set null', string="Request By", index=True)
    program_ids = fields.Many2many(
        'comservice.com_program', string="Programs")

class ComputerReceive(models.Model):
    _inherit  = 'comservice.com_request'
    _name = 'comservice.com_receive'
    equipment_ids = fields.One2many('comservice.com_request_equipment', 'receive_id', string="Equipments")
    returned_id = fields.Many2one('comservice.com_return',
         ondelete='set null', string="Returned Computer", index=True)
    returned_ids = fields.Many2many('comservice.com_return', string="Return Forms")
    requested_company = fields.Char(string="Requested Company" ,related="user_request_id.user_company")
    def get_remain_index(self,indexs,programType):
        indexs[programType] = indexs[programType] + 1
        return indexs
    def get_remain_type_index(self,indexs,programType):
        print indexs
        print programType
        return range(7 - indexs[programType])
    # @api.one
    # def revise_form(self):
    @api.model
    def revise_form(self,vals):
    # def revise_form(self, cr, uid, ids, context=None):
        modeldetail = self.browse(vals)
        tempID = modeldetail.name
        sql = "SELECT MAX(CASE WHEN position('-' IN right(name,2) ) =1 THEN CONCAT(substr('%(format_str1)s',1,13),'-', CAST(right(name,1) AS integer)+1) ELSE  CONCAT(substr('%(format_str2)s',1,13),'-1') END) AS reviseID FROM comservice_com_receive  WHERE name  LIKE concat(substr('%(format_str3)s',1,13),'%%')" % { "format_str1" : tempID, "format_str2" : tempID ,"format_str3" : tempID}
        print sql
        tempQuery = self.env.cr
        tempQuery.execute(sql)
        nextID =  tempQuery.fetchone()
        print nextID[0]
        # vals = {'name': nextID[0],'user_company' : self.user_company}
        newForm = self.create({'name': nextID[0],'user_company' : modeldetail.user_company})
        # return super(ComputerReceive, self).create(vals)

        print "rerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"
        print self.id
        print newForm.id
        # return super(ComputerReceive, newForm)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Received Computer',
            'res_model': 'comservice.com_receive',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': newForm.id,
            'target' : 'current'
            }
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            company = vals['user_company']
            vals['name'] = self.env['ir.sequence'].next_by_code('comservice.com_receive',company) or '/'
        return super(ComputerReceive, self).create(vals)

class ComputerReturn(models.Model):
    _inherit  = 'comservice.com_request'
    _name = 'comservice.com_return'
    equipment_ids = fields.One2many('comservice.com_request_equipment', 'return_id',string="Equipments")
    received_ids = fields.Many2many('comservice.com_receive', string="Receive Forms")
    received_id = fields.Many2one('comservice.com_receive',
         ondelete='set null', string="Received Computer")
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            company = vals['user_company']
            vals['name'] = self.env['ir.sequence'].next_by_code('comservice.com_return',company) or '/'
        return super(ComputerReturn, self).create(vals)

    @api.onchange('received_ids')
    def _get_received_form_detail(self):
        if len(self.received_ids) :
            self.user_company=self.received_ids[0].user_company
            for received_id in self.received_ids:
                print(type(received_id))
                print(received_id.equipment_ids)
                print('==============')
                print(type(self.equipment_ids))
                print(self.equipment_ids)
                print('==================')
                self.equipment_ids =self.equipment_ids + received_id.equipment_ids
                # self.program_ids =self.received_ids.program_ids

class ComputerProgram(models.Model):
     _name = 'comservice.com_program'
     name = fields.Char()
     version = fields.Char()
     program_type = fields.Selection(( ('freeware','Freeware'),('license','License') ), 'Program Type')
     request_ids = fields.Many2many('comservice.com_request', string="Programs")


class ComputerEquipment(models.Model):
    _name = 'comservice.com_equipment'
    name = fields.Char(string="Equipment Name")
    modelName = fields.Char(string="Model")
    brand = fields.Char()
    type_id = fields.Many2one('comservice.com_equipment_type',
         ondelete='set null', string="Equipment Type", index=True)
    program_ids = fields.Many2many('comservice.com_repair', string="Repairs")
    # @api.multi
    # def name_get(self):
    #     result = []
    #     name = self._rec_name
    #     brand = 'brand'
    #     typeName = 'type_id'
    #     if typeName in self._fields:
    #         convertTypeName = self._fields[typeName].convert_to_display_name
    #     if brand in self._fields:
    #         convertBrand = self._fields[brand].convert_to_display_name
    #     if name in self._fields:
    #         convertName = self._fields[name].convert_to_display_name
    #     for record in self:
    #         displayname = convertTypeName(record[typeName], record) + " " + convertBrand(record[brand], record) + " " + convertName(record[name], record)
    #         result.append((record.id,displayname))

    #     return result

class ComputerEquipmentType(models.Model):
    _name = 'comservice.com_equipment_type'
    name = fields.Char(string="Equipment Type")
    # shortname = fields.Char()
    # _rec_name ='shortname'
    equipment_ids = fields.One2many('comservice.com_equipment',
         'type_id', string="Equipment List")
    # @api.multi
    # def name_get(self):
    #     print self
    #     result = []
    #     name = self._rec_name
    #     fullname = 'name'
    #     if name in self._fields:
    #         convert = self._fields[name].convert_to_display_name
    #     if fullname in self._fields:
    #         convert2 = self._fields[fullname].convert_to_display_name
    #         for record in self:
    #             displayname = convert(record[name], record) + convert2(record[fullname], record)
    #             result.append((record.id,displayname))

    #     return result

class ComputerRequestEquipment(models.Model):
    _name = 'comservice.com_request_equipment'
    quantity = fields.Integer(default=1)
    serial = fields.Char(string="Serial No")
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="Ram")
    hdd = fields.Char(string="Harddisk")
    isBroken = fields.Boolean(string="isBroken")
    equipment_id = fields.Many2one('comservice.com_equipment',
        ondelete='set null', string="Equipment", index=True)
    receive_id = fields.Many2one('comservice.com_receive',
        ondelete='set null', string="Receive Form", index=True)
    return_id = fields.Many2one('comservice.com_return',
        ondelete='set null', string="Return Form", index=True)

class ComputerRepair(models.Model):
    _name = 'comservice.com_repair'
    name = fields.Char()
    serial = fields.Char()
    equipment_ids = fields.Many2many('comservice.com_equipment', string="Programs")
    return_id = fields.Many2one('comservice.com_return',
        ondelete='set null', string="Return Form", index=True)
