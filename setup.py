import sys

from setuptools import setup

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

__version__ = "0.5.0"

setup(
    name="my-package",
    version=__version__,
    description="description",
    # And so on...
)
