package classifier

import (
	"regexp"
	"strings"
)

type CommType string

const (
	Acknowledgment CommType = "acknowledgment"
	Rejection      CommType = "rejection"
	Interview      CommType = "interview"
	Offer          CommType = "offer"
	Inquiry        CommType = "inquiry"
	Followup       CommType = "followup"
	Unknown        CommType = "unknown"
)

type Classification struct {
	Type       CommType
	Confidence float64
}

var patterns = map[CommType][]string{
	Acknowledgment: {
		`kätte\s+saanud`, `received`, `kinnitame`, `täname\s+kandideerimise`,
		`edukalt`, `avaldus.*edastatud`, `successfully\s+submitted`,
		`application.*received`, `thank\s+you.*applying`,
	},
	Rejection: {
		`kahjuks`, `teise\s+kandidaadi`, `unfortunately`, `not\s+selected`,
		`valitud\s+kandidaat`, `selected.*another`, `proceeded\s+with`,
		`better\s+matching`, `ei\s+vasta.*nõuetele`,
	},
	Interview: {
		`intervjuu`, `interview`, `kohtumine`, `meeting`,
		`vestlus`, `kutsume.*kohtumisele`, `invite.*interview`,
		`schedule.*interview`, `kohtume`,
	},
	Offer: {
		`pakkumine`, `offer`, `salary`, `palk`,
		`tööpakkumine`, `job\s+offer`, `lepingu.*projekt`,
	},
	Inquiry: {
		`küsimus`, `question`, `lisainfo`, `additional\s+information`,
		`täpsustus`, `clarification`, `võiksime.*arutada`,
	},
	Followup: {
		`update`, `status`, `jätkuteade`, `järgmine\s+samm`,
		`next\s+steps`, `progress`, `otsustusprotsess`,
	},
}

func Classify(subject, body string) Classification {
	text := strings.ToLower(subject + " " + body)
	
	scores := make(map[CommType]int)
	
	for commType, keywords := range patterns {
		for _, pattern := range keywords {
			re := regexp.MustCompile(pattern)
			if re.MatchString(text) {
				scores[commType]++
			}
		}
	}
	
	// Find highest scoring type
	maxScore := 0
	var bestType CommType = Unknown
	
	for commType, score := range scores {
		if score > maxScore {
			maxScore = score
			bestType = commType
		}
	}
	
	if maxScore == 0 {
		return Classification{Type: Unknown, Confidence: 0.0}
	}
	
	// Calculate confidence (normalized)
	totalMatches := 0
	for _, score := range scores {
		totalMatches += score
	}
	
	confidence := float64(maxScore) / float64(totalMatches)
	if confidence > 1.0 {
		confidence = 1.0
	}
	
	// Boost confidence if we have multiple matches for the same type
	if maxScore >= 2 {
		confidence = confidence * 1.2
		if confidence > 1.0 {
			confidence = 1.0
		}
	}
	
	return Classification{
		Type:       bestType,
		Confidence: confidence,
	}
}

func (c CommType) String() string {
	return string(c)
}

func (c CommType) TitleCase() string {
	s := string(c)
	if len(s) == 0 {
		return s
	}
	return strings.ToUpper(s[:1]) + s[1:]
}
