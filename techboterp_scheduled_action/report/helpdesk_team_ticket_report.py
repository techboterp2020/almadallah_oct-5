# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ReportHelpDeskTeamTicket(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_helpdesk_team_ticket'
    _description = "Based on Abstract Team  PDF Report"

    @api.model
    def get_help_desk_data(self, data):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        users = self.env['res.users'].search([])
        data = []
        for user in users:
            # domain_total_sla_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to),('user_id', '=', user.id)]
            # domain_total_nonsla_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to),('user_id', '=', user.id)]

            domain_total_user_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to),
                                        ('user_id', '=', user.id)]

            domain_sla_lapsed_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                        ('stage_id.is_close', '=', False), ('ticket_overdue', '=', True),
                                        ('user_id', '=', user.id)]
            domain_non_sla_lapsed_ticket = [('non_sla_dead_line', '>=', date_from),('non_sla_dead_line', '<=', date_to),
                                            ('sla_deadline', '=', False), ('ticket_overdue', '=', True),
                                            ('stage_id.is_close', '=', False), ('user_id', '=', user.id)]

            domain_attended_non_sla_ticket = [('non_sla_dead_line', '>=', date_from),
                                              ('non_sla_dead_line', '<=', date_to), ('stage_id.is_close', '=', True),
                                              ('sla_deadline', '=', False), ('user_id', '=', user.id)]
            domain_attended_sla_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                          ('stage_id.is_close', '=', True), ('sla_deadline', '=', False),
                                          ('user_id', '=', user.id)]
            users = self.env['helpdesk.ticket'].search([('user_id', '=', user.id)])

            if users:
                no_of_user_ticket_recs = (self.env['helpdesk.ticket'].search_count(domain_total_user_ticket))
                total_ticket_recs = no_of_user_ticket_recs

                # Lapsed Tickets detail
                lapsed_sla_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_sla_lapsed_ticket)

                lapsed_non_sla_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_non_sla_lapsed_ticket)
                # print('*********************** Non Sla Lapsed****************************', lapsed_non_sla_ticket_recs)

                total_lapsed = (lapsed_sla_ticket_recs + lapsed_non_sla_ticket_recs)

                # Closed Ticket Details
                total_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_sla_ticket)
                total_non_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_non_sla_ticket)
                attended_with_tat = (total_sla_attended + total_non_sla_attended)

                if total_ticket_recs > 0:
                    service_percentage = round((attended_with_tat / total_ticket_recs) * 100, 2)
                else:
                    service_percentage = 0.0

                user_data = {'user': user.name, 'total': total_ticket_recs, 'attended': attended_with_tat,
                             'lapsed': total_lapsed, 'service_perc': service_percentage}
                data.append(user_data)

        return {'complete_recs': data,
                'from_date': date_from,
                'to_date': date_to}

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(self.get_help_desk_data(data))
        return data
