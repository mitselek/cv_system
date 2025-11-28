package storage

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/michelek/cv_system/email-monitor/internal/classifier"
)

type CommunicationData struct {
	Date     time.Time
	From     string
	FromAddr string
	Subject  string
	Body     string
	Type     classifier.CommType
}

func SaveCommunication(basePath, appPath string, data CommunicationData) (string, error) {
	// Create full path: basePath/appPath/communications/
	commDir := filepath.Join(basePath, appPath, "communications")
	
	if err := os.MkdirAll(commDir, 0755); err != nil {
		return "", fmt.Errorf("failed to create communications directory: %w", err)
	}
	
	// Generate filename: YYYY-MM-DD_type.md
	filename := fmt.Sprintf("%s_%s.md", data.Date.Format("2006-01-02"), data.Type)
	fullPath := filepath.Join(commDir, filename)
	
	// Check if file already exists
	if _, err := os.Stat(fullPath); err == nil {
		return fullPath, fmt.Errorf("file already exists: %s", filename)
	}
	
	// Generate markdown content
	content := fmt.Sprintf(`# Communication: %s

**Date:** %s
**From:** %s <%s>
**Subject:** %s

---

%s
`,
		data.Type.TitleCase(),
		data.Date.Format("2006-01-02"),
		data.From,
		data.FromAddr,
		data.Subject,
		data.Body,
	)
	
	// Write file
	if err := os.WriteFile(fullPath, []byte(content), 0644); err != nil {
		return "", fmt.Errorf("failed to write file: %w", err)
	}
	
	return fullPath, nil
}
