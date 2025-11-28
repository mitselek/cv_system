package config

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	IMAP       IMAPConfig
	Processing ProcessingConfig
	Output     OutputConfig
}

type IMAPConfig struct {
	Server   string
	Port     int
	Username string
	Password string
	Folder   string
}

type ProcessingConfig struct {
	LookbackDays int
	DryRun       bool
}

type OutputConfig struct {
	BasePath     string
	RegistryPath string
	StatePath    string
}

func Load() (*Config, error) {
	// Try to load .env file (ignore error if it doesn't exist)
	_ = godotenv.Load()

	username := os.Getenv("EMAIL_USER")
	password := os.Getenv("EMAIL_APP_PASSWORD")

	if username == "" {
		return nil, fmt.Errorf("EMAIL_USER environment variable not set")
	}
	if password == "" {
		return nil, fmt.Errorf("EMAIL_APP_PASSWORD environment variable not set")
	}

	// Check for dry-run mode
	dryRun := os.Getenv("DRY_RUN") == "true" || os.Getenv("DRY_RUN") == "1"

	return &Config{
		IMAP: IMAPConfig{
			Server:   "imap.gmail.com",
			Port:     993,
			Username: username,
			Password: password,
			Folder:   "[Gmail]/All Mail",
		},
		Processing: ProcessingConfig{
			LookbackDays: 7,
			DryRun:       dryRun,
		},
		Output: OutputConfig{
			BasePath:     "../applications",
			RegistryPath: "../applications/REGISTRY.md",
			StatePath:    ".email-monitor-state.json",
		},
	}, nil
}
