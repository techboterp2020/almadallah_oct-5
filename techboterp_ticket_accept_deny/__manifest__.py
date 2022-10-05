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
    'name': 'TechbotErp Help Desk Approve and Deny Button',
    'version': '15.0.0.0.8',

    'description': 'Adding Accept/Deny button for tickets',
    'category': 'Services/Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'images': [],
    'sequence': -10,
    'summary': 'Adding background color for kanban view in helpdesk ticket',
    'depends': [
        'base',
        'helpdesk',
    ],
    'description': "",
    'data': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'techboterp_ticket_accept_deny/static/src/js/attendance_button.js',
            'techboterp_ticket_accept_deny/static/src/scss/button_highlight.scss',
        ],
        'web.assets_qweb': [
            'techboterp_ticket_accept_deny/static/src/xml/**/*',
        ],

    },
}
