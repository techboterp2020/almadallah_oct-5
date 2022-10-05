# -*- coding: utf-8 -*-
# #############################################################################
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
# #############################################################################

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import relativedelta
import dateutil.relativedelta
from odoo.exceptions import ValidationError, UserError


class InheritHelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for rec in self:
            # if rec.stage_id.is_forward == True:
            if rec.stage_id.is_forward:
                rec.team_id = rec.stage_id.team_id.id

            # rec.user_id = rec.env['helpdesk.team']._determine_user_to_assign(self)
            # rec.user_id = rec.team_id.user_id.filtered(lambda j: j.user_available == True)

    non_sla_dead_line = fields.Datetime("NON SLA Dead Line", compute='_compute_non_sla_deadline', store=True)
    time = fields.Float('In', help='Time to reach given stage based on ticket creation date', default=1, required=True)
    color = fields.Integer(string='Color Index', compute='_compute_color')
    ticket_overdue = fields.Boolean(compute='_compute_ticket_overdue_reminder', string='Ticket Overdue')
    # new Field Added
    created_on = fields.Datetime("Created Date", default=datetime.now())
    completed_on = fields.Datetime("Closed Time")
    closed_ticket_time_in_hour = fields.Float('Ticket Closing Time', store=True, compute='_compute_working_time',
                                              readonly=True, tracking=4)

    # Method To Find Ticket Closed Date Time
    def write(self, vals):
        res = super(InheritHelpdeskTicket, self).write(vals)
        if self.stage_id.is_close and 'stage_id' in vals:
            self.completed_on = fields.Datetime.now()
        # Method to restrict New stage change to another stage without Tag_id
        if not self.stage_id.is_new_stage:
            if not self.tag_ids:
                raise ValidationError(_("Please Add/ Select Tags for current ticket"))
        return res

    #  To calculate Non sla deadline
    @api.depends('time')
    def _compute_non_sla_deadline(self):
        for rec in self:
            rec.non_sla_dead_line = False
            rec.non_sla_dead_line = datetime.now() + relativedelta.relativedelta(hours=rec.time)

    # Method to Change the Kanban background color in Sla and Non_Sla deadline
    @api.depends('stage_id', 'sla_deadline', 'non_sla_dead_line')
    def _compute_color(self):
        for ticket in self:
            ticket.color = 0
            if (ticket.sla_deadline and ticket.sla_deadline < fields.Datetime.now()) or (
                    ticket.non_sla_dead_line and ticket.non_sla_dead_line < fields.Datetime.now()):
                """Background Color Changes Based on the Stages in Kanban View
                    if the deadline is overdue the background color changed to Red
                    and the stage is closed then the background color red changed to white
                """
                if not ticket.stage_id.is_close:
                    ticket.color = 6
                else:
                    ticket.color = 0

    # Method to Find Not Closed  ticket based on Deadline
    @api.depends('sla_deadline', 'non_sla_dead_line')
    def _compute_ticket_overdue_reminder(self):
        for record in self:
            overdue = False
            for ticket in record:
                if (ticket.non_sla_dead_line and ticket.non_sla_dead_line < fields.Datetime.now()) or (
                        ticket.sla_deadline and ticket.sla_deadline < fields.Datetime.now()):
                    if not ticket.stage_id.is_close:
                        overdue = True
            record.ticket_overdue = overdue

    # Method To Find Total time Taken For Close A Ticket
    @api.depends('created_on', 'completed_on')
    def _compute_working_time(self):
        for rec in self:
            rec.closed_ticket_time_in_hour = False
            if rec.created_on and rec.completed_on:
                start_dt = fields.Datetime.from_string(rec.created_on)
                finish_dt = fields.Datetime.from_string(rec.completed_on)
                difference = dateutil.relativedelta.relativedelta(finish_dt, start_dt)
                """ Method to find total Hour """
                time_hour = (24 * difference.days) + difference.hours + (difference.minutes / 60) + (
                        difference.seconds / 3600)
                rec.closed_ticket_time_in_hour = time_hour

        # Method to Change Helpdesk Team Based on Stage Have Forwarded Team
