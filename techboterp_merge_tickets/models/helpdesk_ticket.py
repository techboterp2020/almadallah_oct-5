
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

from odoo import models, fields, api


class InheritHelpdesk(models.Model):
    _inherit = "helpdesk.ticket"

    is_merge = fields.Boolean(default=False)
    is_closed = fields.Boolean()

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        super(InheritHelpdesk, self)._onchange_stage_id()
        for stage in self.stage_id:
            if stage.is_close:
                self.is_closed = True


