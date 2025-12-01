"""
Configuration management for job monitoring system.

This module handles loading, validating, and accessing configuration from YAML/JSON files.
"""

import json
from pathlib import Path
from typing import Any

import yaml

from schemas import SystemConfig


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""

    pass


class ConfigManager:
    """Manages system configuration with validation and easy access."""

    def __init__(self, config_path: Path | str) -> None:
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file (YAML or JSON)

        Raises:
            ConfigurationError: If config file doesn't exist or is invalid
        """
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")

        self._config: SystemConfig | None = None
        self._load_config()

    def _load_config(self) -> None:
        """
        Load and validate configuration from file.

        Raises:
            ConfigurationError: If file cannot be parsed or validation fails
        """
        try:
            with open(self.config_path, encoding="utf-8") as f:
                if self.config_path.suffix in [".yaml", ".yml"]:
                    data = yaml.safe_load(f)
                elif self.config_path.suffix == ".json":
                    data = json.load(f)
                else:
                    raise ConfigurationError(
                        f"Unsupported config format: {self.config_path.suffix}. "
                        "Use .yaml, .yml, or .json"
                    )

            # Validate with Pydantic
            self._config = SystemConfig(**data)

        except yaml.YAMLError as e:
            raise ConfigurationError(f"YAML parsing error: {e}") from e
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"JSON parsing error: {e}") from e
        except Exception as e:
            raise ConfigurationError(f"Configuration validation failed: {e}") from e

    @property
    def config(self) -> SystemConfig:
        """
        Get validated configuration.

        Returns:
            Validated SystemConfig instance
        """
        if self._config is None:
            raise ConfigurationError("Configuration not loaded")
        return self._config

    def get_enabled_sources(self) -> list[str]:
        """
        Get list of enabled source names.

        Returns:
            List of source names where enabled=True
        """
        return [source.name for source in self.config.sources if source.enabled]

    def get_source_queries(self, source_name: str) -> list[dict[str, Any]]:
        """
        Get queries for a specific source.

        Args:
            source_name: Name of the source portal

        Returns:
            List of query configurations as dictionaries

        Raises:
            ConfigurationError: If source not found
        """
        for source in self.config.sources:
            if source.name == source_name:
                return [
                    {
                        "keywords": q.keywords,
                        "location": q.location,
                        "limit": q.limit,
                    }
                    for q in source.queries
                ]
        raise ConfigurationError(f"Source not found: {source_name}")

    def reload(self) -> None:
        """
        Reload configuration from file.

        Useful for picking up config changes without restarting.

        Raises:
            ConfigurationError: If reload fails
        """
        self._load_config()

    def validate_paths(self) -> list[str]:
        """
        Validate that required directories/files exist.

        Returns:
            List of validation warnings (empty if all OK)
        """
        warnings = []

        # Check if state file directory exists
        state_dir = self.config.state_file.parent
        if not state_dir.exists():
            warnings.append(f"State file directory does not exist: {state_dir}")

        # Check if candidates directory exists
        if not self.config.candidates_dir.exists():
            warnings.append(
                f"Candidates directory does not exist: {self.config.candidates_dir}"
            )

        # Check if cookies files exist for sources that need them
        for source in self.config.sources:
            if source.cookies_file:
                if not source.cookies_file.exists():
                    warnings.append(
                        f"Cookies file for {source.name} not found: {source.cookies_file}"
                    )

        return warnings

    def __repr__(self) -> str:
        """String representation."""
        enabled = len(self.get_enabled_sources())
        total = len(self.config.sources)
        return f"ConfigManager({self.config_path}, {enabled}/{total} sources enabled)"


def load_config(config_path: Path | str) -> SystemConfig:
    """
    Convenience function to load and validate configuration.

    Args:
        config_path: Path to configuration file

    Returns:
        Validated SystemConfig instance

    Raises:
        ConfigurationError: If loading or validation fails

    Example:
        >>> config = load_config("config.yaml")
        >>> print(config.sources[0].name)
    """
    manager = ConfigManager(config_path)
    return manager.config
