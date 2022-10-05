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


class MergeTicketWzd(models.Model):
    _name = "merge.ticket.wiz"
    _description = "Merge Ticket Wizard"

    # method to get customer from the current ticket to wizard
    @api.model
    def default_get(self, fields):
        result = super(MergeTicketWzd, self).default_get(fields)
        ticket = self.env['helpdesk.ticket'].browse(self.env.context.get('active_id'))
        result['partner_id'] = ticket.partner_id.id
        return result

    partner_id = fields.Many2one('res.partner', required=True, readonly=True, string="Customer")
    ticket_ids = fields.Many2many('helpdesk.ticket')

    # button method to merge the selected tickets

    def merge_tickets(self):
        ticket = self.env['helpdesk.ticket'].browse(self.env.context.get('active_id'))
        for tickets in self.ticket_ids:
            ticket.write({
                'tag_ids': [(4, i.id) for i in tickets.tag_ids],
                'message_ids': [(4, i.id) for i in tickets.message_ids],
                'activity_ids': tickets.activity_ids.ids,
                'is_merge': True,
            })
            tickets.unlink()
