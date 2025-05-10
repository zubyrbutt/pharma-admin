#!/usr/bin/env python
"""
Script to import pharmaceutical data from JSON files into the database.
Run this script after creating the database tables with Flask-Migrate.
"""

import os
import sys
import json
from pathlib import Path
import logging

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path to JSON data files
JSON_DATA_DIR = Path('json_data')

# Create Flask application context
app = create_app(os.getenv('FLASK_ENV', 'default'))


def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return []


def clean_text(text):
    """Clean and validate text data."""
    if text is None:
        return "Unknown"
    
    text = str(text).strip()
    if text == "" or text.isspace() or text.lower() == "null" or text.lower() == "none":
        return "Unknown"
    
    return text


def import_companies():
    """Import company data from COMPANY.json."""
    logger.info("Importing companies...")
    file_path = JSON_DATA_DIR / 'COMPANY.json'
    companies_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for company_data in companies_data:
        try:
            # Get values with proper casing and cleaning
            name = clean_text(company_data.get('NAME') or company_data.get('name'))
            code = clean_text(company_data.get('CODE') or company_data.get('code'))
            address = clean_text(company_data.get('ADDRESS') or company_data.get('address'))
            country = clean_text(company_data.get('COUNTRY') or company_data.get('country'))
            
            # Skip the first entry if it's a placeholder
            if name == "Unknown" and company_data.get('ID', company_data.get('id')) == 0:
                logger.info("Skipping placeholder company with ID 0")
                continue
            
            # Check if company already exists
            company = Company.query.filter_by(name=name).first()
            if company:
                skipped += 1
                continue
            
            # Create new company
            company = Company(
                name=name,
                code=code,
                address=address,
                country=country
            )
            db.session.add(company)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} companies so far...")
        except Exception as e:
            logger.error(f"Error importing company {name}: {e}")
            # Roll back the session in case of error to avoid transaction issues
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing companies: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} companies, skipped {skipped} existing records.")


def import_drugs():
    """Import drug data from DRUG.json."""
    logger.info("Importing drugs...")
    file_path = JSON_DATA_DIR / 'DRUG.json'
    drugs_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for drug_data in drugs_data:
        try:
            # Get values with proper casing and cleaning
            name = clean_text(drug_data.get('NAME') or drug_data.get('name'))
            description = clean_text(drug_data.get('DESCRIPTION') or drug_data.get('description'))
            category = clean_text(drug_data.get('CATEGORY') or drug_data.get('category'))
            
            # Skip if name is missing or a placeholder
            if name == "Unknown":
                skipped += 1
                continue
            
            # Check if drug already exists
            drug = Drug.query.filter_by(name=name).first()
            if drug:
                skipped += 1
                continue
            
            # Create new drug
            drug = Drug(
                name=name,
                description=description,
                category=category
            )
            db.session.add(drug)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} drugs so far...")
        except Exception as e:
            logger.error(f"Error importing drug {name}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing drugs: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} drugs, skipped {skipped} existing records.")


def import_brands():
    """Import brand data from BRAND.json."""
    logger.info("Importing brands...")
    file_path = JSON_DATA_DIR / 'BRAND.json'
    brands_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for brand_data in brands_data:
        try:
            # Get values with proper casing and cleaning
            name = clean_text(brand_data.get('BNAME') or brand_data.get('bname'))
            brand_id = brand_data.get('BID', brand_data.get('bid'))
            company_id = brand_data.get('CID', brand_data.get('cid'))
            
            # Skip if name is missing or a placeholder
            if name == "Unknown":
                skipped += 1
                continue
            
            # Check if brand already exists
            brand = Brand.query.filter_by(name=name).first()
            if brand:
                skipped += 1
                continue
            
            # Create new brand
            brand = Brand(
                name=name,
                company_id=company_id
            )
            
            db.session.add(brand)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} brands so far...")
        except Exception as e:
            logger.error(f"Error importing brand {name}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing brands: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} brands, skipped {skipped} existing records.")


def import_brand_drug_relationships():
    """Import brand-drug relationships from BRAND_DRUG.json."""
    logger.info("Importing brand-drug relationships...")
    file_path = JSON_DATA_DIR / 'BRAND_DRUG.json'
    relationship_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for rel in relationship_data:
        try:
            # Extract the relationship IDs
            bid = rel.get('BID')
            did = rel.get('DID')
            
            if not bid or not did:
                skipped += 1
                continue
            
            # Find the brand and drug
            brand = Brand.query.get(bid)
            drug = Drug.query.get(did)
            
            if not brand or not drug:
                skipped += 1
                continue
            
            # Add drug to brand if not already associated
            if drug not in brand.drugs:
                brand.drugs.append(drug)
                count += 1
            else:
                skipped += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} brand-drug relationships so far...")
        except Exception as e:
            logger.error(f"Error importing relationship for BID:{bid} - DID:{did}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing brand-drug relationships: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} brand-drug relationships, skipped {skipped} records.")


