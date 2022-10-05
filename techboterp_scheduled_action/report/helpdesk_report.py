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
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class ReportHelpDeskOverDeadline(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_helpdesk_ticket'
    _description = "Abstract PDF Report"

    @api.model
    def get_help_desk_data(self, data):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        user_id = data['form']['user_id']
        team_id = data['form']['team_id']
        partner_id = data['form']['partner_id']
        stage_id = data['form']['stage_id']
        domain_sla = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                      ('stage_id.is_close', '=', False)]
        domain_non_sla = [('non_sla_dead_line', '>=', date_from), ('non_sla_dead_line', '<=', date_to),
                          ('stage_id.is_close', '=', False), ('sla_deadline', '=', False)]

        if user_id:
            domain_sla.append(('user_id', '=', user_id[0]))
            domain_non_sla.append(('user_id', '=', user_id[0]))
        if team_id:
            domain_sla.append(('team_id', '=', team_id[0]))
            domain_non_sla.append(('team_id', '=', team_id[0]))
        if partner_id:
            domain_sla.append(('partner_id', '=', partner_id[0]))
            domain_non_sla.append(('partner_id', '=', partner_id[0]))
        if stage_id:
            domain_sla.append(('stage_id', '=', stage_id[0]))
            domain_non_sla.append(('stage_id', '=', stage_id[0]))

        sla_ticket_recs = self.env['helpdesk.ticket'].search(domain_sla)
        non_sla_ticket_recs = self.env['helpdesk.ticket'].search(domain_non_sla)

        return {'complete_recs': sla_ticket_recs | non_sla_ticket_recs,
                'from_date': date_from,
                'to_date': date_to}


    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(self.get_help_desk_data(data))
        return data
