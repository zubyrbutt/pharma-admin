# Database Scripts

This directory contains scripts for database operations.

## Import Data Script

The `import_data.py` script imports pharmaceutical data from JSON files in the `json_data` directory into the database.

### Prerequisites

Before running this script, make sure:

1. The database migrations have been created and applied:

```bash
# From the project root
flask db init      # If migrations folder doesn't exist
flask db migrate   # Create migration script based on models
flask db upgrade   # Apply migrations to the database
```

2. The JSON data files exist in the `json_data` directory.

### Running the Import Script

Run the script from the project root directory:

```bash
# Make sure the script is executable
chmod +x scripts/import_data.py

# Run the script
./scripts/import_data.py
```

The script will import data in the following order to maintain relationships:

1. Companies from `COMPANY.json`
2. Drugs from `DRUG.json`
3. Brands from `BRAND.json`
4. Brand-Drug relationships from `BRAND_DRUG.json`
5. Adult dosages from `adult.json`
6. Pediatric dosages from `Paedriatic.json`
7. Neonatal dosages from `Neonatal.json`

### Notes

- The script skips existing records based on name to avoid duplicates
- Progress is logged to the console
- Errors are logged but won't stop the import process
- Commits are performed in batches to avoid memory issues 