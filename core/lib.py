from enum import Enum
from abc import ABC
from abc import abstractmethod

class ResourceType(Enum):
    Geolocation = 1
    Camera = 2
    Microphone = 3

class ApprovedResource(object):
    """
        Represents approved resource results.
    """

    def __init__(self, origin, resource_type, expiration_time=None):
        """
            Creates an instance.
        """

        # Save members
        self.origin = origin
        self.resource_type = resource_type
        self.expiration_time = expiration_time

class BrowserResults(object):
    """
        Container for browser results.
    """

    def __init__(self, browser_name):
        """
            Creates an instance.
        """

        # Save members
        self.browser_name = browser_name
        self.modifiable_settings_filepaths = []
        self.approved_resources = []

    def add_modifiable_settings_path(self, settings_filepath):
        """
            Adds a modifiable settings filepath.
        """

        # Append
        self.modifiable_settings_filepaths.append(settings_filepath)

    def add_approved_resource(self, approved_resource):
        """
            Adds an approved resource.
        """

        # Append
        self.approved_resources.append(approved_resource)

    def is_heuristically_vulnerable(self):
        """
            Indicates if the results indicate a TCC-bypassing vulnerability.
        """

        # We want to see at least one approved setting and one writable path
        return len(self.approved_resources) > 0 and len(self.modifiable_settings_filepaths) > 0

class BrowserEvaluatorBase(ABC):
    """
        Base class for evaluating a browser
    """

    def __init__(self):
        """
            Creates an instance.
        """

        # Creates an instance
        super().__init__()
    
    @abstractmethod
    def get_browser_name(self):
        """
            Gets the browser name.
        """
        pass

    @abstractmethod
    def evaluate(self, username, home_dir):
        """
            Evaluates the given username with the given home directory.
        """
        pass
        
