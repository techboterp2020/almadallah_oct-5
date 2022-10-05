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
from odoo import models, fields, api, SUPERUSER_ID
import time
from datetime import datetime
from datetime import time as datetime_time
from odoo.exceptions import ValidationError


class HelpdeskTicketReportWiz(models.TransientModel):
    _name = "helpdesk.ticket.report.wizard"
    _description = "Helpdesk Ticket wizard "

    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To', default=fields.Datetime.now, readonly=True)
    team_id = fields.Many2one('helpdesk.team', string='Team')
    partner_id = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='Assigned To')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    stage_id = fields.Many2one('helpdesk.stage', string='Stage', domain=[('is_close', '=', False)])

    def generate_report(self):
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'team_id', 'user_id', 'partner_id', 'company_id', 'stage_id'])[0]
        return self.env.ref('techboterp_scheduled_action.action_report_helpdesk_ticket_timeover').report_action(self, data=data)

    def generate_excel_report(self):
        # print('************************************************')
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'team_id', 'user_id', 'partner_id', 'company_id', 'stage_id'])[0]
        return self.env.ref('techboterp_scheduled_action.action_report_helpdesk_ticket_timeover_xlsx').report_action(
            self, data=data)

    @api.constrains('date_from', 'date_to')
    def _check_ending_date(self):
        """ Method to Restrict dates b/w date form and date_to """
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError('The From Date Should not be Greater than the To Date.')
