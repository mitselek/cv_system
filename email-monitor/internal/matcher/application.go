package matcher

import (
	"strings"

	"github.com/michelek/cv_system/email-monitor/internal/registry"
)

type Match struct {
	Application *registry.Application
	Confidence  float64
	Reason      string
}

// MatchApplication tries to match an email to a known application
func MatchApplication(fromAddr, fromName, subject, body string, apps []registry.Application) *Match {
	fromDomain := extractDomain(fromAddr)
	
	var bestMatch *Match
	
	for i := range apps {
		app := &apps[i]
		score := 0.0
		reasons := []string{}
		
		// Check domain match
		companySlug := strings.ToLower(strings.ReplaceAll(app.Company, " ", ""))
		if strings.Contains(fromDomain, companySlug) {
			score += 0.4
			reasons = append(reasons, "domain match")
		}
		
		// Check company name in subject or body
		if containsCaseInsensitive(subject, app.Company) || containsCaseInsensitive(body, app.Company) {
			score += 0.3
			reasons = append(reasons, "company name in email")
		}
		
		// Check position in subject or body
		if containsCaseInsensitive(subject, app.Position) || containsCaseInsensitive(body, app.Position) {
			score += 0.3
			reasons = append(reasons, "position in email")
		}
		
		// Special case: cv.ee, cvkeskus.ee job boards
		if strings.Contains(fromDomain, "cv.ee") || strings.Contains(fromDomain, "cvkeskus") {
			// Look for company name in body
			if containsCaseInsensitive(body, app.Company) {
				score += 0.5
				reasons = append(reasons, "job board + company match")
			}
		}
		
		if score > 0 && (bestMatch == nil || score > bestMatch.Confidence) {
			bestMatch = &Match{
				Application: app,
				Confidence:  score,
				Reason:      strings.Join(reasons, ", "),
			}
		}
	}
	
	return bestMatch
}

func extractDomain(email string) string {
	parts := strings.Split(email, "@")
	if len(parts) == 2 {
		return strings.ToLower(parts[1])
	}
	return ""
}

func containsCaseInsensitive(haystack, needle string) bool {
	return strings.Contains(strings.ToLower(haystack), strings.ToLower(needle))
}
