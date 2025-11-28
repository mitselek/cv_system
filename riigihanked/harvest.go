package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const (
	baseURL  = "https://riigihanked.riik.ee"
	apiBase  = baseURL + "/rhr/api/public/v1"
	fileBase = baseURL + "/filetransfer/client/shared/file"
)

type RiigihankedAPI struct {
	client *http.Client
}

func NewRiigihankedAPI() *RiigihankedAPI {
	return &RiigihankedAPI{
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func (api *RiigihankedAPI) doRequest(url string) (*http.Response, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
	req.Header.Set("Accept", "application/json")

	return api.client.Do(req)
}

func (api *RiigihankedAPI) getLatestVersion(procurementID string) (int, error) {
	url := fmt.Sprintf("%s/procurement/%s/latest-version", apiBase, procurementID)
	resp, err := api.doRequest(url)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var result struct {
		Value int `json:"value"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return 0, err
	}

	return result.Value, nil
}

func (api *RiigihankedAPI) getGeneralInfo(procVersID int) (map[string]interface{}, error) {
	url := fmt.Sprintf("%s/proc-vers/%d/general-info", apiBase, procVersID)
	resp, err := api.doRequest(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result, nil
}

type Document struct {
	ProcurementDocumentOldID int    `json:"procurementDocumentOldId"`
	FileName                 string `json:"fileName"`
}

func (api *RiigihankedAPI) getDocumentsList(procVersID int) ([]Document, error) {
	url := fmt.Sprintf("%s/proc-vers/%d/documents/general-info", apiBase, procVersID)
	resp, err := api.doRequest(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var result struct {
		ProcurementDocuments []Document `json:"procurementDocuments"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result.ProcurementDocuments, nil
}

func (api *RiigihankedAPI) getTempDownloadURL(procVersID, docOldID int) (string, error) {
	url := fmt.Sprintf("%s/proc-vers/%d/documents/%d/temp-url", apiBase, procVersID, docOldID)
	resp, err := api.doRequest(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var result struct {
		Value string `json:"value"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}

	return baseURL + result.Value, nil
}

func (api *RiigihankedAPI) downloadFile(url, outputPath string) error {
	resp, err := api.doRequest(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	out, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

type DownloadResult struct {
	ProcurementID  string `json:"procurement_id"`
	VersionID      int    `json:"version_id"`
	TotalDocuments int    `json:"total_documents"`
	Downloaded     int    `json:"downloaded"`
	OutputDir      string `json:"output_dir"`
	DownloadedAt   string `json:"downloaded_at"`
}

func (api *RiigihankedAPI) downloadDocuments(procurementID, outputDir string) (*DownloadResult, error) {
	fmt.Printf("🔍 Fetching documents for procurement %s...\n", procurementID)

	versionID, err := api.getLatestVersion(procurementID)
	if err != nil {
		return nil, fmt.Errorf("failed to get latest version: %w", err)
	}
	fmt.Printf("📌 Latest version: %d\n", versionID)

	fmt.Println("📋 Fetching general information...")
	generalInfo, err := api.getGeneralInfo(versionID)
	if err != nil {
		return nil, fmt.Errorf("failed to get general info: %w", err)
	}

	documents, err := api.getDocumentsList(versionID)
	if err != nil {
		return nil, fmt.Errorf("failed to get documents list: %w", err)
	}
	fmt.Printf("📄 Found %d documents\n", len(documents))

	if outputDir == "" {
		outputDir = filepath.Join("procurements", procurementID)
	}

	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create output directory: %w", err)
	}

	generalInfoPath := filepath.Join(outputDir, "general_info.json")
	if err := saveJSON(generalInfoPath, generalInfo); err != nil {
		return nil, fmt.Errorf("failed to save general info: %w", err)
	}
	fmt.Printf("💾 Saved general info to %s\n", generalInfoPath)

	metadata := map[string]interface{}{
		"procurement_id": procurementID,
		"version_id":     versionID,
		"downloaded_at":  time.Now().Format(time.RFC3339),
		"documents":      documents,
	}
	metadataPath := filepath.Join(outputDir, "metadata.json")
	if err := saveJSON(metadataPath, metadata); err != nil {
		return nil, fmt.Errorf("failed to save metadata: %w", err)
	}
	fmt.Printf("💾 Saved metadata to %s\n", metadataPath)

	downloaded := 0
	for _, doc := range documents {
		filename := doc.FileName
		filepath := filepath.Join(outputDir, filename)

		fmt.Printf("⬇️  Downloading: %s... ", filename)

		tempURL, err := api.getTempDownloadURL(versionID, doc.ProcurementDocumentOldID)
		if err != nil {
			fmt.Printf("❌ Failed to get temp URL: %v\n", err)
			continue
		}

		if err := api.downloadFile(tempURL, filepath); err != nil {
			fmt.Printf("❌ Failed: %v\n", err)
			continue
		}

		fileInfo, _ := os.Stat(filepath)
		fmt.Printf("✅ (%d bytes)\n", fileInfo.Size())
		downloaded++
	}

	fmt.Printf("\n✨ Downloaded %d/%d documents to %s\n", downloaded, len(documents), outputDir)

	return &DownloadResult{
		ProcurementID:  procurementID,
		VersionID:      versionID,
		TotalDocuments: len(documents),
		Downloaded:     downloaded,
		OutputDir:      outputDir,
		DownloadedAt:   time.Now().Format(time.RFC3339),
	}, nil
}

func saveJSON(path string, data interface{}) error {
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(data)
}

func main() {
	downloadCmd := flag.NewFlagSet("download", flag.ExitOnError)
	downloadOutputDir := downloadCmd.String("output-dir", "", "Directory to save documents")

	if len(os.Args) < 2 {
		fmt.Println("Riigihanked Document Harvester")
		fmt.Println("\nUsage:")
		fmt.Println("  harvest download <procurement_id> [--output-dir <dir>]")
		fmt.Println("\nExamples:")
		fmt.Println("  harvest download 9559644")
		fmt.Println("  harvest download 9559644 --output-dir ./my-procurements")
		os.Exit(1)
	}

	api := NewRiigihankedAPI()

	switch os.Args[1] {
	case "download":
		downloadCmd.Parse(os.Args[2:])
		if downloadCmd.NArg() < 1 {
			fmt.Println("Error: procurement_id required")
			downloadCmd.Usage()
			os.Exit(1)
		}

		procurementID := downloadCmd.Arg(0)
		result, err := api.downloadDocuments(procurementID, *downloadOutputDir)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

		if result.Downloaded > 0 {
			fmt.Printf("\n✅ Success! Downloaded %d/%d documents\n", result.Downloaded, result.TotalDocuments)
		} else {
			fmt.Println("\n❌ No files downloaded")
			os.Exit(1)
		}

	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		fmt.Println("Available commands: download")
		os.Exit(1)
	}
}
