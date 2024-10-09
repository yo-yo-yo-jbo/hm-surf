from evaluators.chromium_base import ChromiumEvaluatorBase

import os

class OperaEvaluator(ChromiumEvaluatorBase):
    """
        Evaluates Opera.
    """

    def get_browser_name(self):
        """
            Gets the browser name.
        """

        # Return the name
        return 'Opera'

    def get_preferences_filepath(self, home_dir):
        """
            Gets the preferences file path.
        """
    
        # Return the preferences filepath
        return os.path.join(home_dir, 'Library', 'Application Support', 'com.operasoftware.Opera', 'Default', 'Preferences')

