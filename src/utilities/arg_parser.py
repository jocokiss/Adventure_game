"""Module used to parse arguments from command line or .env.settings files."""
from argparse import ArgumentParser, Namespace

from dotenv import dotenv_values


class ArgParser:
    """Class used to parse arguments from command line or .env.settings files."""

    def __init__(self) -> None:
        self.parser = ArgumentParser()

    def run(self) -> Namespace:
        """Return parsed arguments from command line or .env.settings files."""

        local_arguments = dotenv_values(".env.settings")
        for key, value in local_arguments.items():
            self.parser.add_argument(f"--{key}", default=value)

        return self.parser.parse_args()
