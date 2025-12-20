---
id: data-processing
skill_name:
  et: Andmetöötlus
  en: Data Processing
category: Data Engineering
proficiency_level: Advanced
tags: [python, pandas, etl, data-transformation]
status: verified
last_verified: '2025-12-20'
evidence:
  - vabamu-museum-migration
  - poff-scripts
  - job-monitoring-system
---

# Data Processing

**Advanced data manipulation and ETL operations using Python, Pandas, and modern data engineering tools**

Comprehensive experience in large-scale data processing, transformation, and validation using Python's data science ecosystem. Proven ability to handle complex ETL pipelines, CSV operations, and data quality assurance across diverse domains.

## Core Technologies

### Primary Libraries

- **Pandas 2.0+** - DataFrame operations and data manipulation
- **Python 3.x** - Primary language
- **Pydantic** - Data validation and schema enforcement
- **CSV/Excel** - Structured data I/O
- **pytest** - Testing and validation

### Data Operations

- DataFrame transformations
- CSV reading and writing
- Row-by-row processing
- Data type conversions
- Quality checks and validation
- Schema transformations

## Production Projects

### Vabamu Museum Data Migration

**[[projects/vabamu-museum-migration]]** - Large-scale historical data processing

- **108,867 museum records** processed with Pandas
- **38 CSV files** in ETL pipeline
- **Pandas 2.0+** DataFrame operations
- Production-ready data migration architecture
- Comprehensive testing (96-test pytest suite)
- Data quality assurance throughout pipeline

**Key Operations:**

```python
# Production Pandas patterns from project
df = pd.read_csv(csv_path, nrows=limit)
for index, row in df.iterrows():
    record = row.to_dict()
    # Transform and validate
```

### PÖFF Data Processing

**[[projects/poff-scripts]]** - Festival data transformation

- XML/HTML to structured data conversion
- Multiple data format handling
- Schema validation with Pydantic
- Production reliability requirements
- Data integration for web platform

### Job Monitoring Data Pipeline

**[[projects/job-monitoring-system]]** - Multi-source data aggregation

- Job posting data extraction
- Cross-platform standardization
- Deduplication logic
- Data validation and scoring
- State management

## Technical Capabilities

### Pandas Expertise

- **DataFrame operations** - Complex data manipulations
- **CSV I/O** - `pd.read_csv()`, `df.to_csv()`
- **Iterative processing** - `df.iterrows()`, `df.itertuples()`
- **Data transformations** - `to_dict()`, type conversions
- **Filtering and selection** - Boolean indexing
- **Aggregations** - Group-by operations

### ETL Patterns

- **Extract** - CSV files, web scraping, API data
- **Transform** - Schema mapping, validation, normalization
- **Load** - Database insertion, file output
- **Validation** - Pydantic schemas, data quality checks
- **Error handling** - Graceful failures, logging

## Real-World Applications

### Museum Data Migration

- Historical record standardization
- Legacy format transformation
- Quality assurance validation
- Schema migration across systems
- Documentation for maintainability

### Festival Operations

- XML/HTML data extraction
- Film catalog processing
- Schedule data transformation
- Industry data integration
- Real-time updates

### Career Intelligence

- Job posting normalization
- Multi-source aggregation
- Duplicate detection
- Scoring and ranking
- Continuous monitoring

## Scale & Complexity

### Data Volume

- **108,867 records** - Vabamu museum migration
- **38 CSV files** - Complex ETL pipeline
- **Multiple platforms** - Cross-source integration
- **Production deployment** - Years of reliable operation

### Technical Challenges

- Large-scale CSV processing
- Historical data quality issues
- Multiple data format conversions
- Schema validation across sources
- Production reliability requirements

## Best Practices

### Code Quality

- Type hints throughout
- Comprehensive testing (pytest)
- Documentation and comments
- Modular design patterns
- Error handling

### Data Quality

- Pydantic validation schemas
- Data type enforcement
- Quality check pipelines
- Error logging and tracking
- Test coverage

### Performance

- Efficient DataFrame operations
- Memory-conscious processing
- Batch operations where applicable
- Row-limit controls for testing
- Production optimization

## Proficiency Evidence

### Production Scale

- 108,867 records processed successfully
- Multi-year production deployments
- Critical mission systems (festival, museum)
- Comprehensive test coverage (96 tests)
- Clear documentation

### Technical Depth

- Pandas 2.0+ advanced features
- Complex DataFrame transformations
- ETL pipeline architecture
- Data validation patterns
- Schema design and enforcement

## Connections

- **Projects:**
  - [[projects/vabamu-museum-migration]] (108,867 records, Pandas 2.0+)
  - [[projects/poff-scripts]] (XML/HTML transformation)
  - [[projects/job-monitoring-system]] (Multi-source aggregation)
- **Related Skills:**
  - [[skills/python]] (9/10 proficiency)
  - [[skills/web-scraping]] (Data extraction)
  - [[skills/database-management]] (Data storage)
- **Experience:**
  - [[experiences/ilusa-koodi-instituut-2021-2024]] (Production data pipelines)
