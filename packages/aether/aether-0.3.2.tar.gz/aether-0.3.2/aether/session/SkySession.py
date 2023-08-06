import aether
import pip
from aether.Sky import Sky
from aether.session.GlobalConfig import GlobalConfig
from aether.session import Exceptions

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkySession(object):

    def __init__(self, app=None):
        self._app = app

    def GlobalConfig(self):
        return GlobalConfig._getInstance()

    def aether_client(self):
        return GlobalConfig._getInstance()._aether_client()

    @staticmethod
    def _package_diagnostic(p):
        return "SDK INFO: {} version {}; Location: {}; Egg Name: {}\n".format(p.project_name, p.version, p.location, p.egg_name)

    def __enter__(self):
        return Sky(self.aether_client(), app=self._app)

    def __exit__(self, type, value, traceback):

        # Error catching on the Sky
        if isinstance(value, Exceptions.SkyError):
            msg = "\nAether SDK Diagnostic Stack. Please provide when reporting errors or issues.\n"

            actual_runtime_path = "/".join(aether.__path__[0].split("/")[:-1])
            msg += "SDK INFO: Runtime package path: {}\n".format(actual_runtime_path)

            # packages = pip.utils.get_installed_distributions()
            # aether_package = [p for p in packages if p.project_name == "aether"]
            # if len(aether_package) != 1:
            #     msg += "SDK WARNING: Multiple pip installed packages of aether found: {}".format(aether_package)
            #
            # runtime_package = [p for p in aether_package if p.location == actual_runtime_path]
            # if len(runtime_package) == 0:
            #     msg += "SDK WARNING: Runtime package of aether could not be located.\n"
            #
            # msg += "".join([self._package_diagnostic(p) for p in runtime_package])
            msg += "SDK INFO: {}".format(self.GlobalConfig()._diagnostic_debug_report())

            logger.info(msg)



        # Throw the error still.
        return False
