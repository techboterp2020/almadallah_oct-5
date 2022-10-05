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


class HelpDeskOverAllXlsxReport(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_overall_ticket_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Abstract Ticket Over All XLSX Report"

    @api.model
    def get_helpdesk_overall_ticket_data(self, data):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        data = []
        domain_total_ticket = [('created_on', '>=', date_from), ('created_on', '<=', date_to)]
        no_of_ticket_recs = self.env['helpdesk.ticket'].search_count(domain_total_ticket)

        # Closed Ticket Details
        domain_attended_non_sla_ticket = [('non_sla_dead_line', '>=', date_from),
                                          ('non_sla_dead_line', '<=', date_to), ('stage_id.is_close', '=', True),
                                          ('sla_deadline', '=', False)]
        no_of_non_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_non_sla_ticket)

        domain_attended_sla_ticket = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                                      ('stage_id.is_close', '=', True)]
        no_of_sla_attended = self.env['helpdesk.ticket'].search_count(domain_attended_sla_ticket)

        attended_with_tat = (no_of_sla_attended + no_of_non_sla_attended)

        #     UN Closed Ticket
        domain_sla_overdue = [('sla_deadline', '>=', date_from), ('sla_deadline', '<=', date_to),
                              ('stage_id.is_close', '=', False)]
        total_exceeding_sla = self.env['helpdesk.ticket'].search_count(domain_sla_overdue)

        domain_non_sla_overdue = [('non_sla_dead_line', '>=', date_from), ('non_sla_dead_line', '<=', date_to),
                                  ('stage_id.is_close', '=', False)]
        total_exceeding_non_sla = self.env['helpdesk.ticket'].search_count(domain_non_sla_overdue)
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

    def generate_xlsx_report(self, workbook, data, tickets):
        worksheet = workbook.add_worksheet('Ticket Overall Report')
        bold = workbook.add_format({'bold': True, 'align': 'left'})
        text = workbook.add_format({'font_size': 12, 'align': 'center', 'font_color': 'FFFFFF', 'bg_color': 'd4af37'})
        top_heading = workbook.add_format(
            {'bold': True, 'font_size': 18, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_color': '915e4c'})
        heading = workbook.add_format(
            {'bold': True, 'border': 1, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'bg_color': '915e4c',
             'font_color': 'FFFFFF'})
        heading2 = workbook.add_format(
            {'bold': True, 'italic': True, 'border': 1, 'font_size': 8, 'align': 'center', 'valign': 'vcenter',
             'bg_color': '915e4c',
             'font_color': 'FFFFFF'})
        # Column width
        worksheet.set_column("A:A", 13)
        worksheet.set_column("B:B", 30)
        worksheet.set_column("C:C", 10)
        worksheet.set_column("D:D", 10)
        worksheet.set_column("E:E", 30)

        worksheet.merge_range('A1:E3', "Overall Ticket  Report", top_heading)
        # From date And To Date string to Datetime Convert
        worksheet.write('A5', 'From Date : ', bold)
        from_dt = data['form']['date_from']
        # from_dt is string then we want to convert string into date time
        dt_f = datetime.fromisoformat(str(from_dt))
        new_date_from = datetime.strftime((dt_f + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write('B5', new_date_from)

        worksheet.write('D5', 'End Date : ', bold)
        to_dt = data['form']['date_to']
        dt_to = datetime.fromisoformat(str(to_dt))
        new_date_to = datetime.strftime((dt_to + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write('E5', new_date_to)
        #
        new_data = self.get_helpdesk_overall_ticket_data(data)
        # print(new_data)

        # Method To Write The Column Headings
        row = 6
        heading_list = ["Total Email", "Attended on TAT"]
        for column in range(len(heading_list)):
            worksheet.write(row, column, heading_list[column], heading)

        worksheet.merge_range('C7:D7', "Exceeding SLA", heading)
        worksheet.write('E7', 'Time Taken', heading)
        row = 7
        heading2_list = ["#", "#", "#", "%", "Time in Hour", ]
        for column in range(len(heading2_list)):
            worksheet.write(row, column, heading2_list[column], heading2)

        # Insert Values into the Column
        row = 8
        column = 0
        for tickets in new_data['complete_recs']:
            worksheet.write(row, column, tickets['total'], text)
            worksheet.write(row, column + 1, tickets['attended_tat'], text)
            worksheet.write(row, column + 2, tickets['exceeding_ticket'], text)
            worksheet.write(row, column + 3, tickets['exceeding_avg'], text)
            worksheet.write(row, column + 4, tickets['time_taken'], text)
            row += 1
