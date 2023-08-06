# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Console interface for AutoML experiments logs."""

from datetime import datetime
import json
import numpy as np
import os
import pytz
import sys
import time

from automl.client.core.common import logging_utilities
from automl.client.core.common.metrics import minimize_or_maximize

from . import automl, constants


class ConsoleInterface(object):
    """Class responsible for printing iteration information to console."""

    def __init__(self, metric, file_handler=None):
        """
        Create a ConsoleInterface object.

        Arguments:
        :param metric: str representing which metric is being used to score the pipeline
        :param training_type: str representing what type of training is being executed
        :param logger:
        """
        self.metric = metric
        self.metric_pretty = metric
        self.file_handler = file_handler
        if file_handler is None:
            self.file_handler = open(os.devnull, 'w')

        self.columns = [
            "ITERATION",
            "PIPELINE",
            "TRAINFRAC",
            "DURATION",  # "MESSAGE",
            "METRIC",
            "BEST",
        ]
        self.descriptions = [
            "The iteration being evaluated.",
            "A summary description of the pipeline being evaluated.",
            "Fraction of the training data to train on.",
            "Time taken for the current iteration.",  # "Error or warning message for the current iteration.",
            "The result of computing %s on the fitted pipeline." % (self.metric_pretty,),
            "The best observed %s thus far." % self.metric_pretty,
        ]

        self.widths = [
            10,
            48,
            12,
            10,
            10,
            10
        ]
        self.sep_width = 3
        self.filler = " "
        self.total_width = sum(self.widths) + self.sep_width

    def _format_float(self, v):
        if isinstance(v, float):
            return "{:.4f}".format(v)
        return v

    def _format_int(self, v):
        if isinstance(v, int):
            return "%d" % v
        return v

    def print_descriptions(self):
        """
        Print description of AutoML console output.

        :return:
        """
        self.file_handler.write("\n")
        self.file_handler.write(("*" * self.total_width) + '\n')
        for column, description in zip(self.columns, self.descriptions):
            self.file_handler.write(column + ": " + description + '\n')
        self.file_handler.write("*" * self.total_width + '\n')
        self.file_handler.write("\n")

    def print_columns(self):
        """
        Print column headers for AutoML printing block.

        :return:
        """
        self.print_start(self.columns[0])
        self.print_pipeline(self.columns[1], '', self.columns[2])
        self.print_end(self.columns[3], self.columns[4], self.columns[5])

    def print_start(self, iteration=""):
        """
        Print iteration number.

        Arguments:
        :param iteration: iteration number.
        :return:
        """
        iteration = self._format_int(iteration)

        s = ""
        s += iteration.rjust(self.widths[0], self.filler)[-self.widths[0]:] + self.filler * self.sep_width
        self.file_handler.write(s)
        sys.stdout.flush()

    def print_pipeline(self, preprocessor='', model_name='', train_frac=1):
        """
        Format a sklearn Pipeline string to be readable.

        Arguments:
        :param preprocessor: string of preprocessor name
        :param model_name: string of model name
        :param train_frac: float of fraction of train data to use
        :return:
        """
        separator = ' '
        if preprocessor is None:
            preprocessor = ''
            separator = ''
        if model_name is None:
            model_name = ''
        combined = preprocessor + separator + model_name
        train_frac = str(self._format_float(train_frac))
        self.file_handler.write(combined.ljust(self.widths[1], self.filler)[:(self.widths[1] - 1)])
        self.file_handler.write(train_frac.ljust(self.widths[2], self.filler)[:(self.widths[2] - 1)])
        sys.stdout.flush()

    def print_end(self, duration="", metric="", best_metric=""):
        """
        Print iteration status, metric, and running best metric.

        Arguments:
        :param duration: Status of the given iteration
        :param metric: Score for this iteration
        :param best_metric: Best score so far
        :return:
        """
        metric, best_metric = tuple(map(self._format_float, (metric, best_metric)))
        duration, metric, best_metric = tuple(map(str, (duration, metric, best_metric)))
        metric = str(metric)
        s = ""
        s += duration.ljust(self.widths[3], self.filler)
        s += metric.rjust(self.widths[4], self.filler)
        s += best_metric.rjust(self.widths[5], self.filler)
        self.file_handler.write(s + '\n')
        sys.stdout.flush()

    def print_error(self, message):
        """
        Print an error message to the console.

        Arguments:
        :param message: Error message to display to user
        :return:
        """
        self.file_handler.write('ERROR: ')
        self.file_handler.write(str(message).ljust(self.widths[1], self.filler) + '\n')
        sys.stdout.flush()


