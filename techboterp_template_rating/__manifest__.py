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
    'name': 'Rating Template in HelpDesk',
    'version': '15.0.1.2.0',
    'summary': 'Rating Template in HelpDesk',
    'description': 'Rating Template in HelpDesk v15',
    'category': 'Helpdesk',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': '-100',
    'images': [],
    'depends': ['helpdesk','rating'],
    'data': [
        'data/mail_template_data.xml',
        'views/rating_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
