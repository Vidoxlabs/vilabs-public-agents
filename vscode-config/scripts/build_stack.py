#!/usr/bin/env python3
"""
VS Code Configuration Builder

Assembles modular VS Code configurations from stack manifests.
Merges JSON modules and substitutes variables.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_json(path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries."""
    result = base.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        elif key in result and isinstance(result[key], list) and isinstance(value, list):
            # For lists, extend rather than replace
            result[key] = result[key] + value
        else:
            result[key] = value
    return result


def substitute_variables(data: str, variables: Dict[str, str]) -> str:
    """Substitute variables in the format {{VARIABLE_NAME}}."""
    result = data
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def collect_extensions(modules: List[Path]) -> List[str]:
    """Collect extension recommendations from extension modules."""
    extensions = []
    for module_path in modules:
        data = load_json(module_path)
        if 'recommendations' in data:
            extensions.extend(data['recommendations'])
    # Remove duplicates while preserving order
    seen = set()
    unique_extensions = []
    for ext in extensions:
        if ext not in seen:
            seen.add(ext)
            unique_extensions.append(ext)
    return unique_extensions


def collect_tasks(modules: List[Path], variables: Dict[str, str]) -> Dict[str, Any]:
    """Collect and merge tasks from task modules."""
    merged_tasks = {"version": "2.0.0", "tasks": []}
    all_inputs = []
    
    for module_path in modules:
        data = load_json(module_path)
        if 'tasks' in data:
            merged_tasks['tasks'].extend(data['tasks'])
        if 'inputs' in data:
            all_inputs.extend(data['inputs'])
    
    # Remove duplicate inputs
    if all_inputs:
        seen_ids = set()
        unique_inputs = []
        for inp in all_inputs:
            if inp['id'] not in seen_ids:
                seen_ids.add(inp['id'])
                unique_inputs.append(inp)
        merged_tasks['inputs'] = unique_inputs
    
    # Substitute variables in tasks
    tasks_str = json.dumps(merged_tasks, indent=2)
    tasks_str = substitute_variables(tasks_str, variables)
    return json.loads(tasks_str)


def build_stack(manifest_path: Path, output_dir: Path, config_root: Path) -> None:
    """Build VS Code configuration from a stack manifest."""
    # Load manifest
    manifest = load_yaml(manifest_path)
    stack_name = manifest.get('name', 'Unknown Stack')
    print(f"Building stack: {stack_name}")
    
    # Get variables
    variables = manifest.get('variables', {})
    
    # Initialize merged configurations
    merged_settings = {}
    extension_modules = []
    task_modules = []
    
    # Process modules by category
    modules_config = manifest.get('modules', {})
    
    for category, module_files in modules_config.items():
        category_path = config_root / category
        
        for module_file in module_files:
            module_path = category_path / module_file
            
            if not module_path.exists():
                print(f"Warning: Module not found: {module_path}")
                continue
            
            if category == 'extensions':
                extension_modules.append(module_path)
            elif category == 'tasks':
                task_modules.append(module_path)
            else:
                # Merge into settings
                module_data = load_json(module_path)
                merged_settings = merge_dicts(merged_settings, module_data)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write settings.json
    settings_str = json.dumps(merged_settings, indent=2)
    settings_str = substitute_variables(settings_str, variables)
    settings_path = output_dir / 'settings.json'
    with open(settings_path, 'w') as f:
        f.write(settings_str)
    print(f"✓ Created {settings_path}")
    
    # Write extensions.json
    if extension_modules:
        extensions = collect_extensions(extension_modules)
        extensions_data = {"recommendations": extensions}
        extensions_path = output_dir / 'extensions.json'
        with open(extensions_path, 'w') as f:
            json.dump(extensions_data, f, indent=2)
        print(f"✓ Created {extensions_path}")
    
    # Write tasks.json
    if task_modules:
        tasks_data = collect_tasks(task_modules, variables)
        tasks_path = output_dir / 'tasks.json'
        with open(tasks_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)
        print(f"✓ Created {tasks_path}")
    
    print(f"\n✓ Stack '{stack_name}' built successfully in {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Build VS Code configuration from stack manifest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build Violet dev stack to current directory's .vscode/
  %(prog)s stacks/violet-dev.yaml

  # Build Python dev stack to a specific output directory
  %(prog)s stacks/python-dev.yaml -o /path/to/project/.vscode

  # Override variables
  %(prog)s stacks/violet-dev.yaml -v VILABS_VIOLET_PATH=/custom/path
        """
    )
    
    parser.add_argument(
        'manifest',
        type=Path,
        help='Path to stack manifest YAML file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('.vscode'),
        help='Output directory for VS Code configuration (default: .vscode)'
    )
    
    parser.add_argument(
        '-v', '--variable',
        action='append',
        help='Override variables (format: KEY=VALUE)',
        dest='variables'
    )
    
    parser.add_argument(
        '-c', '--config-root',
        type=Path,
        help='Root directory of vscode-config modules (default: auto-detect)'
    )
    
    args = parser.parse_args()
    
    # Determine config root
    if args.config_root:
        config_root = args.config_root
    else:
        # Auto-detect: assume script is in vscode-config/scripts/
        script_dir = Path(__file__).parent
        config_root = script_dir.parent
    
    if not config_root.exists():
        print(f"Error: Config root not found: {config_root}")
        sys.exit(1)
    
    # Resolve manifest path
    manifest_path = args.manifest
    if not manifest_path.is_absolute():
        # Try relative to config root's stacks directory
        manifest_path = config_root / 'stacks' / manifest_path.name
    
    if not manifest_path.exists():
        print(f"Error: Manifest not found: {manifest_path}")
        sys.exit(1)
    
    # Parse variable overrides
    variable_overrides = {}
    if args.variables:
        for var in args.variables:
            if '=' not in var:
                print(f"Error: Invalid variable format: {var}")
                print("Use: KEY=VALUE")
                sys.exit(1)
            key, value = var.split('=', 1)
            variable_overrides[key] = value
    
    # Load manifest and apply overrides
    manifest = load_yaml(manifest_path)
    if variable_overrides:
        manifest_vars = manifest.get('variables', {})
        manifest_vars.update(variable_overrides)
        manifest['variables'] = manifest_vars
        # Write back temporarily for building
        temp_manifest = manifest_path.parent / f'.{manifest_path.name}.tmp'
        with open(temp_manifest, 'w') as f:
            yaml.dump(manifest, f)
        manifest_path = temp_manifest
    
    try:
        build_stack(manifest_path, args.output, config_root)
    finally:
        # Clean up temp manifest
        if variable_overrides and temp_manifest.exists():
            temp_manifest.unlink()


if __name__ == '__main__':
    main()
