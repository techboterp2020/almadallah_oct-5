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

from odoo import models, fields, _
from odoo.exceptions import UserError


class AssignUser(models.Model):
    _name = "assign.user.wiz"
    _description = "Assigned User"

    user_id = fields.Many2one('res.users', string="Assigned User", required=True)

    # Method for assigning new users to the ticket
    def assign_user_tickets(self):
        record_list = self._context.get('active_ids')
        tck_list = []
        for rec in record_list:
            ticket = self.env['helpdesk.ticket'].browse(rec)
            if ticket.team_id.assign_method == 'balanced' or ticket.team_id.privacy == 'invite':
                if self.user_id not in ticket.team_id.member_ids or self.user_id not in ticket.team_id.visibility_member_ids:
                    tck_list.append(ticket.name)
                else:
                    ticket.user_id = self.user_id.id
            else:
                ticket.user_id = self.user_id.id
        if tck_list:
            raise UserError(_('User "%s" not in helpdesk team of following tickets %s', self.user_id.name, tck_list))
