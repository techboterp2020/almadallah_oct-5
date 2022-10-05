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
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, ValidationError
from datetime import date, datetime
from odoo.addons.web.controllers.main import WebClient, Home, Session


class SessionWebsite(Session):

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        user = request.env['res.users'].sudo().browse(request.env.context.get('uid'))
        if user.has_group('helpdesk.group_helpdesk_user') or user.has_group('helpdesk.group_helpdesk_manager'):
            if user.user_available:
                user.write({'user_available': False})
                if user.last_availblity_id:
                    user.last_availblity_id.write({'check_out': datetime.now()})
        return super().logout(redirect=redirect)
