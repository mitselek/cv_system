package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"

	"github.com/michelek/cv_system/email-monitor/config"
	"github.com/michelek/cv_system/email-monitor/internal/classifier"
	"github.com/michelek/cv_system/email-monitor/internal/imap"
	"github.com/michelek/cv_system/email-monitor/internal/matcher"
	"github.com/michelek/cv_system/email-monitor/internal/parser"
	"github.com/michelek/cv_system/email-monitor/internal/registry"
	"github.com/michelek/cv_system/email-monitor/internal/state"
	"github.com/michelek/cv_system/email-monitor/internal/storage"
)

// SavedFile tracks a saved communication file
type SavedFile struct {
	Path    string
	Subject string
}

func main() {
	// Suppress log output unless VERBOSE is set
	if os.Getenv("VERBOSE") != "true" && os.Getenv("VERBOSE") != "1" {
		log.SetOutput(io.Discard)
	} else {
		log.SetFlags(log.LstdFlags | log.Lshortfile)
	}

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to load config: %v\n", err)
		os.Exit(1)
	}

	// Load known applications from registry
	registryPath := filepath.Join(cfg.Output.BasePath, "REGISTRY.md")
	apps, err := registry.LoadApplications(registryPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Warning: Could not load registry: %v\n", err)
		apps = []registry.Application{}
	}

	// Connect to IMAP
	imapCreds := imap.Credentials{
		Server:   cfg.IMAP.Server,
		Port:     cfg.IMAP.Port,
		Username: cfg.IMAP.Username,
		Password: cfg.IMAP.Password,
	}

	client, err := imap.NewClient(imapCreds)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to create IMAP client: %v\n", err)
		os.Exit(1)
	}
	defer client.Close()

	// Load state to track last checked email
	statePath := cfg.Output.StatePath
	st, err := state.Load(statePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Warning: Could not load state: %v (starting fresh)\n", err)
		st = &state.State{}
	}

	// Select folder and check UID validity
	folderInfo, err := client.SelectFolder(cfg.IMAP.Folder)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to select folder: %v\n", err)
		os.Exit(1)
	}

	// Check if state is valid for this folder
	var messages []imap.EmailMessage
	if st.IsValid(cfg.IMAP.Folder, folderInfo.UIDValidity) {
		// Incremental: fetch only new emails since last run
		messages, err = client.FetchEmailsSinceUID(st.LastUID)
	} else {
		// First run or folder changed: use date-based fallback
		messages, err = client.FetchEmailsSinceUID(0) // 0 triggers 7-day fallback
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to fetch emails: %v\n", err)
		os.Exit(1)
	}

	// Track highest UID seen
	var maxUID uint32

	var savedFiles []SavedFile
	var saved, skipped, unmatched, parseErrors int

	// Process each email
	for _, msg := range messages {
		// Track highest UID
		if uint32(msg.UID) > maxUID {
			maxUID = uint32(msg.UID)
		}

		email, err := parser.ParseEmail(bytes.NewReader(msg.Raw))
		if err != nil {
			parseErrors++
			continue
		}

		// Classify the email
		classification := classifier.Classify(email.Subject, email.Body)

		if classification.Type == classifier.Unknown {
			skipped++
			continue
		}

		// Match to application
		match := matcher.MatchApplication(
			email.From.Address,
			email.From.Name,
			email.Subject,
			email.Body,
			apps,
		)

		if match == nil || match.Confidence < 0.3 {
			unmatched++
			continue
		}

		// Save communication (unless dry-run)
		if cfg.Processing.DryRun {
			// In dry-run, simulate the path
			dryPath := filepath.Join(
				cfg.Output.BasePath,
				match.Application.Path,
				"communications",
				fmt.Sprintf("%s_%s.md", email.Date.Format("2006-01-02"), classification.Type),
			)
			savedFiles = append(savedFiles, SavedFile{
				Path:    dryPath,
				Subject: email.Subject,
			})
			saved++
		} else {
			commData := storage.CommunicationData{
				Date:     email.Date,
				From:     email.From.Name,
				FromAddr: email.From.Address,
				Subject:  email.Subject,
				Body:     email.Body,
				Type:     classification.Type,
			}

			savedPath, err := storage.SaveCommunication(cfg.Output.BasePath, match.Application.Path, commData)
			if err != nil {
				skipped++
				continue
			}
			savedFiles = append(savedFiles, SavedFile{
				Path:    savedPath,
				Subject: email.Subject,
			})
			saved++
		}
	}

	// Output: List of saved files
	if len(savedFiles) > 0 {
		fmt.Println("# Created Files")
		fmt.Println()
		for _, f := range savedFiles {
			fmt.Printf("- `%s`\n", f.Path)
			fmt.Printf("  Subject: %s\n", f.Subject)
		}
		fmt.Println()
	}

	// Stats
	fmt.Println("## Statistics")
	fmt.Println()
	fmt.Printf("- Emails processed: %d\n", len(messages))
	fmt.Printf("- Files created: %d\n", saved)
	fmt.Printf("- Skipped (unknown type): %d\n", skipped)
	fmt.Printf("- Unmatched (no application): %d\n", unmatched)
	if parseErrors > 0 {
		fmt.Printf("- Parse errors: %d\n", parseErrors)
	}
	fmt.Println()

	// Disclaimer
	fmt.Println("## Action Required")
	fmt.Println()
	fmt.Println("⚠️  **Classification is preliminary** (keyword-based heuristics).")
	fmt.Println()
	fmt.Println("Please review each file and:")
	fmt.Println("1. Verify/correct the classification type in the filename")
	fmt.Println("2. Rename files if needed (e.g., `_interview.md` → `_acknowledgment.md`)")
	fmt.Println("3. Update `REGISTRY.md` with any status changes")
	fmt.Println()

	if cfg.Processing.DryRun {
		fmt.Println("---")
		fmt.Println("🔍 **DRY-RUN mode** - no files were actually created")
	}

	// Save state for next run (unless dry-run)
	if !cfg.Processing.DryRun && maxUID > 0 {
		st.LastUID = maxUID
		st.LastFolder = cfg.IMAP.Folder
		st.UIDValidity = folderInfo.UIDValidity
		if err := st.Save(statePath); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: Could not save state: %v\n", err)
		}
	}
}
