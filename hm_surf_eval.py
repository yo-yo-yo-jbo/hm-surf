#!/usr/bin/env python3
from core.lib import BrowserEvaluatorBase
from core.printing import PrettyPrinter
from core.utils import Utils

import sys
import os
import traceback

# Printer
printer = PrettyPrinter.get_instance()

def main():
    """
        Main routine.
    """

    # Print the logo
    printer.print_logo()

    # Catch-all
    try:

        # Summary
        summary = {}

        # Get all evaluators
        base_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], 'evaluators'))
        evaluators = Utils.get_evaluators(base_path)

        # Iterate all relevant users
        users = Utils.get_all_users()
        for username, home_dir in users.items():

            # Run all evaluators
            for evaluator in evaluators:

                # Get the results and add them
                printer.start_stage(f'Evaluating for user {username} over browser {evaluator.get_browser_name()}')
                eval_results = evaluator.evaluate(username, home_dir)
                if eval_results is not None:
                    for modifiable_setting_filepath in eval_results.modifiable_settings_filepaths:
                        printer.append_extra(f'⚠️  File "{modifiable_setting_filepath}" is modifiable!')
                    for approved_resource in eval_results.approved_resources:
                        expiration_time = 'until {approved_resource.expiration_time}' if approved_resource.expiration_time is not None else 'indefinitely'
                        printer.append_extra(f'Origin "{approved_resource.origin}" has access to {approved_resource.resource_type.name.lower()} {expiration_time}')
                printer.end_stage()

                # Add to summary
                if eval_results is not None and eval_results.is_heuristically_vulnerable():
                    if username not in summary:
                        summary[username] = []
                    summary[username].append(evaluator.get_browser_name())

        # Summarize
        printer.start_stage('Summarizing')
        for username, browsers in summary.items():
            vuln_browsers = ', '.join(browsers)
            printer.append_extra(f'🛑 User "{username}" has vulnerable browsers: {vuln_browsers}')
        printer.end_stage()

    # Catch exceptions
    except Exception as ex:
        printer.end_stage(''.join(traceback.format_exc()))
        sys.exit(-1)

    # Finalize
    printer.finalize()

if __name__ == '__main__':
    main()
