"""
Configuration for the Decomposition agent.
"""
from dataclasses import dataclass
import os
from typing import Optional

from aurelian.dependencies.workdir import HasWorkdir, WorkDir


@dataclass
class DecompositionDependencies(HasWorkdir):
    """
    Configuration for the Decomposition agent.

    Breaks down high-level functions into atomic components.
    """

    def __post_init__(self):
        """Initialize the config with default values."""
        if self.workdir is None:
            self.workdir = WorkDir()


def get_config() -> DecompositionDependencies:
    """Get the Decomposition configuration from environment variables or defaults."""
    workdir_path = os.environ.get("AURELIAN_WORKDIR", None)
    workdir = WorkDir(location=workdir_path) if workdir_path else None

    config = DecompositionDependencies(workdir=workdir)
    return config