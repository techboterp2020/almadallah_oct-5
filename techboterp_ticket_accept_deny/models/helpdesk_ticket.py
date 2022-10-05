
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


from odoo import models, fields, api
from datetime import datetime,date


class InheritHelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    #adding accept button in helpdesk ticket list view

    @api.model
    def user_accept_ticket(self):
        availability = self.env['helpdesk.user.availability'].create({'user_id': self.env.user.id,
                                                                      'created_date_help': date.today(),
                                                                      'check_in': datetime.now()})
        self.env.user.sudo().write({'user_available': True,
                                      'last_availblity_id': availability.id})
        return True


    # adding decline button in helpdesk ticket list view

    @api.model
    def user_decline_ticket(self):
        self.env.user.sudo().write({'user_available': False})
        if self.env.user.last_availblity_id:
            self.env.user.last_availblity_id.check_out = datetime.now()
            self.env.user.sudo().write({'last_availblity_id': False})
        return False


    @api.model
    def accept_deny_val(self):
        return self.env.user.user_available