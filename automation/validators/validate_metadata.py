#!/usr/bin/env python3
"""
Metadata Validator

Validates agent metadata files against the JSON schema
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError


def validate_metadata(metadata_file: Path, schema_file: Path) -> bool:
    """Validate a metadata file against the schema"""
    try:
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        
        validate(instance=metadata, schema=schema)
        print(f"✓ {metadata_file.name} is valid")
        return True
        
    except ValidationError as e:
        print(f"✗ {metadata_file.name} is invalid:")
        print(f"  {e.message}")
        return False
        
    except Exception as e:
        print(f"✗ Error validating {metadata_file.name}: {e}")
        return False


def main():
    repo_root = Path(__file__).parent.parent.parent
    schema_file = repo_root / 'schemas' / 'agent-metadata.schema.json'
    
    if not schema_file.exists():
        print(f"Error: Schema file not found: {schema_file}")
        sys.exit(1)
    
    metadata_files = list(repo_root.rglob("metadata.json"))
    
    print(f"Validating {len(metadata_files)} metadata files...\n")
    
    valid_count = 0
    for metadata_file in metadata_files:
        if validate_metadata(metadata_file, schema_file):
            valid_count += 1
    
    print(f"\n{valid_count}/{len(metadata_files)} metadata files are valid")
    
    if valid_count < len(metadata_files):
        sys.exit(1)


if __name__ == '__main__':
    main()
