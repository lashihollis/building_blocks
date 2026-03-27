"""Clinical Quality Measure Engine - Simple & Clean
Run quality measures from YAML definitions against DuckDB.
"""

import duckdb
import yaml
import argparse
from pathlib import Path


class QualityMeasureEngine:
    """Simple quality measure calculator."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to DuckDB database."""
        self.conn = duckdb.connect(self.db_path)
        print(f"✓ Connected to: {self.db_path}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✓ Connection closed")
    
    def load_measures(self, yaml_path):
        """Load measure(s) from YAML file."""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Handle both single measure and multiple measures format
        if isinstance(data, list):
            measures = data
            print(f"✓ Loaded {len(measures)} measures")
        elif 'measures' in data:
            measures = data['measures']
            print(f"✓ Loaded {len(measures)} measures from combined file")
        else:
            measures = [data]
            print(f"✓ Loaded 1 measure")
        
        return measures
    
    def execute_sql(self, sql, name):
        """Execute SQL and return patient IDs."""
        if not sql:
            return set()
        
        print(f"  → {name}...", end=" ", flush=True)
        try:
            result = self.conn.execute(sql).fetchall()
            patients = {row[0] for row in result}
            print(f"{len(patients)} patients")
            return patients
        except Exception as e:
            print(f"\n  ✗ Error: {e}")
            raise
    
    def calculate(self, measure):
        """Calculate measure results."""
        print(f"\n{'='*50}")
        print(f"📊 {measure['measure_name']}")
        print(f"{'='*50}")
        
        # Get denominator
        denominator = self.execute_sql(measure['denominator_sql'], "Denominator")
        
        # Apply exclusions
        exclusions = set()
        if measure.get('exclusions_sql'):
            exclusions = self.execute_sql(measure['exclusions_sql'], "Exclusions")
            denominator = denominator - exclusions
            print(f"     Final denominator: {len(denominator)} patients")
        
        # Get numerator
        numerator = self.execute_sql(measure['numerator_sql'], "Numerator")
        numerator = numerator & denominator
        
        # Calculate rate
        rate = (len(numerator) / len(denominator) * 100) if denominator else 0
        
        return {
            'id': measure['measure_id'],
            'name': measure['measure_name'],
            'denominator': len(denominator),
            'numerator': len(numerator),
            'exclusions': len(exclusions),
            'rate': round(rate, 1)
        }
    
    def report(self, results):
        """Display results."""
        print(f"\n{'='*50}")
        print("📈 RESULTS")
        print(f"{'='*50}")
        print(f"Numerator:   {results['numerator']:>6,} patients")
        print(f"Denominator: {results['denominator']:>6,} patients")
        print(f"Exclusions:  {results['exclusions']:>6,} patients")
        print(f"{'-'*50}")
        print(f"Rate:        {results['rate']:>6}%")
        
        # Visual bar
        bar_len = 30
        filled = int(bar_len * results['rate'] / 100)
        bar = '█' * filled + '░' * (bar_len - filled)
        print(f"Performance: [{bar}]")
        print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(
        description='Clinical Quality Measure Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
EXAMPLES:
  # Run multiple measures from a combined file
  python execute_measure.py --measure measures/quality_measures.yaml

  # Generate fresh data and run measures
  python execute_measure.py --measure measures/quality_measures.yaml --generate-data

  # Use a different database (Change the database to your database name.)
  python execute_measure.py --measure measures/quality_measures.yaml --db my_data.duckdb
        '''
    )
    
    parser.add_argument(
        '--measure',
        required=True,
        help='Path to YAML file containing measure definition(s)'
    )
    parser.add_argument(
        '--db',
        default='clinical_data.duckdb',
        help='Database file (default: clinical_data.duckdb)'
    )
    parser.add_argument(
        '--generate-data',
        action='store_true',
        help='Generate synthetic data before running measures'
    )
    
    args = parser.parse_args()
    
    # Generate data if requested
    if args.generate_data:
        print("\n📦 GENERATING SYNTHETIC DATA")
        print("-"*50)
        from data.generate_data import generate_all_data
        generate_all_data(args.db)
    
    # Check if measure file exists
    if not Path(args.measure).exists():
        print(f"\n✗ Error: File not found: {args.measure}")
        return
    
    # Initialize engine
    engine = QualityMeasureEngine(args.db)
    
    try:
        engine.connect()
        
        # Load and run measures
        measures = engine.load_measures(args.measure)
        
        for measure in measures:
            results = engine.calculate(measure)
            engine.report(results)
        
        print(f"\n✅ Completed {len(measures)} measure(s)")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        
    finally:
        engine.close()


if __name__ == "__main__":
    main()
