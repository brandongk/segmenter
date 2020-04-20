import argparse
from typing import Dict
import pprint
import os
import sys
from segmenter.config import validate_config
from launcher import Task
from segmenter.evaluators import Evaluators
from segmenter.tasks import BaseTask


class EvaluateTask(BaseTask):

    name = 'evaluate'

    def __init__(self, args):
        super().__init__(args)
        pprint.pprint(self.job_config)
        validate_config(self.job_config)
        self.evaluator = args["evaluator"].value
        if args["classes"] is not None:
            self.classes = list(
                filter(lambda c: c in args["classes"], self.classes))

    @staticmethod
    def arguments(parser) -> None:
        command_parser = parser.add_parser(EvaluateTask.name,
                                           help='Evaluate a model.')
        BaseTask.arguments(command_parser)

        command_parser.add_argument("--evaluator",
                                    type=Evaluators.argparse,
                                    default="metric",
                                    choices=list(Evaluators),
                                    help='the evaluation to perform.')
        command_parser.add_argument("--classes",
                                    type=str,
                                    help='the clases to train',
                                    required=False,
                                    nargs='+')

    @staticmethod
    def arguments_to_cli(args) -> str:
        return " ".join([
            args["dataset"], "--evaluator {}".format(args["evaluator"]),
            "--classes {}".format(" ".join(args["classes"]))
            if args["classes"] is not None else ""
        ])

    def execute(self) -> None:
        for clazz in self.classes:
            self.evaluator(clazz, self.job_config, self.job_hash,
                           self.data_dir, self.output_dir).execute()


tasks = [EvaluateTask]