import os
import sys

import petname

from conjureup import controllers, juju, utils
from conjureup.app_config import app


class CloudsController:

    def finish(self):
        if app.argv.cloud == "localhost":
            if not utils.check_bridge_exists():
                back = "{} to localhost".format(app.argv.config['spell'])
                os.execl("/usr/share/conjure-up/run-lxd-config",
                         "/usr/share/conjure-up/run-lxd-config",
                         back)

        existing_controller = juju.get_controller_in_cloud(app.argv.cloud)
        if existing_controller is None:
            return controllers.use('newcloud').render(app.argv.cloud)

        app.current_controller = existing_controller
        app.current_model = petname.Name()
        utils.info("Creating new juju model named '{}', "
                   "please wait.".format(app.current_model))
        juju.add_model(app.current_model, app.current_controller)

        return controllers.use('deploy').render()

    def render(self):
        if app.argv.cloud not in juju.get_clouds().keys():
            formatted_clouds = ", ".join(juju.get_clouds().keys())
            utils.warning(
                "Unknown Cloud: {}, please choose "
                "from one of the following: {}".format(app.argv.cloud,
                                                       formatted_clouds))
            sys.exit(1)
        utils.info(
            "Summoning {} to {}".format(app.argv.spell, app.argv.cloud))
        self.finish()

_controller_class = CloudsController
