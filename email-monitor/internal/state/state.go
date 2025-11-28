package state

import (
	"encoding/json"
	"os"
	"time"
)

// State tracks the email-monitor's progress
type State struct {
	LastUID     uint32    `json:"last_uid"`
	LastRun     time.Time `json:"last_run"`
	LastFolder  string    `json:"last_folder"`
	UIDValidity uint32    `json:"uid_validity"` // IMAP folder validity - if changed, UIDs are invalid
}

// Load reads state from file, returns empty state if file doesn't exist
func Load(path string) (*State, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			// No state file - return empty state (first run)
			return &State{}, nil
		}
		return nil, err
	}

	var s State
	if err := json.Unmarshal(data, &s); err != nil {
		return nil, err
	}

	return &s, nil
}

// Save writes state to file
func (s *State) Save(path string) error {
	s.LastRun = time.Now()

	data, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(path, data, 0644)
}

// IsValid checks if the state is valid for the given folder and UID validity
func (s *State) IsValid(folder string, uidValidity uint32) bool {
	// Empty state (first run)
	if s.LastUID == 0 {
		return false
	}

	// Different folder
	if s.LastFolder != folder {
		return false
	}

	// UID validity changed - folder was recreated, UIDs are meaningless
	if s.UIDValidity != uidValidity {
		return false
	}

	return true
}
