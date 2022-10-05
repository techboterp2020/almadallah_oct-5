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
from odoo import models, Command, fields, api, _
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    user_available = fields.Boolean(string='Available')
    last_availblity_id = fields.Many2one('helpdesk.user.availability')
    accept_deny = fields.Selection([('active', 'Active'), ('non', 'Non Active')], compute='_check_user_availability', store=True)

#method for computing user_availability

    @api.depends('user_available')
    def _check_user_availability(self):
        for user in self:
            if user.user_available == True:
                user.accept_deny = 'active'
            else:
                user.accept_deny = 'non'


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    
    @api.depends('team_id')
    def _compute_domain_user_ids(self):
        helpdesk_user_group_id = self.env.ref('helpdesk.group_helpdesk_user').id
        helpdesk_manager_group_id = self.env.ref('helpdesk.group_helpdesk_manager').id
        users_data = self.env['res.users'].read_group(
            [('groups_id', 'in', [helpdesk_user_group_id, helpdesk_manager_group_id])],
            ['ids:array_agg(id)', 'groups_id'],
            ['groups_id'],
        )
        mapped_data = {data['groups_id'][0]: data['ids'] for data in users_data}
        for ticket in self:
            if ticket.team_id and ticket.team_id.privacy == 'invite' and ticket.team_id.visibility_member_ids:
                manager_ids = mapped_data.get(helpdesk_manager_group_id, [])
                ticket.domain_user_ids = [Command.set(manager_ids + ticket.team_id.visibility_member_ids.ids)]
            else:
                user_ids = mapped_data.get(helpdesk_user_group_id, [])
                ticket.domain_user_ids = [Command.set(user_ids)]
    
    def assign_ticket_to_self(self):
        self.ensure_one()
        if not self.env.user.user_available:
            raise ValidationError('You are not available now,Please make available')
        return super(HelpdeskTicket, self).assign_ticket_to_self()
    
class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"
    
    def _determine_user_to_assign(self):
        result = dict.fromkeys(self.ids, self.env['res.users'])
        for team in self:
            member_ids = sorted(team.member_ids.filtered(lambda user_id: user_id.user_available == True).ids)
            if team.assign_method == 'randomly':  # randomly means new tickets get uniformly distributed
                last_assigned_user = self.env['helpdesk.ticket'].search([('team_id', '=', team.id)], order='create_date desc, id desc', limit=1).user_id
                index = 0
                if last_assigned_user and last_assigned_user.id in member_ids:
                    previous_index = member_ids.index(last_assigned_user.id)
                    index = (previous_index + 1) % len(member_ids)
                result[team.id] = self.env['res.users'].browse(member_ids[index])
            elif team.assign_method == 'balanced':  # find the member with the least open ticket
                ticket_count_data = self.env['helpdesk.ticket'].read_group([('stage_id.is_close', '=', False), ('user_id', 'in', member_ids), ('team_id', '=', team.id)], ['user_id'], ['user_id'])
                open_ticket_per_user_map = dict.fromkeys(member_ids, 0)  # dict: user_id -> open ticket count
                open_ticket_per_user_map.update((item['user_id'][0], item['user_id_count']) for item in ticket_count_data)
                if open_ticket_per_user_map:
                    result[team.id] = self.env['res.users'].browse(min(open_ticket_per_user_map, key=open_ticket_per_user_map.get))
        return result
