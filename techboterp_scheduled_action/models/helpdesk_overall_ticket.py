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

from odoo import models, Command, fields, SUPERUSER_ID, api, _

from odoo.exceptions import ValidationError
from datetime import date, datetime,timedelta

import base64


class IrCron(models.Model):
    _inherit = 'helpdesk.ticket'

    def _send_help_overall_ticket_report(self):
        data = {'form': {'date_from': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=45) - timedelta(days=1)-timedelta(hours=4)),
                         'date_to': datetime.now()
                         }}
        # data = {'form': {'date_from': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        #                  'date_to': datetime.now()
        #                  }}

        # To Create Pdf Report
        REPORT_ID = 'techboterp_scheduled_action.action_report_helpdesk_overall_ticket'
        pdf = self.env.ref(REPORT_ID).with_user(SUPERUSER_ID)._render_qweb_pdf(self.ids, data=data)
        b64_pdf = base64.b64encode(pdf[0])
        ATTACHMENT_NAME = 'Helpdesk Daily wise Overall Ticket Report'
        attachment_id = self.env['ir.attachment'].create({
            'name': ATTACHMENT_NAME + '.pdf',
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': ATTACHMENT_NAME + '.pdf',
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf',
            'company_id': self.env.user.company_id.id
        })

        # Create the XLSX Report
        XLSX_REPORT_ID = 'techboterp_scheduled_action.action_report_helpdesk_overall_ticket_xlsx'
        xlsx = self.env.ref(XLSX_REPORT_ID).with_user(SUPERUSER_ID)._render_xlsx(self.ids, data=data)
        b64_xlsx = base64.b64encode(xlsx[0])
        attachment_xlsx_id = self.env['ir.attachment'].create({
            'name': ATTACHMENT_NAME + '.xlsx',
            'type': 'binary',
            'datas': b64_xlsx,
            'store_fname': ATTACHMENT_NAME + '.xlsx',
            'mimetype': 'text/csv',
        })

        # Email Pdf and Xlsx Attachment
        attach = {
            attachment_id.id, attachment_xlsx_id.id
        }

        team_admin_emails = ','.join([user.email for user in self.env.ref(
            'techboterp_scheduled_action.group_overall_ticket_report_mail_send').users])
        mail_values = {

            'reply_to': team_admin_emails,
            'email_to': team_admin_emails,
            'subject': ATTACHMENT_NAME,
            'body_html': """<div>
                        <p>Hello,</p>
                        <p>This email was created Automatically by Odoo. Please find the attached HelpDesk Dialy Team Ticket Report.</p>
                        </div>
                        <div>Thank You</div>""",
            'attachment_ids': [(6, 0, attach)]
        }
        mail_id = self.env['mail.mail'].create(mail_values)
        mail_id.send()