class RemoteConsoleInterface(ConsoleInterface):
    """Class responsible for printing iteration information to console for a remote run."""

    def __init__(self, logger, file_logger=None):
        """
        Create an instance of the RemoteConsoleInterface class.

        Arguments:
        :param logger: Console logger for printing this info
        :param file_logger: Optional file logger for more detailed logs
        """
        self._console_logger = logger
        self.logger = file_logger
        self.metric_map = {}
        self.run_map = {}
        self.properties_map = {}
        self.best_metric = None
        super().__init__("score", self._console_logger)

    def print(self, parent_run, primary_metric, iterations):
        """
        Print all history for a given parent run.

        Arguments:
        :param parent_run: AutoMLRun to print status for
        :param primary_metric: Metric being optimized for this run
        :param iterations: How many iterations to print total
        :return:
        """
        try:
            self.print_descriptions()
            self.print_columns()
        except Exception as e:
            logging_utilities.log_traceback(e, self.logger)
            raise
        print_loop = True
        best_metric = None
        while print_loop:
            status = parent_run.get_tags().get('_aml_system_automl_status', None)
            if status is None:
                status = parent_run.get_status()
            if status in ('Completed', 'Failed', 'Canceled'):
                print_loop = False
            children = sorted(list(parent_run.get_children(_rehydrate_runs=False)), key=lambda run: run._run_number)
            if children is None:
                continue

            for run in children:
                run_id = run.id
                status = run.get_status()
                if ((run_id not in self.run_map) and
                        (status in ('Completed', 'Failed'))):
                    metrics = run.get_metrics()
                    properties = run.get_properties()
                    self.metric_map[run_id] = metrics
                    self.run_map[run_id] = run
                    self.properties_map[run_id] = properties
                    if 'iteration' in properties:
                        current_iter = properties['iteration']
                    else:
                        current_iter = run_id.split('_')[-1]

                    print_line = ""
                    if 'run_preprocessor' in properties:
                        print_line += properties['run_preprocessor']
                    if 'run_algorithm' in properties:
                        print_line += " " + properties['run_algorithm']

                    train_frac = 1
                    if 'training_percent' in properties and \
                            properties['training_percent']:
                        train_frac = float(properties['training_percent']) / 100

                    created_time = run._run_dto['created_utc']
                    if isinstance(created_time, str):
                        created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                    start_iter_time = created_time.replace(tzinfo=pytz.UTC)
                    end_iter_time = datetime.strptime(run.get_details()['endTimeUtc'],
                                                      '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
                    iter_duration = str(end_iter_time - start_iter_time).split(".")[0]

                    objective = minimize_or_maximize(metric=primary_metric)
                    if primary_metric in metrics:
                        score = metrics[primary_metric]
                    else:
                        score = constants.Defaults.DEFAULT_PIPELINE_SCORE

                    if best_metric is None or best_metric == 'nan' or np.isnan(best_metric):
                        best_metric = score
                    elif objective == constants.OptimizerObjectives.MINIMIZE:
                        if score < best_metric:
                            best_metric = score
                    elif objective == constants.OptimizerObjectives.MAXIMIZE:
                        if score > best_metric:
                            best_metric = score
                    else:
                        best_metric = 'Unknown'

                    self.print_start(current_iter)
                    self.print_pipeline(print_line, train_frac=train_frac)
                    self.print_end(iter_duration, score, best_metric)

                    errors = properties.get('friendly_errors')
                    if errors is not None:
                        error_dict = json.loads(errors)
                        for error in error_dict:
                            self.print_error(error_dict[error])
            time.sleep(3)

    @staticmethod
    def _show_output(current_run, logger, file_logger, primary_metric, iterations):
        try:
            remote_printer = RemoteConsoleInterface(
                logger, file_logger)
            remote_printer.print(current_run, primary_metric, iterations)
        except KeyboardInterrupt:
            logger.write("Received interrupt. Returning now.")
