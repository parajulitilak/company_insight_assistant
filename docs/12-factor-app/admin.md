
##### `docs/12-factor-app/admin.md`
Admin processes principle.


# 12. Admin Processes

> Run admin/management tasks as one-off processes

Admin tasks, like scraping and indexing jobs, are run as one-off scripts.

## Implementation
- **Script**: `scripts/scrape_index_jobs.py` scrapes and indexes jobs.
- **Docker**: Run scripts in the same environment as the app.
- **Example**:
  > docker exec -it rag_fusemachines python scripts/scrape_index_jobs.py