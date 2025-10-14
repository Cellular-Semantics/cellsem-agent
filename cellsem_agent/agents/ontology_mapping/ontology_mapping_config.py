"""
Configuration for the Ontology Mapping agent.
"""
from dataclasses import dataclass
import os
from typing import List, Optional
from pathlib import Path


@dataclass
class OntologyMappingDependencies:
    """
    Configuration for the Ontology Mapping agent.

    Maps atomic functions and cellular components to terms in OLS ontologies.
    Target ontologies include GO, CL, UBERON, and others as appropriate.
    """
    workdir: Optional[Path] = None
    target_ontologies: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize the config with default values."""
        if self.workdir is None:
            workdir_path = os.environ.get("WORKDIR", "./workdir")
            self.workdir = Path(workdir_path)
            # Create workdir if it doesn't exist
            self.workdir.mkdir(parents=True, exist_ok=True)

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
    return OntologyMappingDependencies(target_ontologies=target_ontologies)