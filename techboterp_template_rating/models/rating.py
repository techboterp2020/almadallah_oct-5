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
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import api, fields, models, tools
from odoo.modules.module import get_resource_path

RATING_LIMIT_SATISFIED = 5
RATING_LIMIT_ABOVE_AVG = 4
RATING_LIMIT_OK = 3
RATING_LIMIT_BELOW_AVG = 2
RATING_LIMIT_MIN = 1


class Rating(models.Model):
    _inherit = "rating.rating"

    rating_text = fields.Selection(selection_add=[
        ('above_ok', 'Above Average'),
        ('below_ok', 'Below Average')], string='Rating', store=True, compute='_compute_rating_text', readonly=True)
    
    def _get_rating_image_filename(self):
        self.ensure_one()
        if self.rating >= RATING_LIMIT_SATISFIED:
            rating_int = 5
        elif self.rating >= RATING_LIMIT_ABOVE_AVG:
            rating_int = 4
        elif self.rating >= RATING_LIMIT_OK:
            rating_int = 3
        elif self.rating >= RATING_LIMIT_BELOW_AVG:
            rating_int = 2
        elif self.rating >= RATING_LIMIT_MIN:
            rating_int = 1
        else:
            rating_int = 0
        return 'rating_%s.png' % rating_int

    def _compute_rating_image(self):
        for rating in self:
            try:
                image_path = get_resource_path('techboterp_template_rating', 'static/src/img', rating._get_rating_image_filename())
                rating.rating_image = base64.b64encode(open(image_path, 'rb').read()) if image_path else False
            except (IOError, OSError):
                rating.rating_image = False

    @api.depends('rating')
    def _compute_rating_text(self):
        for rating in self:
            if rating.rating >= RATING_LIMIT_SATISFIED:
                rating.rating_text = 'top'
            elif self.rating >= RATING_LIMIT_ABOVE_AVG:
                rating.rating_text = 'above_ok'
            elif rating.rating >= RATING_LIMIT_OK:
                rating.rating_text = 'ok'
            elif rating.rating >= RATING_LIMIT_BELOW_AVG:
                rating.rating_text = 'below_ok'   
            elif rating.rating >= RATING_LIMIT_MIN:
                rating.rating_text = 'ko'
            else:
                rating.rating_text = 'none'


class RatingMixin(models.AbstractModel):
    _inherit = 'rating.mixin'  
    
    def rating_apply(self, rate, token=None, feedback=None, subtype_xmlid=None):
        if self._name == "helpdesk.ticket":
            rating = None
            if token:
                rating = self.env['rating.rating'].search([('access_token', '=', token)], limit=1)
            else:
                rating = self.env['rating.rating'].search([('res_model', '=', self._name), ('res_id', '=', self.ids[0])], limit=1)
            if rating:
                rating.write({'rating': rate, 'feedback': feedback, 'consumed': True})
                if hasattr(self, 'message_post'):
                    feedback = tools.plaintext2html(feedback or '')
                    self.message_post(
                        body="<img src='/techboterp_template_rating/static/src/img/rating_%s.png' alt=':%s/5' style='width:18px;height:18px;float:left;margin-right: 5px;'/>%s"
                        % (rate, rate, feedback),
                        subtype_xmlid=subtype_xmlid or "mail.mt_comment",
                        author_id=rating.partner_id and rating.partner_id.id or None  # None will set the default author in mail_thread.py
                    )
                if hasattr(self, 'stage_id') and self.stage_id and hasattr(self.stage_id, 'auto_validation_kanban_state') and self.stage_id.auto_validation_kanban_state:
                    if rating.rating > 2:
                        self.write({'kanban_state': 'done'})
                    else:
                        self.write({'kanban_state': 'blocked'})
            return rating 
        
        return super(RatingMixin, self).rating_apply(rate, token=None, feedback=None, subtype_xmlid=None)
        
