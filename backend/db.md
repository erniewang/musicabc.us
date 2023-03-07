# Database

The `sheets` table was created in scrapy project.  The table creating statement is in [db.py](../crapy/musicabc/db.py).

## Create Gin index for title

To make search fast, we use Gin index on title column of sheets table.

In psql:

    create extension pg_trgm;
    create index concurrently idx_sheets_title_trigram on sheets using gin (title gin_trgm_ops);
