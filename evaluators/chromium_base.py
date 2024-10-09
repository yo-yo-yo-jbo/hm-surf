from core.lib import ResourceType
from core.lib import ApprovedResource
from core.lib import BrowserResults
from core.lib import BrowserEvaluatorBase
from core.utils import Utils

import os
import json
from abc import abstractmethod

class ChromiumEvaluatorBase(BrowserEvaluatorBase):
    """
        Evaluates Opera.
    """

    @abstractmethod
    def get_preferences_filepath(self, home_dir):
        """
            Gets the preferences file path.
        """
        pass

    def evaluate(self, username, home_dir):
        """
            Evaluates the browser.
        """

        # Get the preferences
        prefs_filepath = self.get_preferences_filepath(home_dir)
        if not os.path.isfile(prefs_filepath):
            return None

        # Parse the preferences and ignore permission errors
        try:
            with open(prefs_filepath, 'r') as prefs_fp:
                prefs = json.load(prefs_fp)
        except PermissionError:
            return None

        # Saves the results
        results = BrowserResults(self.get_browser_name())
        if Utils.has_write_access(prefs_filepath):
            results.add_modifiable_settings_path(prefs_filepath)

        # Get geolocation results
        for origin, entry in prefs['profile']['content_settings'].get('exceptions', {}).get('geolocation', {}).items():
            if entry['setting'] != 0:
                results.add_approved_resource(ApprovedResource(origin, ResourceType.Geolocation)) 

        # Get camera results
        for origin, entry in prefs['profile']['content_settings'].get('exceptions', {}).get('media_stream_camera', {}).items():
            if entry['setting'] != 0:
                results.add_approved_resource(ApprovedResource(origin, ResourceType.Camera))

        # Get microphone results
        for origin, entry in prefs['profile']['content_settings'].get('exceptions', {}).get('media_stream_mic', {}).items():
            if entry['setting'] != 0:
                results.add_approved_resource(ApprovedResource(origin, ResourceType.Microphone))

        # Return the results
        return results

