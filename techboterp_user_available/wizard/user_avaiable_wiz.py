# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models,fields,api, SUPERUSER_ID
import time
from datetime import datetime,date

class UserAvailableWiz(models.TransientModel):
    _name = "user.available.wiz"
    _description = "User Available"
    _rec_name = "user_id"
    
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    available = fields.Boolean(string='Available')
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        for rec in self:
            rec.available = False
            if rec.user_id:
                rec.available = rec.user_id.user_available 
    
    def user_available(self):
        for rec in self:
            if rec.user_id:
                availability = self.env['helpdesk.user.availability'].create({'user_id':rec.user_id.id,
                                                               'created_date_help':date.today(),
                                                               'check_in':datetime.now()})
                rec.user_id.sudo().write({'user_available':True,
                                          'last_availblity_id':availability.id})
                
    def user_not_available(self):
         for rec in self:
            if rec.user_id:
                rec.user_id.sudo().write({'user_available':False})
                if rec.user_id.last_availblity_id:
                    rec.user_id.last_availblity_id.check_out= datetime.now()
                    rec.user_id.sudo().write({'last_availblity_id':False})
