from core.singleton import Singleton
from core.printing import PrettyPrinter
from core.lib import BrowserEvaluatorBase

import importlib.util
import importlib.machinery
import os
import inspect
import subprocess
import datetime
import urllib.parse

# Printer
printer = PrettyPrinter.get_instance()

class Utils(metaclass=Singleton):
    """
        Auxiliary utilities.
    """

    # SQL timestamp base
    SQL_TIMESTAMP_BASE = 978307200

    @staticmethod
    def sql_timestamp_to_datetime(timestamp):
        """
            Converts SQL timestamp to a datetime.
        """

        # Convert to UNIX epoch and then to Python datetime
        return Utils.unix_epoch_to_datetime(timestamp + Utils.SQL_TIMESTAMP_BASE)

    @staticmethod
    def unix_epoch_to_datetime(timestamp):
        """
            Converts UNIX epoch to a Python datetime.
        """

        # Convert
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def encode_as_uri(query):
        """
            Encodes as a URI.
        """

        # Encode as a URI
        return urllib.parse.quote(query)

    @staticmethod
    def has_read_access(path):
        """
            Indicates whether the path has read access.
        """

        # Indicate
        return os.access(path, os.R_OK)

    @staticmethod
    def has_write_access(path):
        """
            Indicates whether the path has write access.
        """

        # Indicate
        return os.access(path, os.W_OK)

    @staticmethod
    def get_evaluators(base_path):
        """
            Gets all the evaluators from the given base path.
        """

        # Fetch evaluators
        evaluators = []
        printer.start_stage('Fetching evaluators')

        # Get the evaluators base path
        for evaluator_filename in os.listdir(base_path):

            # Only take Python files
            if not evaluator_filename.endswith('.py'):
                continue
            evaluator_path = os.path.join(base_path, evaluator_filename)

            # Load the file
            module_name = f'evaluators.{os.path.splitext(evaluator_filename)[0]}'
            loader = importlib.machinery.SourceFileLoader(module_name, evaluator_path)
            spec = importlib.util.spec_from_loader(module_name, loader)
            evaluator_impl = importlib.util.module_from_spec(spec)
            loader.exec_module(evaluator_impl)

            # Find the implementation
            impl_class = [ (name, val) for name, val in evaluator_impl.__dict__.items() if inspect.isclass(val) and issubclass(val, BrowserEvaluatorBase) and not inspect.isabstract(val) ]
            if len(impl_class) == 0:
                printer.append_extra(f'Skipping file "evaluator_filename"')
                continue
            if len(impl_class) > 1:
                raise Exception(f'Evaluator file "{evaluator_filename}" contains multiple subclasses of "BrowserEvaluatorBase"')

            # Instanciate the implementation
            instance = impl_class[0][1]()
            evaluators.append(instance)
            printer.append_extra(f'"{instance.get_browser_name()}"')

        # Return result
        printer.end_stage()
        return evaluators

    @staticmethod
    def get_user_home_directory(username):
        """
            Gets the user's home directory.
        """

        # Run "dscl" to discover the home directory
        proc = subprocess.run([ '/usr/bin/dscl', '.', 'read', f'/Users/{username}', 'NFSHomeDirectory' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
        assert proc.returncode == 0, Exception(f'Getting the home directory of the user "{username}" failed with error code {proc.returncode}')
        return proc.stdout.split('NFSHomeDirectory:')[-1].strip()

    @staticmethod
    def get_all_users():
        """
            Lists users and their home directories.
        """

        # Discovering local users
        local_users = {}
        printer.start_stage('Discovering local users')

        # Run "dscl" to discover all local users
        proc = subprocess.run([ '/usr/bin/dscl', '.', 'list', '/Users' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
        assert proc.returncode == 0, Exception(f'Listing local users failed with error code {proc.returncode}')

        # Iterate all users
        skipped_users = 0
        for username in proc.stdout.strip().split('\n'):

            # Heusitically conclude dummy users
            if username.startswith('_'):
                skipped_users += 1
                continue

            # Get the user's home directory and check if we have read access
            home_dir = Utils.get_user_home_directory(username)
            if '/var/empty' == home_dir:
                printer.append_extra(f'Skipping user "{username}" since its home directory is empty')
                skipped_users += 1
                continue
            if not Utils.has_read_access(home_dir):
                printer.append_extra(f'Skipping user "{username}" since its home directory "{home_dir}" is not readable')
                skipped_users += 1
                continue

            # Add the user and its home directory
            local_users[username] = home_dir

        # Return result
        if skipped_users > 0:
            printer.append_extra(f'Skipped {skipped_users} users')
        printer.end_stage()
        return local_users

