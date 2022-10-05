odoo.define('attendance.button.tree', function (require) {
"use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc')

    var includeDict = {
        willStart: function () {
            var self = this;
            return this._rpc({
                method: 'accept_deny_val',
                model: 'helpdesk.ticket',
            }).then(function (result) {
               self.result = result
            });
        },

        buttons_template: 'AttendenceMarkListView.buttons',
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            var self = this;
            this.$buttons.on('click', '.o_button_accept_ticket', this._onAcceptAttendance.bind(this));
            this.$buttons.on('click', '.o_button_deny_ticket', this._onDeclineAttendance.bind(this));

        },

        _onAcceptAttendance: function(){
            var self = this;
            return self._rpc({
            model: 'helpdesk.ticket',
            method: 'user_accept_ticket',
            args: [],
            }).then(function (data) {

                if(data == true)
                {
                    self.$("#button_accept").addClass("oe_hide_button");
                    window.location.reload();
                }

            });
        },

         _onDeclineAttendance: function(){
            var self = this;
            return self._rpc({
                model: 'helpdesk.ticket',
                method: 'user_decline_ticket',
                args: [],
            }).then(function (data) {
                if(data == false)
                {
                    self.$("#button_reject").addClass("oe_hide_button");
                    window.location.reload();
                }

                });
        },
    };

    ListController.include(includeDict);

});