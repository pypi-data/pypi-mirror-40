import logging

import fs
from cliff.command import Command

from ..constants import BASE_CONFIG_EXAMPLE, CURRENT_DIR
from ..exceptions import CommandFailure
from ..helpers import (check_config_existence, get_config_example,
                       get_providers, snakeless_spinner)


class Init(Command):
    "Create initial snakeless.yml configuration"

    logger = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Rewrite current config if it exists",
        )
        available_providers = ["base"] + list(get_providers().keys())
        parser.add_argument(
            "-p",
            "--provider",
            default="base",
            choices=available_providers,
            help="Which provider's example we should use",
        )
        return parser

    def check_config_existence(self, root_fs):
        with snakeless_spinner(
            text="Checking the config existence.", spinner="dots"
        ) as spinner:
            config_file_exists = check_config_existence(root_fs)
            if config_file_exists:
                raise CommandFailure("Config was found. Ignore it with -f")
            else:
                spinner.succeed("Config was not found.")

    def create_configuration(self, root_fs, provider):
        with snakeless_spinner(
            text="Creating configuration", spinner="dots"
        ) as spinner:
            if provider == "base":
                config_example = BASE_CONFIG_EXAMPLE
            else:
                try:
                    config_example = get_config_example(provider)
                except KeyError:
                    raise CommandFailure("Plugin doesn't provide example config")
            root_fs.writetext("snakeless.yml", config_example)
            spinner.succeed("Config was created")

    def take_action(self, parsed_args):
        parsed_args = vars(parsed_args)
        ignore_config = parsed_args.get("force", False)
        provider = parsed_args.get("provider", "base")
        with fs.open_fs(CURRENT_DIR) as root_fs:
            try:
                if not ignore_config:
                    self.check_config_existence(root_fs)
                self.create_configuration(root_fs, provider)
            except Exception as exc:
                self.logger.exception(exc, exc_info=True)
