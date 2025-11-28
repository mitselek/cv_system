package parser

import (
	"bytes"
	"encoding/base64"
	"io"
	"mime"
	"mime/multipart"
	"mime/quotedprintable"
	"net/mail"
	"regexp"
	"strings"
	"time"
)

type Email struct {
	MessageID string
	Date      time.Time
	From      mail.Address
	Subject   string
	Body      string
	RawBody   string
}

func ParseEmail(r io.Reader) (*Email, error) {
	msg, err := mail.ReadMessage(r)
	if err != nil {
		return nil, err
	}

	header := msg.Header

	// Parse From
	fromStr := header.Get("From")
	from, err := mail.ParseAddress(fromStr)
	if err != nil {
		from = &mail.Address{Address: fromStr}
	}

	// Parse Date
	dateStr := header.Get("Date")
	date, err := mail.ParseDate(dateStr)
	if err != nil {
		date = time.Now()
	}

	// Extract body based on content type
	contentType := header.Get("Content-Type")
	body, rawBody := extractBody(msg.Body, contentType)

	// Decode subject if needed
	subject := decodeHeader(header.Get("Subject"))

	return &Email{
		MessageID: header.Get("Message-ID"),
		Date:      date,
		From:      *from,
		Subject:   subject,
		Body:      cleanBody(body),
		RawBody:   rawBody,
	}, nil
}

func extractBody(r io.Reader, contentType string) (string, string) {
	bodyBytes, err := io.ReadAll(r)
	if err != nil {
		return "", ""
	}
	rawBody := string(bodyBytes)

	mediaType, params, err := mime.ParseMediaType(contentType)
	if err != nil {
		// No valid content type, treat as plain text
		return rawBody, rawBody
	}

	// Handle multipart messages
	if strings.HasPrefix(mediaType, "multipart/") {
		boundary := params["boundary"]
		if boundary == "" {
			return rawBody, rawBody
		}

		mr := multipart.NewReader(bytes.NewReader(bodyBytes), boundary)
		var textBody, htmlBody string

		for {
			part, err := mr.NextPart()
			if err != nil {
				break
			}

			partContentType := part.Header.Get("Content-Type")
			partMediaType, _, _ := mime.ParseMediaType(partContentType)
			
			partBody, _ := io.ReadAll(part)
			decoded := decodeContent(partBody, part.Header.Get("Content-Transfer-Encoding"))

			if strings.HasPrefix(partMediaType, "text/plain") {
				textBody = decoded
			} else if strings.HasPrefix(partMediaType, "text/html") {
				htmlBody = decoded
			} else if strings.HasPrefix(partMediaType, "multipart/") {
				// Nested multipart, recurse
				nested, _ := extractBody(bytes.NewReader(partBody), partContentType)
				if nested != "" {
					textBody = nested
				}
			}
		}

		// Prefer plain text over HTML
		if textBody != "" {
			return textBody, rawBody
		}
		if htmlBody != "" {
			return stripHTML(htmlBody), rawBody
		}
	}

	// Single part message
	decoded := decodeContent(bodyBytes, "")
	if strings.HasPrefix(mediaType, "text/html") {
		return stripHTML(decoded), rawBody
	}

	return decoded, rawBody
}

func decodeContent(data []byte, encoding string) string {
	encoding = strings.ToLower(encoding)
	
	switch encoding {
	case "base64":
		decoded, err := base64.StdEncoding.DecodeString(string(data))
		if err != nil {
			return string(data)
		}
		return string(decoded)
	case "quoted-printable":
		reader := quotedprintable.NewReader(bytes.NewReader(data))
		decoded, err := io.ReadAll(reader)
		if err != nil {
			return string(data)
		}
		return string(decoded)
	default:
		return string(data)
	}
}

func decodeHeader(s string) string {
	dec := new(mime.WordDecoder)
	decoded, err := dec.DecodeHeader(s)
	if err != nil {
		return s
	}
	return decoded
}

func stripHTML(html string) string {
	// Remove script tags with content
	reScript := regexp.MustCompile(`(?is)<script[^>]*>.*?</script>`)
	html = reScript.ReplaceAllString(html, "")
	
	// Remove style tags with content
	reStyle := regexp.MustCompile(`(?is)<style[^>]*>.*?</style>`)
	html = reStyle.ReplaceAllString(html, "")

	// Remove all HTML tags
	re := regexp.MustCompile(`<[^>]+>`)
	text := re.ReplaceAllString(html, " ")

	// Decode HTML entities
	text = strings.ReplaceAll(text, "&nbsp;", " ")
	text = strings.ReplaceAll(text, "&amp;", "&")
	text = strings.ReplaceAll(text, "&lt;", "<")
	text = strings.ReplaceAll(text, "&gt;", ">")
	text = strings.ReplaceAll(text, "&quot;", "\"")
	text = strings.ReplaceAll(text, "&#39;", "'")

	return text
}

func cleanBody(raw string) string {
	// Normalize line endings
	raw = strings.ReplaceAll(raw, "\r\n", "\n")
	raw = strings.ReplaceAll(raw, "\r", "\n")

	// Split into lines and clean
	lines := strings.Split(raw, "\n")
	var cleaned []string
	emptyCount := 0

	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		
		if trimmed == "" {
			emptyCount++
			if emptyCount <= 2 {
				cleaned = append(cleaned, "")
			}
		} else {
			emptyCount = 0
			cleaned = append(cleaned, trimmed)
		}
	}

	result := strings.Join(cleaned, "\n")
	result = strings.TrimSpace(result)
	
	return result
}
