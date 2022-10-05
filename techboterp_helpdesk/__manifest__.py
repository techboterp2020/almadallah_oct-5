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
    'name': 'TechbotErp Help Desk ',
    'version': '15.0.0.2.1',
    'description': 'Helpdesk Enterprise version15',
    'category': 'Services/Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'images': [],
    'sequence': -10,
    'summary': 'Adding background color for kanban view in helpdesk ticket',
    'depends': [
        'base',
        'helpdesk',
    ],
    'data': [
        'views/helpdesk_ticket_add_color_kanban_view.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_stage_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'techboterp_helpdesk/static/src/scss/helpdesk.scss',
        ],
    },
}
