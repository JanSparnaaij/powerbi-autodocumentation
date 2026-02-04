"""Base documentation engine interface for Power BI models.

This module defines the abstract interface that all documentation engines must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ModelMetadata:
    """Container for extracted Power BI model metadata."""
    
    summary: dict[str, Any]
    tables: list[Any]  # List of Table objects
    measures: list[Any]  # List of Measure objects
    relationships: list[Any]  # List of Relationship objects
    power_query: dict[str, str] | None = None


class IDocumentationEngine(ABC):
    """Abstract interface for Power BI documentation engines.
    
    All documentation engines (pbixray, MCP, etc.) must implement this interface
    to provide a consistent API for metadata extraction.
    """
    
    @abstractmethod
    async def load_model(self, source: str, **kwargs) -> None:
        """Load a Power BI model from a source (file path, connection string, etc.).
        
        Args:
            source: Model source identifier (file path, PBIP folder, connection string)
            **kwargs: Engine-specific loading options
            
        Raises:
            FileNotFoundError: If source file/folder doesn't exist
            RuntimeError: If model loading fails
        """
        pass
    
    @abstractmethod
    async def extract_metadata(self) -> ModelMetadata:
        """Extract all metadata from the loaded model.
        
        Returns:
            ModelMetadata: Container with all extracted metadata
            
        Raises:
            RuntimeError: If no model is loaded or extraction fails
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the engine and release resources.
        
        This should be called when the engine is no longer needed to clean up
        connections, processes, etc.
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
