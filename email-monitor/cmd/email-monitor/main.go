package main

import (
	"bytes"
	"fmt"
	"log"
	"path/filepath"
	"time"

	"github.com/michelek/cv_system/email-monitor/config"
	"github.com/michelek/cv_system/email-monitor/internal/classifier"
	"github.com/michelek/cv_system/email-monitor/internal/imap"
	"github.com/michelek/cv_system/email-monitor/internal/matcher"
	"github.com/michelek/cv_system/email-monitor/internal/parser"
	"github.com/michelek/cv_system/email-monitor/internal/registry"
	"github.com/michelek/cv_system/email-monitor/internal/storage"
)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Load known applications from registry
	registryPath := filepath.Join(cfg.Output.BasePath, "REGISTRY.md")
	apps, err := registry.LoadApplications(registryPath)
	if err != nil {
		log.Printf("Warning: Could not load registry: %v", err)
		apps = []registry.Application{}
	}
	log.Printf("Loaded %d applications from registry", len(apps))

	// Connect to IMAP
	imapCreds := imap.Credentials{
		Server:   cfg.IMAP.Server,
		Port:     cfg.IMAP.Port,
		Username: cfg.IMAP.Username,
		Password: cfg.IMAP.Password,
	}

	client, err := imap.NewClient(imapCreds)
	if err != nil {
		log.Fatalf("Failed to create IMAP client: %v", err)
	}
	defer client.Close()

	// Fetch emails from the last N days
	since := time.Now().AddDate(0, 0, -cfg.Processing.LookbackDays)
	log.Printf("Searching for emails since %s (%d days)", since.Format("2006-01-02"), cfg.Processing.LookbackDays)

	messages, err := client.FetchUnreadEmails(cfg.IMAP.Folder, since)
	if err != nil {
		log.Fatalf("Failed to fetch emails: %v", err)
	}

	log.Printf("\n=== Processing %d email(s) ===\n", len(messages))

	var saved, skipped, unmatched int

	// Process each email
	for i, msg := range messages {
		email, err := parser.ParseEmail(bytes.NewReader(msg.Raw))
		if err != nil {
			log.Printf("Error parsing email UID %d: %v", msg.UID, err)
			skipped++
			continue
		}

		fmt.Printf("\n--- Email %d/%d (UID: %d) ---\n", i+1, len(messages), msg.UID)
		fmt.Printf("Date: %s\n", email.Date.Format("2006-01-02 15:04:05"))
		fmt.Printf("From: %s <%s>\n", email.From.Name, email.From.Address)
		fmt.Printf("Subject: %s\n", email.Subject)

		// Classify the email
		classification := classifier.Classify(email.Subject, email.Body)
		fmt.Printf("Classification: %s (confidence: %.0f%%)\n", 
			classification.Type.TitleCase(), classification.Confidence*100)

		if classification.Type == classifier.Unknown {
			fmt.Printf("⏭️  Skipping: Unknown email type\n")
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
			fmt.Printf("❓ No application match found (confidence too low)\n")
			fmt.Printf("   Body preview: %s\n", truncate(email.Body, 150))
			unmatched++
			continue
		}

		fmt.Printf("Match: %s / %s (confidence: %.0f%%, %s)\n",
			match.Application.Company,
			match.Application.Position,
			match.Confidence*100,
			match.Reason,
		)

		// Save communication (unless dry-run)
		if cfg.Processing.DryRun {
			fmt.Printf("🔍 DRY-RUN: Would save to %s/communications/%s_%s.md\n",
				match.Application.Path,
				email.Date.Format("2006-01-02"),
				classification.Type,
			)
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
				fmt.Printf("⚠️  Error saving: %v\n", err)
				skipped++
				continue
			}
			fmt.Printf("✅ Saved: %s\n", savedPath)
			saved++
		}
	}

	// Summary
	fmt.Printf("\n=== Summary ===\n")
	fmt.Printf("Total emails: %d\n", len(messages))
	fmt.Printf("Saved: %d\n", saved)
	fmt.Printf("Skipped: %d\n", skipped)
	fmt.Printf("Unmatched: %d\n", unmatched)

	if cfg.Processing.DryRun {
		fmt.Println("\n🔍 DRY-RUN mode - no files were created")
	}
}

func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen] + "..."
}
