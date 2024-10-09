from core.lib import ResourceType
from core.lib import ApprovedResource
from core.lib import BrowserResults
from core.lib import BrowserEvaluatorBase
from core.utils import Utils
from core.sqlite_aux import SqliteAux

import os
import plistlib

class AppleSafariEvaluator(BrowserEvaluatorBase):
    """
        Evaluates Apple Safari.
    """

    # Maps generic settings to resource types
    SETTING_TO_RESOURCE_TYPE_MAP = {
            'PerSitePreferencesCamera' : ResourceType.Camera,
            'PerSitePreferencesMicrophone' : ResourceType.Microphone,
            'PerSitePreferencesGeolocation' : ResourceType.Geolocation
    }

    # Map media flags to resource types
    RESOURCE_TYPE_TO_MEDIA_FLAGS_MAP = {
        ResourceType.Camera : 32,
        ResourceType.Microphone : 4
    }

    def get_browser_name(self):
        """
            Gets the browser name.
        """

        # Return the name
        return 'Apple Safari'

    def evaluate(self, username, home_dir):
        """
            Evaluates Apple Safari.
        """

        # Get the generic preferences
        general_prefs_filepath = os.path.join(home_dir, 'Library', 'Safari', 'PerSitePreferences.db')
        if not os.path.isfile(general_prefs_filepath):
            return None

        # Saves the results
        results = BrowserResults(self.get_browser_name())
        if Utils.has_write_access(general_prefs_filepath):
            results.add_modifiable_settings_path(general_prefs_filepath)

        # Parse the general preferences
        with SqliteAux(general_prefs_filepath) as conn:
            for pref in conn.run_query('SELECT preference, default_value FROM default_preferences;'):
                resource_type = self.__class__.SETTING_TO_RESOURCE_TYPE_MAP.get(pref[0], None)
                if resource_type is not None and pref[1] != 0:
                    results.add_approved_resource(ApprovedResource('*', resource_type))
            for pref in conn.run_query('SELECT domain, preference, preference_value FROM preference_values;'):
                resource_type = self.__class__.SETTING_TO_RESOURCE_TYPE_MAP.get(pref[1], None)
                if resource_type is not None and pref[2] != 0:
                    results.add_approved_resource(ApprovedResource(pref[0], resource_type))

        # Get the per-origin media settings
        per_origin_media_prefs_filepath = os.path.join(home_dir, 'Library', 'Safari', 'UserMediaPermissions.plist')
        if not os.path.isfile(per_origin_media_prefs_filepath):
            return results

        # Add to results
        if Utils.has_write_access(per_origin_media_prefs_filepath):
            results.add_modifiable_settings_path(per_origin_media_prefs_filepath)

        # Parse the per-origin media settings and ignore permission errors
        try:
            with open(per_origin_media_prefs_filepath, 'rb') as per_origin_media_prefs_fp:
                data = plistlib.load(per_origin_media_prefs_fp)
            for entry in data.values():
                for resource_type, flags in self.__class__.RESOURCE_TYPE_TO_MEDIA_FLAGS_MAP.items():
                    if (flags & entry['permission']) != 0:
                        results.add_approved_resource(ApprovedResource(entry['origin'], resource_type))
        except PermissionError:
            pass

        # Return the results
        return results
