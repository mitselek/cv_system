"""
Tests for ConfigManager.

Tests configuration loading, validation, and access methods.
"""

from pathlib import Path

from job_monitor.config import ConfigManager, ConfigurationError, load_config


def test_load_yaml_config() -> None:
    """Test loading YAML configuration."""
    manager = ConfigManager("config.example.yaml")
    assert manager.config is not None
    assert len(manager.config.sources) == 3
    print("✅ YAML config loaded successfully")


def test_get_enabled_sources() -> None:
    """Test getting enabled sources."""
    manager = ConfigManager("config.example.yaml")
    enabled = manager.get_enabled_sources()
    assert len(enabled) == 2  # cv.ee and cvkeskus.ee
    assert "cv.ee" in enabled
    assert "cvkeskus.ee" in enabled
    assert "duunitori.fi" not in enabled  # disabled
    print(f"✅ Got {len(enabled)} enabled sources: {enabled}")


def test_get_source_queries() -> None:
    """Test getting queries for a source."""
    manager = ConfigManager("config.example.yaml")
    queries = manager.get_source_queries("cv.ee")
    assert len(queries) == 2
    assert queries[0]["keywords"] == "python django postgresql"
    assert queries[0]["limit"] == 50
    print(f"✅ Got {len(queries)} queries for cv.ee")


def test_get_source_queries_not_found() -> None:
    """Test getting queries for non-existent source."""
    manager = ConfigManager("config.example.yaml")
    try:
        manager.get_source_queries("nonexistent")
        assert False, "Should raise ConfigurationError"
    except ConfigurationError as e:
        assert "not found" in str(e).lower()
        print("✅ ConfigurationError raised for non-existent source")


def test_validate_paths() -> None:
    """Test path validation."""
    manager = ConfigManager("config.example.yaml")
    warnings = manager.validate_paths()
    # Warnings expected if directories don't exist, empty list if they do
    assert isinstance(warnings, list)
    print(f"✅ Path validation found {len(warnings)} warnings")


def test_load_config_convenience() -> None:
    """Test convenience load_config function."""
    config = load_config("config.example.yaml")
    assert config is not None
    assert len(config.sources) == 3
    assert config.scoring.remote_bonus == 15.0
    assert config.scan_interval_hours == 6
    print("✅ Convenience load_config() works")


def test_config_properties() -> None:
    """Test configuration properties."""
    config = load_config("config.example.yaml")
    
    # Check scoring config
    assert len(config.scoring.positive_keywords) == 10
    assert "python" in config.scoring.positive_keywords
    assert len(config.scoring.negative_keywords) == 4
    assert config.scoring.days_threshold_fresh == 7
    
    # Check paths
    assert config.state_file == Path("state/monitor_state.json")
    assert config.candidates_dir == Path("candidates/")
    
    print("✅ All config properties validated")


def test_config_file_not_found() -> None:
    """Test error when config file doesn't exist."""
    try:
        ConfigManager("nonexistent.yaml")
        assert False, "Should raise ConfigurationError"
    except ConfigurationError as e:
        assert "not found" in str(e).lower()
        print("✅ ConfigurationError raised for missing file")


def test_repr() -> None:
    """Test ConfigManager string representation."""
    manager = ConfigManager("config.example.yaml")
    repr_str = repr(manager)
    assert "ConfigManager" in repr_str
    assert "config.example.yaml" in repr_str
    assert "2/3 sources enabled" in repr_str
    print(f"✅ __repr__ works: {repr_str}")


if __name__ == "__main__":
    test_load_yaml_config()
    test_get_enabled_sources()
    test_get_source_queries()
    test_get_source_queries_not_found()
    test_validate_paths()
    test_load_config_convenience()
    test_config_properties()
    test_config_file_not_found()
    test_repr()
    print("\n🎉 All ConfigManager tests passed!")
