# EdgeDB Infrastructure Setup

This directory contains the EdgeDB database schema and migration files for the CV System.

## Quick Start

1. **Start EdgeDB:**

   ```bash
   docker compose up -d edgedb
   ```

2. **Verify EdgeDB is running:**

   ```bash
   docker compose ps
   ```

3. **Connect to EdgeDB:**

   ```bash
   docker compose exec edgedb edgedb query --host localhost --port 5656 --user edgedb --tls-security=insecure "SELECT 1"
   ```

4. **Check version:**

   ```bash
   docker compose exec edgedb edgedb query --host localhost --port 5656 --user edgedb --tls-security=insecure "SELECT sys::get_version()"
   ```

## Schema Overview

The schema defines two main domains:

### Applications Domain

- **Company** - Companies you're applying to
- **Posting** - Job postings from various sources
- **Application** - Your application records (status, documents)
- **Correspondence** - Email communications (incoming/outgoing)
- **Event** - Interviews, deadlines, follow-ups

### Knowledge Base Domain

- **Experience** - Work history entries (multilingual)
- **Skill** - Technical and soft skills with evidence
- **Achievement** - Notable accomplishments
- **Tag** - Classification system for all entities

## Schema File

- `dbschema/default.esdl` - Main schema definition (EdgeDB SDL)

## Migrations

EdgeDB tracks schema changes automatically. When you modify `default.esdl`:

```bash
# Create migration
docker compose exec edgedb edgedb migration create

# Apply migration
docker compose exec edgedb edgedb migrate
```

## TypeScript Integration

EdgeDB generates TypeScript types from the schema:

```bash
# Generate query builder types (run after schema changes)
npx @edgedb/generate edgeql-js
```

This creates type-safe query builders in `dbschema/edgeql-js/`.

## Development Workflow

1. Modify `dbschema/default.esdl`
2. Create migration: `docker compose exec edgedb edgedb migration create`
3. Apply migration: `docker compose exec edgedb edgedb migrate`
4. Regenerate types: `npx @edgedb/generate edgeql-js`
5. Use types in MCP servers

## Backup & Restore

```bash
# Backup
docker compose exec edgedb edgedb dump cv_system > backup.dump

# Restore
docker compose exec -T edgedb edgedb restore cv_system < backup.dump
```

## Troubleshooting

**Cannot connect to EdgeDB:**

- Check container is running: `docker compose ps`
- Check logs: `docker compose logs edgedb`

**Schema errors:**

- Validate syntax: `docker compose exec edgedb edgedb migration create --non-interactive`

**Port already in use:**

- Change port in `docker-compose.yml` (default: 5656)

## Resources

- [EdgeDB Documentation](https://www.edgedb.com/docs)
- [EdgeDB SDL Reference](https://www.edgedb.com/docs/datamodel/index)
- [TypeScript Query Builder](https://www.edgedb.com/docs/clients/js/generation)
