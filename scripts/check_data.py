#!/usr/bin/env python
"""
Script to check the imported data counts in the database.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import text

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage

# Create Flask application context
app = create_app(os.getenv('FLASK_ENV', 'default'))

def main():
    """Main function to check imported data counts."""
    with app.app_context():
        try:
            # Check the count of each model
            company_count = Company.query.count()
            drug_count = Drug.query.count()
            brand_count = Brand.query.count()
            
            # Use raw SQL for the association table
            brand_drug_count = db.session.execute(text("SELECT COUNT(*) FROM brand_drugs")).scalar()
            
            adult_dosage_count = AdultDosage.query.count()
            pediatric_dosage_count = PediatricDosage.query.count()
            neonatal_dosage_count = NeonatalDosage.query.count()
            
            # Print the counts
            print("=== Database Record Counts ===")
            print(f"Companies: {company_count}")
            print(f"Drugs: {drug_count}")
            print(f"Brands: {brand_count}")
            print(f"Brand-Drug Relationships: {brand_drug_count}")
            print(f"Adult Dosages: {adult_dosage_count}")
            print(f"Pediatric Dosages: {pediatric_dosage_count}")
            print(f"Neonatal Dosages: {neonatal_dosage_count}")
            print("============================")
            
            # Check if any data was imported
            if company_count == 0 and drug_count == 0 and brand_count == 0:
                print("Warning: No data has been imported into the database!")
            
        except Exception as e:
            print(f"Error checking database: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 