# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from src.taipy.gui_core.GuiCoreLib import GuiCore
from taipy.gui import Gui
from taipy import Scope, Config, Frequency, Core

def replace(input_msg, template, name):
    return input_msg.replace(template, name)

showAdd = True
showCycles = True

page = """
# Scenarios Selector

<|scenario_selector|show_add_button={showAdd}|display_cycles={showCycles}|>

<|{"Hide Add" if showAdd else "Show Add"}|button|on_action={lambda s: s.assign("showAdd", not showAdd)}|>
<|{"Hide Cycles" if showCycles else "Show Cycles"}|button|on_action={lambda s: s.assign("showCycles", not showCycles)}|>

"""    
Gui.add_library(GuiCore())

input_msg_cfg = Config.configure_data_node(id="input_msg", scope=Scope.GLOBAL, default_data="Hello, today it's <TPL>!")
template_cfg = Config.configure_data_node(id="template", scope=Scope.GLOBAL, default_data="<TPL>")
date_cfg = Config.configure_data_node(id="date")
message_cfg = Config.configure_data_node(id="msg")

replace_template_cfg = Config.configure_task("replace", replace, [input_msg_cfg, template_cfg, date_cfg], message_cfg)
scenario_daily_cfg = Config.configure_scenario_from_tasks(id="scenario_daily_cfg",
                                                          task_configs=[replace_template_cfg],
                                                          frequency=Frequency.DAILY)
scenario_cfg = Config.configure_scenario_from_tasks(id="scenario_cfg", task_configs=[replace_template_cfg])

Core().run()

Gui(page).run(debug=True)
