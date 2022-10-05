# -*- coding: utf-8 -*-
##############################################################################
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
from dateutil.relativedelta import relativedelta


class ReportHelpdeskOverallTicket(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_helpdesk_all_ticket'
    _description = "Based on Daily Abstract PDF Report"

    @api.model
    def get_help_desk_data(self, data):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        data = []
        domain_total_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to)]
        no_of_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_total_ticket)

        # Closed Ticket Details
        domain_attended_non_sla_ticket = [('non_sla_dead_line', '>=', date_from), ('non_sla_dead_line', '<=', date_to),
                                          ('stage_id.is_close', '=', True), ('sla_deadline', '=', False)]
        no_of_non_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_non_sla_ticket)

        domain_attended_sla_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                      ('stage_id.is_close', '=', True)]
        no_of_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_sla_ticket)

        attended_with_tat = (no_of_sla_attended + no_of_non_sla_attended)

        #     UN Closed Ticket
        domain_sla_overdue = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                              ('stage_id.is_close', '=', False)]
        total_exceeding_sla = self.env['helpdesk.ticket'].search_count(domain_sla_overdue)
        # ('********************Exceeding SLA ******************',total_exceeding_sla)
        domain_non_sla_overdue = [('non_sla_dead_line', '>=', date_from), ('non_sla_dead_line', '<=', date_to),
                                  ('sla_deadline', '=', False), ('stage_id.is_close', '=', False)]
        total_exceeding_non_sla = self.env['helpdesk.ticket'].search_count(domain_non_sla_overdue)
        # ("**********Exceeding Non Sla*******************", total_exceeding_non_sla)
        total_exceeding_ticket = (total_exceeding_non_sla + total_exceeding_sla)
        if no_of_ticket_recs > 0:
            total_exceeding_ticket_avg = round((total_exceeding_ticket / no_of_ticket_recs) * 100, 2)
        else:
            total_exceeding_ticket_avg = 0.0

        # Time Taken
        total_sla_time_taken = self.env['helpdesk.ticket'].search(domain_attended_sla_ticket)
        total_non_time_taken = self.env['helpdesk.ticket'].search(domain_attended_non_sla_ticket)

        sum_attended_sla_time = sum((time['closed_ticket_time_in_hour'] for time in total_sla_time_taken))
        sum_attended_non_time = sum((time['closed_ticket_time_in_hour'] for time in total_non_time_taken))

        total_time_taken = round(sum_attended_sla_time + sum_attended_non_time, 2)

        user_data = {'total': no_of_ticket_recs, 'attended_tat': attended_with_tat,
                     'exceeding_ticket': total_exceeding_ticket,
                     'exceeding_avg': total_exceeding_ticket_avg, 'time_taken': total_time_taken}

        data.append(user_data)

        return {'complete_recs': data,
                'from_date': date_from,
                'to_date': date_to}

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(self.get_help_desk_data(data))
        return data
