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
# from odoo.exceptions import UserErrorfrom
# from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

class HelpDeskOverDeadlineXlsxReport(models.AbstractModel):
    _name = 'report.techboterp_scheduled_action.report_helpdesk_ticket_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Abstract Ticket overdue XLSX Report"

    @api.model
    def get_help_desk_data(self, data):
        date_from = data['form']['date_from']
        # print(data, '***********************gey Gelp from')
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

    def generate_xlsx_report(self, workbook, data, tickets):
        # now_utc_date = datetime.datetime.strptime(data['form']['date_from'], '%Y-%m-%d').strftime('%d-%m-%Y'))
        worksheet = workbook.add_worksheet('Ticket Overdue')
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        text = workbook.add_format({'font_size': 12, 'align': 'center'})
        top_heading = workbook.add_format(
            {'bold': True, 'font_size': 18, 'align': 'center', 'valign': 'vcenter', 'font_color': '915e4c'})
        heading = workbook.add_format(
            {'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'bg_color': '915e4c',
             'font_color': 'FFFFFF'})
        # Column String size
        worksheet.set_column("A:A", 13)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 25)
        worksheet.set_column("D:D", 22)
        worksheet.set_column("E:E", 27)
        worksheet.set_column("F:F", 30)
        worksheet.set_column("G:G", 30)
        worksheet.set_column("H:H", 10)

        worksheet.merge_range('A1:H3', "Ticket Overdue Report", top_heading)
        worksheet.write('A5', 'From Date : ', bold)
        from_dt = data['form']['date_from']
        # t is string then we want to convert string into date timee
        dt_f = datetime.fromisoformat(str(from_dt))
        new_date_from = datetime.strftime((dt_f + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        # print(type(dt_f))
        to_dt = data['form']['date_to']
        dt_to = datetime.fromisoformat(str(to_dt))
        new_date_to = datetime.strftime((dt_to + timedelta(hours=4)), DEFAULT_SERVER_DATETIME_FORMAT)
        # print(type(dt))
        # worksheet.write('B5', data['form']['date_from'])
        worksheet.write('B5', new_date_from)
        worksheet.write('F5', 'End Date : ', bold)
        worksheet.write('G5', new_date_to)
        # worksheet.write('G5', data['form']['date_to'])

        new_data = self.get_help_desk_data(data)
        # Adding Headings
        row = 6
        heading_list = ["SL No.", "Ticket Name", "Helpdesk Team", "Assigned To", "Customer Name", "SLA Deadline",
                        " Non SLA Deadline", "Stage"]
        for column in range(len(heading_list)):
            worksheet.write(row, column, heading_list[column], heading)

        sl_no = 1
        row = 7
        column = 0
        for tickets in new_data['complete_recs']:
            worksheet.write(row, column, sl_no, text)
            worksheet.write(row, column + 1, tickets['name'], text)
            worksheet.write(row, column + 2, tickets['team_id']['name'], text)
            worksheet.write(row, column + 3, tickets['user_id']['name'], text)
            worksheet.write(row, column + 4, tickets['partner_id']['name'], text)

            if tickets['sla_deadline']:
                sla_time = tickets['sla_deadline'] + timedelta(hours=4)
                sla = datetime.strftime(sla_time, DEFAULT_SERVER_DATETIME_FORMAT)
                # Sla Type is Str type(sla)

                worksheet.write(row, column + 5, sla, text)
            else:
                non_sla_time = tickets['non_sla_dead_line'] + timedelta(hours=4)
                non_sla = datetime.strftime(non_sla_time, DEFAULT_SERVER_DATETIME_FORMAT)
                worksheet.write(row, column + 6, non_sla, text)

            worksheet.write(row, column + 7, tickets['stage_id']['name'], text)
            sl_no += 1
            row += 1
