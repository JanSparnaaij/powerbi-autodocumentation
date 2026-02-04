# src/generators/wiki_generator.py
import os
import asyncio
import logging
from pathlib import Path
from typing import Any

from ..engines import get_engine, IDocumentationEngine
from .mermaid import generate_er_diagram
from .pages import (
    generate_home_page,
    generate_table_page,
    generate_measures_page,
    generate_relationships_page,
    generate_data_sources_page,
)


logger = logging.getLogger(__name__)


class WikiGenerator:
    """Generates documentation pages from Power BI models."""
    
    def __init__(self, output_dir: str):
        self.base_output_dir = Path(output_dir)
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate(
        self,
        source: str,
        model_name: str | None = None,
        engine_type: str = "pbixray",
        engine_kwargs: dict[str, Any] | None = None
    ):
        """Generate complete documentation from a Power BI model.
        
        Args:
            source: Model source (PBIX file, PBIP folder, connection string)
            model_name: Display name for the model (derived from source if not provided)
            engine_type: Documentation engine to use ("pbixray" or "mcp")
            engine_kwargs: Engine-specific configuration options
        """
        if engine_kwargs is None:
            engine_kwargs = {}
        
        if not model_name:
            model_name = Path(source).stem
        
        # Create a subfolder for this model
        model_slug = self._slugify(model_name)
        self.output_dir = self.base_output_dir / model_slug
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Generating documentation for {model_name}...")
        logger.info(f"Output folder: {self.output_dir}")
        logger.info(f"Using engine: {engine_type}")
        
        # Create engine instance
        try:
            engine = get_engine(engine_type, **engine_kwargs)
        except Exception as e:
            logger.error(f"Failed to create engine '{engine_type}': {e}")
            raise RuntimeError(f"Engine initialization failed: {e}")
        
        # Extract metadata using engine
        try:
            async with engine:
                logger.info(f"Loading model from: {source}")
                await engine.load_model(source)
                
                logger.info("Extracting metadata...")
                metadata = await engine.extract_metadata()
                
                summary = metadata.summary
                tables = metadata.tables
                measures = metadata.measures
                relationships = metadata.relationships
                power_query = metadata.power_query
                
                logger.info(
                    f"Found {len(tables)} tables, {len(measures)} measures, "
                    f"{len(relationships)} relationships"
                )
        
        except FileNotFoundError as e:
            logger.error(f"Source not found: {e}")
            raise
        except RuntimeError as e:
            logger.error(f"Engine error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during metadata extraction: {e}")
            raise RuntimeError(f"Metadata extraction failed: {e}")
        
        # Generate pages
        logger.info("Generating documentation pages...")
        self._write_page("Home", generate_home_page(
            model_name, summary, tables, measures
        ))
        
        for table in tables:
            page_name = f"Table-{self._slugify(table.name)}"
        for table in tables:
            page_name = f"Table-{self._slugify(table.name)}"
            self._write_page(page_name, generate_table_page(
                table, measures
            ))
        
        self._write_page("Measures", generate_measures_page(measures))
        
        er_diagram = generate_er_diagram(
            relationships,
            [t.name for t in tables]
        )
        self._write_page("Relationships", generate_relationships_page(
            relationships, er_diagram
        ))
        
        self._write_page("Data-Sources", generate_data_sources_page(power_query))
        
        # Create index page in base directory listing all models
        self._create_models_index()
        
        logger.info(f"✓ Documentation generated in {self.output_dir}")
        logger.info(f"  - Home page")
        logger.info(f"  - {len(tables)} table pages")
        logger.info(f"  - Measures page")
        logger.info(f"  - Relationships page")
        logger.info(f"  - Data Sources page")
    
    def _write_page(self, page_name: str, content: str):
        """Write a wiki page to disk."""
        file_path = self.output_dir / f"{page_name}.md"
        file_path.write_text(content, encoding="utf-8")
    
    def _create_models_index(self):
        """Create an index page listing all models in the base directory."""
        index_path = self.base_output_dir / "README.md"
        
        # Find all model folders
        model_folders = [d for d in self.base_output_dir.iterdir() if d.is_dir()]
        
        if not model_folders:
            return
        
        content = "# Power BI Models Documentation\n\n"
        content += f"This repository contains auto-generated documentation for {len(model_folders)} Power BI model(s).\n\n"
        content += "## Available Models\n\n"
        
        for folder in sorted(model_folders):
            # Read model name from Home.md if it exists
            home_file = folder / "Home.md"
            model_display_name = folder.name.replace("-", " ").title()
            
            if home_file.exists():
                # Try to extract model name from Home.md first line
                first_line = home_file.read_text(encoding="utf-8").split("\n")[0]
                if first_line.startswith("# "):
                    model_display_name = first_line[2:].split(" - ")[0]
            
            content += f"- **[{model_display_name}]({folder.name}/Home.md)**\n"
        
        content += "\n---\n\n"
        content += "*Documentation automatically generated by Power BI Auto-Documentation Pipeline*\n"
        
        index_path.write_text(content, encoding="utf-8")
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-safe slug."""
        return text.lower().replace(" ", "-").replace("_", "-")
