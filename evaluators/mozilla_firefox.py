from core.lib import ResourceType
from core.lib import ApprovedResource
from core.lib import BrowserResults
from core.lib import BrowserEvaluatorBase
from core.utils import Utils
from core.sqlite_aux import SqliteAux

import os
import configparser

class MozillaFirefox(BrowserEvaluatorBase):
    """
        Evaluates Mozilla Firefox.
    """

    # Maps permissions to resource types
    PERMISSION_TO_RESOURCE_TYPE_MAP = {
        'camera' : ResourceType.Camera,
        'microphone' : ResourceType.Microphone,
        'geo' : ResourceType.Geolocation
    }

    def get_browser_name(self):
        """
            Gets the browser name.
        """

        # Return the name
        return 'Mozilla Firefox'

    def evaluate(self, username, home_dir):
        """
            Evaluates Mozilla Firefox.
        """

        # Get the profiles
        profiles_filepath = os.path.join(home_dir, 'Library', 'Application Support', 'Firefox', 'profiles.ini')
        if not os.path.isfile(profiles_filepath):
            return None

        # Saves the results
        results = BrowserResults(self.get_browser_name())

        # Parse all profiles
        config = configparser.ConfigParser()
        config.read(profiles_filepath)
        for profile in config.sections():
           
            # Get the profile details
            profile_path = config[profile].get('path', None)
            if profile_path is None:
                continue
            is_relative = int(config[profile]['isrelative']) != 0
            if is_relative:
                profile_path = os.path.join(home_dir, 'Library', 'Application Support', 'Firefox', profile_path)

            # Get the permissions filepath
            permissions_filepath = os.path.join(profile_path, 'permissions.sqlite')
            if not os.path.isfile(permissions_filepath):
                continue

            # Check permissions to the permissions file
            if Utils.has_write_access(permissions_filepath):
                results.add_modifiable_settings_path(permissions_filepath)
           
            # Parse permissions
            with SqliteAux(permissions_filepath) as conn:
                for perms in conn.run_query('SELECT origin, type, permission, expireTime FROM moz_perms;'):
                    resource_type = self.__class__.PERMISSION_TO_RESOURCE_TYPE_MAP.get(perms[1], None)
                    if resource_type is not None and perms[1] == 0:
                        expiration_time = Utils.sql_timestamp_to_datetime(perms[3]) if perms[3] is not None else None
                        results.add_approved_resource(ApprovedResource(perms[0], resource_type, expiration_time))

        # Return the results
        return results
