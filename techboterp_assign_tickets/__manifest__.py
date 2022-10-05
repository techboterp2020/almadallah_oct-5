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
    'name': 'TechbotErp HelpDesk Ticket Assign Tickets',
    'version': '15.0.0.0.1',
    'description': 'Adding a new mail template and send mail by clicking on the given button',
    'category': 'Services/Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'images': [],
    'depends': [
        'helpdesk', 'techboterp_user_available'
    ],
    'description': "",
    'data': [
        "security/ir.model.access.csv",
        "wizard/assign_user.xml",
        "views/helpdesk_ticket.xml",

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
