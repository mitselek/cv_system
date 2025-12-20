<!-- markdownlint-disable MD003 MD007 MD022 MD032 -->

---
title: PÖFF Data Extraction Scripts
type: project
category: web-scraping
status: archived
repository: https://github.com/mitselek/poff-scripts
language: Python
last_updated: 2024-10
duration: 2021-08 to 2024-10
experience: ilusa-koodi-instituut-2021-2024

skills_demonstrated:
  - python
  - web-scraping
  - data-processing
visibility: public
---

<!-- markdownlint-enable MD003 MD007 MD022 MD032 -->

# PÖFF Data Extraction Scripts

**Production web scraping system for film festival data extraction - 813 lines of BeautifulSoup processing**

Comprehensive Python automation scripts for extracting and processing film festival data from the Eventival platform. This project provided critical data integration capabilities for the PÖFF (Black Nights Film Festival) web platform, handling XML/HTML parsing and data transformation.

## Project Scope

### Purpose

- **Automated data extraction** from Eventival film festival platform
- **XML/HTML parsing** for structured data retrieval
- **Data transformation** for PÖFF web platform integration
- **Festival logistics support** for one of Europe's largest film festivals

### Scale

- **813 lines** of production BeautifulSoup code in `eventivalfetch.py`
- Multiple data sources and formats
- Critical mission: Zero downtime during festival season
- Production use from 2021-2024

## Technology Stack

### Core Technologies

- **Python 3.x** - Primary language
- **BeautifulSoup** - HTML/XML parsing and scraping
- **requests** - HTTP library for data fetching
- **xmltodict** - XML-to-dict conversions
- **Pydantic** - Data validation and schema enforcement

### Data Processing

- XML document parsing
- HTML content extraction
- Data validation and transformation
- Error handling for production reliability
- Schema validation with Pydantic

## Technical Architecture

### Web Scraping Implementation

```python
# Core pattern: BeautifulSoup for XML/HTML parsing
from bs4 import BeautifulSoup
import requests
import xmltodict

# 813-line production implementation
# XML/HTML parsing
# Data extraction and transformation
# Validation and error handling
```

### Key Features

- **Robust XML parsing** - BeautifulSoup handles complex XML structures
- **HTML content extraction** - Festival program data retrieval
- **Data validation** - Pydantic schemas ensure data quality
- **Error handling** - Production-ready reliability
- **Multiple data formats** - XML, HTML, JSON transformations

## Integration

### PÖFF Web Platform Connection

- Data feed for [[projects/poff-web-platform]]
- Festival program automation
- Film catalog updates
- Schedule synchronization
- Industry professional data integration

### Production Usage

- Active use: August 2021 - October 2024
- Critical festival infrastructure component
- Automated data pipeline
- Real-time festival updates during event season

## Technical Achievements

### Production Web Scraping

- **813-line BeautifulSoup implementation** in `eventivalfetch.py`
- Complex XML/HTML parsing patterns
- Multiple data source integration
- Production reliability and error handling
- Data validation with Pydantic

### Data Pipeline

- Automated festival data extraction
- XML-to-structured data transformation
- Integration with PostgreSQL database
- Support for multi-domain festival platform

## Impact

### Festival Operations

- Automated data pipeline reduced manual data entry
- Real-time festival information updates
- Reliable data synchronization during festival season
- Support for international film festival operations

### Technical Contributions

- Production-ready web scraping architecture
- BeautifulSoup expertise in complex XML/HTML parsing
- Pydantic validation patterns
- Reusable data extraction components

## Connections

- **Parent Project:** [[projects/poff-web-platform]]
- **Experience:** [[experiences/ilusa-koodi-instituut-2021-2024]]
- **Skills:**
  - [[skills/python]] (9/10 proficiency)
  - [[skills/web-scraping]]
  - [[skills/data-processing]]

## Repository

- **URL:** https://github.com/mitselek/poff-scripts
- **Organization:** mitselek
- **Language:** Python
- **Key File:** `eventivalfetch.py` (813 lines)
- **Dependencies:** BeautifulSoup, requests, xmltodict, Pydantic
