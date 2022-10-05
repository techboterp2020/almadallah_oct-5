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
{
    'name': 'TechbotErp Ticket Schedular in Help Desk',
    'version': '15.0.2.0.1',
    'summary': 'A module for Manage Automated scheduled Report in Help Desk',
    'description': 'Ticked Schedular in Help Desk v15',
    'category': 'Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': '-100',
    'images': [],
    'depends': ['techboterp_helpdesk', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/cron.xml',
        'report/helpdesk_overall_ticket_report.xml',
        'report/helpdesk_overall_ticket_report_templates.xml',
        'report/helpdesk_ticket_report.xml',
        'report/helpdesk_ticket_report_templates.xml',
        'report/helpdesk_team_ticket_report_templates.xml',
        'wizard/helpdesk_team_ticket_report_wizard.xml',
        'wizard/helpdesk_overall_ticket_report_wizard.xml',
        'wizard/helpdesk_ticket_wizard.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
