from evaluators.chromium_base import ChromiumEvaluatorBase

import os

class MicrosoftEdgeEvaluator(ChromiumEvaluatorBase):
    """
        Evaluates Microsoft Edge.
    """

    def get_browser_name(self):
        """
            Gets the browser name.
        """

        # Return the name
        return 'Microsoft Edge'

    def get_preferences_filepath(self, home_dir):
        """
            Gets the preferences file path.
        """
    
        # Return the preferences filepath
        return os.path.join(home_dir, 'Library', 'Application Support', 'Microsoft Edge', 'Default', 'Preferences')

