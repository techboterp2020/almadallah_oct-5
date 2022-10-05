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
import base64
import io
from odoo import api, fields, models
# from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class HelpDeskTeamTicketXlsxReport(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_team_ticket_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Abstract  Team Ticket  XLSX Report"

    @api.model
    def get_help_desk_data(self, data):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        users = self.env['res.users'].search([])
        data = []
        for user in users:
            domain_total_user_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to),
                                        ('user_id', '=', user.id)]

            domain_sla_lapsed_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                        ('stage_id.is_close', '=', False), ('ticket_overdue', '=', True),
                                        ('user_id', '=', user.id)]
            domain_non_sla_lapsed_ticket = [('non_sla_dead_line', '>=', date_from),
                                            ('non_sla_dead_line', '<=', date_to),
                                            ('sla_deadline', '=', False), ('ticket_overdue', '=', True),
                                            ('stage_id.is_close', '=', False),
                                            ('user_id', '=', user.id)]

            domain_attended_non_sla_ticket = [('non_sla_dead_line', '>=', date_from),
                                              ('non_sla_dead_line', '<=', date_to), ('stage_id.is_close', '=', True),
                                              ('sla_deadline', '=', False),
                                              ('user_id', '=', user.id)]
            domain_attended_sla_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                          ('stage_id.is_close', '=', True), ('sla_deadline', '=', False),
                                          ('user_id', '=', user.id)]
            users = self.env['helpdesk.ticket'].search([('user_id', '=', user.id)])

            if users:
                no_of_user_ticket_recs = (self.env['helpdesk.ticket'].search_count(domain_total_user_ticket))
                total_ticket_recs = no_of_user_ticket_recs

                # Lapsed Tickets detail
                lapsed_sla_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_sla_lapsed_ticket)
                print(10 * 'Lapsed Sla:', lapsed_sla_ticket_recs)
                lapsed_non_sla_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_non_sla_lapsed_ticket)
                print(10 * 'Non Lapsed Sla:', lapsed_non_sla_ticket_recs)
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

    def generate_xlsx_report(self, workbook, data, tickets):
        # print(data,'12356******************************7896555')
        worksheet = workbook.add_worksheet('Team Ticket report ')
        bold = workbook.add_format({'bold': True, 'align': 'left'})
        text = workbook.add_format({'font_size': 12, 'align': 'center'})
        top_heading = workbook.add_format(
            {'bold': True, 'font_size': 18, 'align': 'center', 'valign': 'vcenter', 'font_color': '915e4c'})
        heading = workbook.add_format(
            {'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'bg_color': '915e4c',
             'font_color': 'FFFFFF'})
        # Assign Column Width
        worksheet.set_column("A:A", 13)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 16)
        worksheet.set_column("D:D", 25)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)

        worksheet.merge_range('A1:F3', "Team Tickets Report", top_heading)
        worksheet.write('A5', 'From Date : ', bold)
        from_dt = data['form']['date_from']
        # from_dt is string then we want to convert string into date time
        dt_f = datetime.fromisoformat(str(from_dt))
        new_date_from = datetime.strftime((dt_f + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write('B5', new_date_from)

        worksheet.write('E5', 'End Date : ', bold)
        to_dt = data['form']['date_to']
        dt_to = datetime.fromisoformat(str(to_dt))
        new_date_to = datetime.strftime((dt_to + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write('F5', new_date_to)
        # Assign helpdesk date into new data
        new_data = self.get_help_desk_data(data)

        row = 6
        heading_list = ["SL No.", "User Name", "Total Tickets", "Attended with TAT", "TAT Lapsed", "Serviced (%)"]
        for column in range(len(heading_list)):
            worksheet.write(row, column, heading_list[column], heading)

        sl_no = 1
        row = 7
        column = 0
        for tickets in new_data['complete_recs']:
            worksheet.write(row, column, sl_no, text)
            worksheet.write(row, column + 1, tickets['user'], text)
            worksheet.write(row, column + 2, tickets['total'], text)
            worksheet.write(row, column + 3, tickets['attended'], text)
            worksheet.write(row, column + 4, tickets['lapsed'], text)
            worksheet.write(row, column + 5, tickets['service_perc'], text)
            sl_no += 1
            row += 1
