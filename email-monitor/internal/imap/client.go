package imap

import (
	"crypto/tls"
	"fmt"
	"log"
	"time"

	"github.com/emersion/go-imap/v2"
	"github.com/emersion/go-imap/v2/imapclient"
)

type Client struct {
	client *imapclient.Client
}

// Expose client for debug purposes
func (c *Client) GetClient() *imapclient.Client {
	return c.client
}

type Credentials struct {
	Server   string
	Port     int
	Username string
	Password string
}

func NewClient(creds Credentials) (*Client, error) {
	addr := fmt.Sprintf("%s:%d", creds.Server, creds.Port)
	
	log.Printf("Connecting to %s...", addr)
	
	options := &imapclient.Options{
		TLSConfig: &tls.Config{},
	}
	
	c, err := imapclient.DialTLS(addr, options)
	if err != nil {
		return nil, fmt.Errorf("failed to connect: %w", err)
	}

	log.Printf("Authenticating as %s...", creds.Username)
	
	if err := c.Login(creds.Username, creds.Password).Wait(); err != nil {
		c.Close()
		return nil, fmt.Errorf("failed to login: %w", err)
	}

	log.Printf("Successfully connected and authenticated")
	
	return &Client{client: c}, nil
}

func (c *Client) Close() error {
	if c.client != nil {
		return c.client.Logout().Wait()
	}
	return nil
}

type EmailMessage struct {
	UID       imap.UID
	MessageID string
	Raw       []byte
}

// FolderInfo contains metadata about the selected folder
type FolderInfo struct {
	UIDValidity uint32
	NumMessages uint32
}

// SelectFolder selects a folder and returns its metadata
func (c *Client) SelectFolder(folder string) (*FolderInfo, error) {
	log.Printf("Selecting folder: %s", folder)

	selectData, err := c.client.Select(folder, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("failed to select folder: %w", err)
	}

	log.Printf("Folder status: %d messages, UIDValidity: %d", selectData.NumMessages, selectData.UIDValidity)

	return &FolderInfo{
		UIDValidity: selectData.UIDValidity,
		NumMessages: selectData.NumMessages,
	}, nil
}

// FetchEmailsSinceUID fetches emails with UID greater than the given UID
func (c *Client) FetchEmailsSinceUID(lastUID uint32) ([]EmailMessage, error) {
	if lastUID == 0 {
		// First run - use fallback to last 7 days
		since := time.Now().AddDate(0, 0, -7)
		return c.FetchEmailsSince(since)
	}

	// Search for UIDs greater than lastUID
	log.Printf("Searching for messages with UID > %d...", lastUID)

	// UID search: UID lastUID+1:*
	searchCriteria := &imap.SearchCriteria{
		UID: []imap.UIDSet{
			{imap.UIDRange{Start: imap.UID(lastUID + 1), Stop: 0}}, // 0 means * (highest)
		},
	}

	searchData, err := c.client.Search(searchCriteria, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("failed to search: %w", err)
	}

	if len(searchData.AllUIDs()) == 0 {
		log.Printf("No new messages found")
		return []EmailMessage{}, nil
	}

	uids := searchData.AllUIDs()
	log.Printf("Search found %d new messages", len(uids))

	return c.fetchByUIDs(uids)
}

// FetchEmailsSince fetches emails since a given date (fallback for first run)
func (c *Client) FetchEmailsSince(since time.Time) ([]EmailMessage, error) {
	log.Printf("Searching for messages since %s...", since.Format("2006-01-02"))

	searchCriteria := &imap.SearchCriteria{
		Since: since,
	}

	searchData, err := c.client.Search(searchCriteria, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("failed to search: %w", err)
	}

	if len(searchData.AllSeqNums()) == 0 {
		log.Printf("No messages found matching search criteria")
		return []EmailMessage{}, nil
	}

	seqNums := searchData.AllSeqNums()
	log.Printf("Search found %d messages", len(seqNums))

	// Convert to UIDs first for consistent handling
	seqSet := imap.SeqSetNum(seqNums...)

	fetchOptions := &imap.FetchOptions{
		UID: true,
	}

	fetchCmd := c.client.Fetch(seqSet, fetchOptions)

	var uids []imap.UID
	for {
		msg := fetchCmd.Next()
		if msg == nil {
			break
		}
		buf, err := msg.Collect()
		if err != nil {
			continue
		}
		uids = append(uids, buf.UID)
	}
	fetchCmd.Close()

	if len(uids) == 0 {
		return []EmailMessage{}, nil
	}

	return c.fetchByUIDs(uids)
}

// fetchByUIDs fetches full message content for given UIDs
func (c *Client) fetchByUIDs(uids []imap.UID) ([]EmailMessage, error) {
	var messages []EmailMessage

	uidSet := imap.UIDSet{}
	for _, uid := range uids {
		uidSet = append(uidSet, imap.UIDRange{Start: uid, Stop: uid})
	}

	bodySection := &imap.FetchItemBodySection{
		Specifier: imap.PartSpecifierNone,
		Peek:      true,
	}

	fetchOptions := &imap.FetchOptions{
		UID:         true,
		BodySection: []*imap.FetchItemBodySection{bodySection},
	}

	fetchCmd := c.client.Fetch(uidSet, fetchOptions)

	for {
		msg := fetchCmd.Next()
		if msg == nil {
			break
		}

		buf, err := msg.Collect()
		if err != nil {
			log.Printf("Warning: error collecting message: %v", err)
			continue
		}

		bodyData := buf.FindBodySection(bodySection)
		if bodyData != nil && len(bodyData) > 0 {
			messages = append(messages, EmailMessage{
				UID: buf.UID,
				Raw: bodyData,
			})
		}
	}

	if err := fetchCmd.Close(); err != nil {
		log.Printf("Warning: error closing fetch command: %v", err)
	}

	log.Printf("Successfully fetched %d messages", len(messages))

	return messages, nil
}

// FetchUnreadEmails - DEPRECATED: use FetchEmailsSinceUID instead
func (c *Client) FetchUnreadEmails(folder string, since time.Time) ([]EmailMessage, error) {
	_, err := c.SelectFolder(folder)
	if err != nil {
		return nil, err
	}
	return c.FetchEmailsSince(since)
}