def import_adult_dosages():
    """Import adult dosage data from adult.json."""
    logger.info("Importing adult dosages...")
    file_path = JSON_DATA_DIR / 'adult.json'
    dosages_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for dosage_data in dosages_data:
        try:
            # Get drug ID from CODE field
            drug_id = dosage_data.get('CODE')
            
            if not drug_id:
                skipped += 1
                continue
            
            # Find the drug by ID
            drug = Drug.query.get(drug_id)
            if not drug:
                skipped += 1
                continue
            
            # Get dosage information
            dosage_value = clean_text(dosage_data.get('DOSE') or dosage_data.get('dose'))
            frequency = clean_text(dosage_data.get('FREQ') or dosage_data.get('freq'))
            route = clean_text(dosage_data.get('ROUTE') or dosage_data.get('route'))
            notes = clean_text(dosage_data.get('INSTRUCTION') or dosage_data.get('instruction'))
            
            # Create new dosage record
            dosage = AdultDosage(
                drug_id=drug.id,
                dosage=dosage_value if dosage_value != "Unknown" else None,
                frequency=frequency if frequency != "Unknown" else None,
                route=route if route != "Unknown" else None,
                notes=notes if notes != "Unknown" else None
            )
            db.session.add(dosage)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} adult dosages so far...")
        except Exception as e:
            logger.error(f"Error importing adult dosage for drug ID {drug_id}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing adult dosages: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} adult dosages, skipped {skipped} records.")


def import_pediatric_dosages():
    """Import pediatric dosage data from Paedriatic.json."""
    logger.info("Importing pediatric dosages...")
    file_path = JSON_DATA_DIR / 'Paedriatic.json'
    dosages_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for dosage_data in dosages_data:
        try:
            # Get drug ID from CODE field
            drug_id = dosage_data.get('CODE')
            
            if not drug_id:
                skipped += 1
                continue
            
            # Find the drug by ID
            drug = Drug.query.get(drug_id)
            if not drug:
                skipped += 1
                continue
            
            # Get dosage information
            dosage_value = clean_text(dosage_data.get('DOSE') or dosage_data.get('dose'))
            frequency = clean_text(dosage_data.get('FREQ') or dosage_data.get('freq'))
            route = clean_text(dosage_data.get('ROUTE') or dosage_data.get('route'))
            notes = clean_text(dosage_data.get('INSTRUCTION') or dosage_data.get('instruction'))
            
            # Create new dosage record
            dosage = PediatricDosage(
                drug_id=drug.id,
                dosage=dosage_value if dosage_value != "Unknown" else None,
                frequency=frequency if frequency != "Unknown" else None,
                route=route if route != "Unknown" else None,
                notes=notes if notes != "Unknown" else None
            )
            db.session.add(dosage)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} pediatric dosages so far...")
        except Exception as e:
            logger.error(f"Error importing pediatric dosage for drug ID {drug_id}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing pediatric dosages: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} pediatric dosages, skipped {skipped} records.")


def import_neonatal_dosages():
    """Import neonatal dosage data from Neonatal.json."""
    logger.info("Importing neonatal dosages...")
    file_path = JSON_DATA_DIR / 'Neonatal.json'
    dosages_data = load_json_data(file_path)
    
    count = 0
    skipped = 0
    
    for dosage_data in dosages_data:
        try:
            # Get drug ID from CODE field
            drug_id = dosage_data.get('CODE')
            
            if not drug_id:
                skipped += 1
                continue
            
            # Find the drug by ID
            drug = Drug.query.get(drug_id)
            if not drug:
                skipped += 1
                continue
            
            # Get dosage information
            dosage_value = clean_text(dosage_data.get('DOSE') or dosage_data.get('dose'))
            frequency = clean_text(dosage_data.get('FREQ') or dosage_data.get('freq'))
            route = clean_text(dosage_data.get('ROUTE') or dosage_data.get('route'))
            notes = clean_text(dosage_data.get('INSTRUCTION') or dosage_data.get('instruction'))
            
            # Create new dosage record
            dosage = NeonatalDosage(
                drug_id=drug.id,
                dosage=dosage_value if dosage_value != "Unknown" else None,
                frequency=frequency if frequency != "Unknown" else None,
                route=route if route != "Unknown" else None,
                notes=notes if notes != "Unknown" else None
            )
            db.session.add(dosage)
            count += 1
            
            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                logger.info(f"Imported {count} neonatal dosages so far...")
        except Exception as e:
            logger.error(f"Error importing neonatal dosage for drug ID {drug_id}: {e}")
            db.session.rollback()
    
    # Final commit
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Error committing neonatal dosages: {e}")
        db.session.rollback()
    
    logger.info(f"Imported {count} neonatal dosages, skipped {skipped} records.")


def main():
    """Main function to run all import operations."""
    with app.app_context():
        try:
            logger.info("Starting data import...")
            
            # Import in the correct order to maintain relationships
            import_companies()
            import_drugs()
            import_brands()
            import_brand_drug_relationships()
            import_adult_dosages()
            import_pediatric_dosages()
            import_neonatal_dosages()
            
            logger.info("Data import completed successfully.")
        except Exception as e:
            logger.error(f"Error during data import: {e}")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 