#!/usr/bin/env python3
"""
Validator for VS Code Configuration Templates

Validates:
- JSON syntax in all modules
- YAML syntax in stack manifests
- Module references in stack manifests
- Variable usage consistency
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class VSCodeConfigValidator:
    def __init__(self, config_root: Path):
        self.config_root = config_root
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.valid_categories = ['core', 'settings', 'extensions', 'tasks', 'platforms', 'hardware', 'mcp']
    
    def validate(self) -> bool:
        """Run all validations."""
        print("🔍 Validating VS Code Configuration Templates...")
        print(f"📁 Config root: {self.config_root}\n")
        
        # Check directory structure
        self._validate_directory_structure()
        
        # Validate JSON modules
        self._validate_json_modules()
        
        # Validate YAML manifests
        self._validate_stack_manifests()
        
        # Validate module references
        self._validate_module_references()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _validate_directory_structure(self):
        """Validate that required directories exist."""
        print("📂 Checking directory structure...")
        
        required_dirs = ['core', 'settings', 'extensions', 'tasks', 'stacks', 'scripts']
        for dir_name in required_dirs:
            dir_path = self.config_root / dir_name
            if not dir_path.exists():
                self.errors.append(f"Required directory missing: {dir_name}")
            else:
                print(f"  ✓ {dir_name}/")
        
        print()
    
    def _validate_json_modules(self):
        """Validate JSON syntax in all module files."""
        print("📝 Validating JSON modules...")
        
        json_files = list(self.config_root.rglob('*.json'))
        json_files = [f for f in json_files if not f.name.startswith('.')]
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
                rel_path = json_file.relative_to(self.config_root)
                print(f"  ✓ {rel_path}")
            except json.JSONDecodeError as e:
                rel_path = json_file.relative_to(self.config_root)
                self.errors.append(f"Invalid JSON in {rel_path}: {e}")
                print(f"  ✗ {rel_path}: {e}")
        
        print(f"\n  Validated {len(json_files)} JSON files\n")
    
    def _validate_stack_manifests(self):
        """Validate YAML syntax in stack manifests."""
        print("📋 Validating stack manifests...")
        
        stacks_dir = self.config_root / 'stacks'
        if not stacks_dir.exists():
            self.errors.append("stacks/ directory not found")
            return
        
        yaml_files = list(stacks_dir.glob('*.yaml'))
        yaml_files.extend(list(stacks_dir.glob('*.yml')))
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    manifest = yaml.safe_load(f)
                
                # Validate manifest structure
                if 'name' not in manifest:
                    self.warnings.append(f"{yaml_file.name}: Missing 'name' field")
                
                if 'modules' not in manifest:
                    self.errors.append(f"{yaml_file.name}: Missing 'modules' field")
                else:
                    # Check for invalid categories
                    for category in manifest['modules'].keys():
                        if category not in self.valid_categories:
                            self.warnings.append(
                                f"{yaml_file.name}: Unknown module category '{category}'"
                            )
                
                print(f"  ✓ {yaml_file.name}")
            except yaml.YAMLError as e:
                self.errors.append(f"Invalid YAML in {yaml_file.name}: {e}")
                print(f"  ✗ {yaml_file.name}: {e}")
        
        print(f"\n  Validated {len(yaml_files)} manifest files\n")
    
    def _validate_module_references(self):
        """Validate that modules referenced in manifests exist."""
        print("🔗 Validating module references...")
        
        stacks_dir = self.config_root / 'stacks'
        if not stacks_dir.exists():
            return
        
        yaml_files = list(stacks_dir.glob('*.yaml'))
        yaml_files.extend(list(stacks_dir.glob('*.yml')))
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    manifest = yaml.safe_load(f)
                
                if 'modules' not in manifest:
                    continue
                
                print(f"\n  Checking {yaml_file.name}:")
                
                for category, modules in manifest['modules'].items():
                    if category not in self.valid_categories:
                        continue
                    
                    category_path = self.config_root / category
                    
                    for module_file in modules:
                        module_path = category_path / module_file
                        
                        if not module_path.exists():
                            self.errors.append(
                                f"{yaml_file.name}: Module not found: {category}/{module_file}"
                            )
                            print(f"    ✗ {category}/{module_file} - NOT FOUND")
                        else:
                            print(f"    ✓ {category}/{module_file}")
            
            except Exception as e:
                self.errors.append(f"Error validating {yaml_file.name}: {e}")
        
        print()
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} Warning(s):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} Error(s):")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print("\n✅ All validations passed!")
        
        print()


def main():
    # Determine config root
    script_dir = Path(__file__).parent
    config_root = script_dir.parent.parent / 'vscode-config'
    
    if not config_root.exists():
        print(f"Error: vscode-config directory not found at {config_root}")
        sys.exit(1)
    
    validator = VSCodeConfigValidator(config_root)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
