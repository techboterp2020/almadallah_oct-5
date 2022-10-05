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

from odoo import models, fields, api, _
from lxml import etree
import dateutil.relativedelta


class UserAvavilability(models.Model):
    _name = 'helpdesk.user.availability'
    _description = "HelpDesk User Availability"
    _rec_name = "user_id"
    
    user_id = fields.Many2one('res.users')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    created_date_help = fields.Date(string='Created Date')
    working_time = fields.Float('Working Time', store=True, compute='_compute_working_time', readonly=True)
    # New Field to calculate employee break time
    # break_time = fields.Float("Break Time")

    @api.depends('check_in', 'check_out')
    def _compute_working_time(self):
        for rec in self:
            rec.working_time = False
            if rec.check_in and rec.check_out:
                check_in_time = fields.Datetime.from_string(rec.check_in)
                check_out_time = fields.Datetime.from_string(rec.check_out)
                difference = dateutil.relativedelta.relativedelta(check_out_time, check_in_time)
                # print("Time Difference is:",difference)
                """ Method to find total Hour """
                time_hour = (24 * difference.days) + difference.hours + (difference.minutes / 60) + ( difference.seconds / 3600)
                rec.working_time = time_hour
    
