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
    'name': 'TechbotErp User Avaiable in Help Desk',
    'version': '15.0.1.2',
    'summary': 'A module for Manage User Avaiable in Help Desk',
    'description': 'User Avaiable in Help Desk v15',
    'category': 'Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': '-100',
    'images': [],
    'depends': ['base', 'mail', 'helpdesk'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/user_available_wiz_view.xml',
        'views/user_view.xml',
        'views/techboterp_menu_views.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'techboterp_user_available/static/src/js/kanban_header_btn.js',
        ],
    },
}
