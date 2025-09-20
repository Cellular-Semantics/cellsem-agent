"""
Configuration for the DeepSearch agent.
"""
from dataclasses import dataclass
import os
from typing import Optional

from aurelian.dependencies.workdir import HasWorkdir, WorkDir


@dataclass
class DeepSearchDependencies(HasWorkdir):
    """
    Configuration for the DeepSearch agent.

    Uses o1-mini-deep-research model for literature analysis.
    """

    def __post_init__(self):
        """Initialize the config with default values."""
        if self.workdir is None:
            self.workdir = WorkDir()


def get_config() -> DeepSearchDependencies:
    """Get the DeepSearch configuration from environment variables or defaults."""
    workdir_path = os.environ.get("AURELIAN_WORKDIR", None)
    workdir = WorkDir(location=workdir_path) if workdir_path else None

    config = DeepSearchDependencies(workdir=workdir)
    return config