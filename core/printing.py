from core.singleton import Singleton

import sys
import logging
import re
import base64
import os
import threading
try:
    import colorama
except:
    pass

# Logo
LOGO = 'CiAg4paI4paI4pWXICDilojilojilZfilojilojilojilZcgICDilojilojilojilZcgICAgICDilojilojilojilojilojilojilojilZfilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4paI4pWXCiAg4paI4paI4pWRICDilojilojilZHilojilojilojilojilZcg4paI4paI4paI4paI4pWRICAgICAg4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWd4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdCiAg4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4pWU4paI4paI4paI4paI4pWU4paI4paI4pWR4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4paI4paI4paI4pWXICAKICDilojilojilZTilZDilZDilojilojilZHilojilojilZHilZrilojilojilZTilZ3ilojilojilZHilZrilZDilZDilZDilZDilZ3ilZrilZDilZDilZDilZDilojilojilZHilojilojilZEgICDilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZTilZDilZDilZ0gIAogIOKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4pWRIOKVmuKVkOKVnSDilojilojilZEgICAgICDilojilojilojilojilojilojilojilZHilZrilojilojilojilojilojilojilZTilZ3ilojilojilZEgIOKWiOKWiOKVkeKWiOKWiOKVkSAgICAgCiAg4pWa4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZ0gICAgIOKVmuKVkOKVnSAgICAgIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSDilZrilZDilZDilZDilZDilZDilZ0g4pWa4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZ0gICAgIAogICAgICBUaGUgSGlkZGVuIE1hY2hpbmUgeW91IGNhbiBvbmx5IGdldCBpbiBTYWZhcmkhCiAgICAgICAgICBCeSBKb25hdGhhbiBCYXIgT3IgKEB5b195b195b19qYm8pCgo='

# Pretty-printing
PP_LEN = 116

# Initialize colorama
if 'colorama' in sys.modules:
    colorama.init()

class PrettyPrinter(metaclass=Singleton):
    """
        A pretty-printer container.
    """
    
    def __init__(self):
        """
            Create an instance.
        """
        
        # Save context
        self.extra = []
        self.in_stage = {}
        
        # Save lock
        self.lock = threading.Lock()
        
        # Save a log file handle
        self.log_file = None
        
        # Save colors
        has_colorama = 'colorama' in sys.modules
        self.color_white = colorama.Style.BRIGHT + colorama.Fore.WHITE if has_colorama else ''
        self.color_green = colorama.Style.BRIGHT + colorama.Fore.GREEN if has_colorama else ''
        self.color_red = colorama.Style.BRIGHT + colorama.Fore.RED if has_colorama else ''
        self.color_gray = colorama.Style.BRIGHT + colorama.Fore.LIGHTBLACK_EX if has_colorama else ''
        self.color_cyan = colorama.Style.BRIGHT + colorama.Fore.CYAN if has_colorama else ''
        self.color_yellow = colorama.Style.DIM + colorama.Fore.LIGHTYELLOW_EX if has_colorama else ''
        self.color_reset = colorama.Style.RESET_ALL if has_colorama else ''

    def print_logo(self):
        """
            Prints a pretty logo.
        """

        # Clear screen
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except:
            pass

        # Decode
        print(self.color_white + '\n' + base64.b64decode(LOGO).decode() + self.color_reset)
        sys.stdout.flush()

    def __del__(self):
        """
            Destructor.
        """
        
        # Close the file handle
        if self.log_file is not None:
            self.log_file.close()

    def set_log_file_path(self, log_file_path):
        """
            Sets a log file path.
        """
        
        # Save the log file (locked)
        with self.lock:
            self.log_file = open(log_file_path, 'a', encoding='utf-8')

    def print_raw_locked(self, msg, end='\n'):
        """
            Prints a message.
        """
        
        # Write to standard output and optionally to the log file
        print(msg, end=end)
        sys.stdout.flush()
        if self.log_file is not None:
            raw_msg = f'{PrintingConsoleHandler.remove_color_coding(msg)}{end}'
            self.log_file.write(raw_msg)
            self.log_file.flush()

    def start_stage(self, msg):
        """
            Starts a stage.
        """
        
        # Synchronize
        with self.lock:
        
            # Save state
            self.in_stage[threading.get_ident()] = True
        
            # Empty extra
            self.extra = []
            
            # Pretty-print
            msg = msg[:PP_LEN] + ' ...' + ('.' * (PP_LEN - len(msg))) + ' '
            self.print_raw_locked(msg, end='')

    def print_extra(self):
        """
            Prints extra data.
        """
        
        # Pretty-print
        if len(self.extra) > 0:
            msg = '\n'.join([ '  ' + i for i in self.extra ])
            self.print_raw_locked(msg)
            self.extra = []

    def end_stage(self, fail_msg=None):
        """
            Ends a stage.
        """
        
        # Synchronize
        with self.lock:
        
            # Pretty-print
            if fail_msg is None:
                self.print_raw_locked('[  ' + self.color_green + 'OK' + self.color_reset + '  ]')
                self.print_extra()
            else:
                if self.in_stage.get(threading.get_ident()) == True:
                    self.print_raw_locked('[ ' + self.color_red + 'FAIL' + self.color_reset + ' ]')
                self.extra = [ self.color_yellow + fail_msg + self.color_reset ]
                self.print_extra()
                
            # Save context
            self.in_stage[threading.get_ident()] = False
    
    def append_warning(self, info):
        """
            Adds a warning.
        """
        
        # Append the info as extra
        self.append_extra(self.color_yellow + info + self.color_reset)
    
    def append_extra(self, info, emphasize=False):
        """
            Adds extra information.
        """
        
        # Synchronize
        with self.lock:
        
            # Simply append
            start_color = self.color_cyan if emphasize else self.color_gray
            self.extra.append(start_color + info + self.color_reset)
            
            # Print if not in stage
            if self.in_stage.get(threading.get_ident()) != True:
                self.print_extra()
                
    def finalize(self):
        """
            Finalize with a message.
        """
        
        # Synchronize
        with self.lock:
        
            # Simply write
            self.print_raw_locked('\nFinished ' + self.color_cyan + 'successfully' + self.color_reset + '.')

class PrintingConsoleHandler(logging.StreamHandler):
    """
        Custom logging handler.
    """
    
    @staticmethod
    def remove_color_coding(msg):
        """
            Removes color coding from the given message.
        """
        
        # Remove with a regular expression
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', msg)
    
    def emit(self, record):
        """
            Emits a record.
        """
        
        # Get the printer
        printer = PrettyPrinter.get_instance()
        
        # Print message without colors
        raw_message = PrintingConsoleHandler.remove_color_coding(record.getMessage())
        for chunk in raw_message.split('\n'):
            printer.append_extra(chunk)

# Create the global instance already
global_printer = PrettyPrinter()

