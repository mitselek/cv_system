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

func (c *Client) FetchUnreadEmails(folder string, since time.Time) ([]EmailMessage, error) {
	log.Printf("Selecting folder: %s", folder)
	
	selectData, err := c.client.Select(folder, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("failed to select folder: %w", err)
	}
	
	log.Printf("Folder status: %d messages, %d recent", selectData.NumMessages, selectData.NumRecent)

	if selectData.NumMessages == 0 {
		log.Printf("Folder is empty")
		return []EmailMessage{}, nil
	}

	// Use SEARCH to find messages since the given date
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

	var messages []EmailMessage
	
	// Create sequence set from search results
	seqSet := imap.SeqSetNum(seqNums...)
	
	// Request full body using BODY.PEEK[]
	bodySection := &imap.FetchItemBodySection{
		Specifier: imap.PartSpecifierNone,
		Peek:      true,
	}
	
	fetchOptions := &imap.FetchOptions{
		UID:         true,
		BodySection: []*imap.FetchItemBodySection{bodySection},
	}
	
	fetchCmd := c.client.Fetch(seqSet, fetchOptions)
	
	for {
		msg := fetchCmd.Next()
		if msg == nil {
			break
		}
		
		// Collect the message data into a buffer
		buf, err := msg.Collect()
		if err != nil {
			log.Printf("Warning: error collecting message: %v", err)
			continue
		}
		
		// Get the body section using FindBodySection
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
