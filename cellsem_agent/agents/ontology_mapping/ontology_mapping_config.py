"""
Configuration for the Ontology Mapping agent.
"""
from dataclasses import dataclass
import os
from typing import List, Optional

from aurelian.dependencies.workdir import HasWorkdir, WorkDir


@dataclass
class OntologyMappingDependencies(HasWorkdir):
    """
    Configuration for the Ontology Mapping agent.

    Maps atomic functions and cellular components to terms in OLS ontologies.
    Target ontologies include GO, CL, UBERON, and others as appropriate.
    """
    target_ontologies: List[str] = None

    def __post_init__(self):
        """Initialize the config with default values."""
        if self.workdir is None:
            self.workdir = WorkDir()
        if self.target_ontologies is None:
            # Default ontologies for functional and anatomical mapping
            self.target_ontologies = [
                "GO",     # Gene Ontology (molecular functions, biological processes, cellular components)
                "CL",     # Cell Ontology
                "UBERON", # Uber-anatomy ontology
                "CHEBI",  # Chemical Entities of Biological Interest
                "PR"      # Protein Ontology
            ]


def get_config(target_ontologies: Optional[List[str]] = None) -> OntologyMappingDependencies:
    """Get the Ontology Mapping configuration from environment variables or defaults."""
    workdir_path = os.environ.get("AURELIAN_WORKDIR", None)
    workdir = WorkDir(location=workdir_path) if workdir_path else None

    config = OntologyMappingDependencies(
        workdir=workdir,
        target_ontologies=target_ontologies
    )
    return config