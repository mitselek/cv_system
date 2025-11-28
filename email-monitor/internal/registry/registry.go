package registry

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Application struct {
	Company  string
	Position string
	Path     string
}

func LoadApplications(registryPath string) ([]Application, error) {
	file, err := os.Open(registryPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open registry: %w", err)
	}
	defer file.Close()

	var apps []Application
	scanner := bufio.NewScanner(file)
	inTable := false

	for scanner.Scan() {
		line := scanner.Text()
		
		// Skip until we find the table
		if strings.HasPrefix(line, "|") && strings.Contains(line, "Company") {
			inTable = true
			scanner.Scan() // Skip separator line
			continue
		}
		
		if !inTable {
			continue
		}
		
		// Parse table row
		if strings.HasPrefix(line, "|") {
			parts := strings.Split(line, "|")
			if len(parts) < 4 {
				continue
			}
			
			// Extract fields: | Date | Company | Position | ...
			company := strings.TrimSpace(parts[2])
			position := strings.TrimSpace(parts[3])
			
			if company == "" || company == "---" {
				continue
			}
			
			// Extract path from Application Link column (index 5)
			if len(parts) > 5 {
				linkCol := strings.TrimSpace(parts[5])
				// Extract path from [README](path) format
				if strings.Contains(linkCol, "](") {
					start := strings.Index(linkCol, "](") + 2
					end := strings.Index(linkCol[start:], ")")
					if end > 0 {
						path := linkCol[start : start+end]
						// Convert relative path to company/position format
						pathParts := strings.Split(path, "/")
						if len(pathParts) >= 2 {
							apps = append(apps, Application{
								Company:  company,
								Position: position,
								Path:     fmt.Sprintf("%s/%s", pathParts[0], pathParts[1]),
							})
						}
					}
				}
			}
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading registry: %w", err)
	}

	return apps, nil
}
