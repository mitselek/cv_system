# Go Version of Riigihanked Harvester

A simple, fast Go implementation of the procurement document harvester.

## Building

```bash
go build -o harvest harvest.go
```

## Usage

Download all documents for a procurement:

```bash
./harvest download 9559644
```

Download to a custom directory:

```bash
./harvest download 9559644 --output-dir ./my-procurements
```

## What You Get

For each procurement, the tool downloads:

- All document files (PDF, DOCX, XLSX, etc.)
- `general_info.json` - Procurement metadata
- `metadata.json` - Document listing and download info

## Learning Go Concepts

This implementation demonstrates:

1. **Structs and Methods** - `RiigihankedAPI` struct with methods
2. **HTTP Client** - Making GET requests with custom headers
3. **JSON Encoding/Decoding** - Unmarshaling API responses, marshaling output files
4. **File I/O** - Creating directories, saving files, streaming downloads
5. **Error Handling** - Go's explicit error return pattern
6. **Command-line Flags** - Using the `flag` package for CLI arguments
7. **String Formatting** - `fmt.Sprintf` and `fmt.Printf`

## Comparison with Python Version

**Similarities:**

- Same API endpoints and logic
- Same output format
- Same command structure

**Differences:**

- Single binary, no dependencies to install
- Explicit error handling (no exceptions)
- Statically typed (structs vs. dynamic dicts)
- Faster execution and startup time

## Next Steps

To learn more Go concepts, you could add:

1. **Concurrent Downloads** - Use goroutines to download multiple files simultaneously
2. **Progress Bars** - Add a progress indicator for large downloads
3. **Investigate Command** - Port the API investigation functionality
4. **Search Command** - Add procurement search when API is discovered
5. **Tests** - Write unit tests using Go's testing package
6. **Better Error Messages** - Create custom error types
