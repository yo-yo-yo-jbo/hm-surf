from evaluators.chromium_base import ChromiumEvaluatorBase

import os

class GoogleChromeEvaluator(ChromiumEvaluatorBase):
    """
        Evaluates Google Chrome.
    """

    def get_browser_name(self):
        """
            Gets the browser name.
        """

        # Return the name
        return 'Google Chrome'

    def get_preferences_filepath(self, home_dir):
        """
            Gets the preferences file path.
        """

        # Return the preferences filepath
        return os.path.join(home_dir, 'Library', 'Application Support', 'Google', 'Chrome', 'Default', 'Preferences')

