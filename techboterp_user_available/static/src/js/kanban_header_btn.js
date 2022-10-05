/** @odoo-module **/

import { registry } from "@web/core/registry";
import { preferencesItem } from "@web/webclient/user_menu/user_menu_items";

export function hrPreferencesItem123(env)  {
    console.log("********************************************TEST",self,this)
    return {
        type: "item",
        id: "settings1",
        description: env._t("Availability"),
        callback: async function () {
          env.services.action.doAction({
                res_model: "user.available.wiz",
                name: " ",
                views: [
                    [false, "form"],
                ],
                type: "ir.actions.act_window",
		target:"new",
            });
        },
        sequence: 50,
    };
}

registry.category("user_menuitems").add('profile2', hrPreferencesItem123, { force: true })
