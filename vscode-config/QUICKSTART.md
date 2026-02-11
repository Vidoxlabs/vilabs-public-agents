# Quick Start Guide

This guide will help you get started with the VS Code configuration templates.

## Prerequisites

- Python 3.7 or later
- PyYAML: `pip install pyyaml`
- VS Code installed

## Step 1: Choose a Stack

Select a stack that matches your development needs:

- **python-dev.yaml** - General Python development
- **violet-dev.yaml** - Violet orchestrator development (Python + infrastructure tools)

## Step 2: Build the Configuration

Navigate to your project directory and run the builder script:

```bash
cd /path/to/your/project

# For Python development
python3 /path/to/vscode-config/scripts/build_stack.py \
    /path/to/vscode-config/stacks/python-dev.yaml

# For Violet development
python3 /path/to/vscode-config/scripts/build_stack.py \
    /path/to/vscode-config/stacks/violet-dev.yaml \
    -v VILABS_VIOLET_PATH=/path/to/violet/repo
```

This will create a `.vscode` directory with:
- `settings.json` - Editor and tool settings
- `extensions.json` - Recommended extensions
- `tasks.json` - Automated tasks

## Step 3: Install Recommended Extensions

1. Open your project in VS Code
2. View → Extensions (or press `Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Look for the "Workspace Recommendations" section
4. Click "Install All" to install all recommended extensions

## Step 4: Verify the Setup

Run the health check task:
1. View → Command Palette (or press `Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "vilabs: health-check"

This will verify that required tools are installed.

## Step 5: Start Developing

### For Python Projects

Available tasks:
- No additional tasks in the base stack, but settings are configured

### For Violet Projects

Available tasks (accessible via Command Palette → Tasks: Run Task):
- `Violet: Install Dev Tools` - Install development dependencies
- `Violet: Format` - Format code with Black
- `Violet: Lint` - Lint code with Ruff
- `Violet: Typecheck` - Type check with Mypy
- `Violet: Test` - Run tests with Pytest
- `Violet: Check All` - Run all checks
- `Violet: Compose Up` - Start Docker services
- `Violet: Compose Down` - Stop Docker services
- `Violet: Rebuild Images` - Rebuild Docker images
- `Violet: Deploy Dev Stack` - Deploy development stack

## Customization

### Override Variables

You can override stack variables when building:

```bash
python3 scripts/build_stack.py stacks/violet-dev.yaml \
    -v VILABS_VIOLET_PATH=/custom/path \
    -v VILABS_REMOTE_NODE=my-node-name
```

### Modify Settings

After building, you can manually edit the generated files in `.vscode/`:
- Edit `settings.json` to adjust editor behavior
- Add custom tasks to `tasks.json`
- Add or remove extensions in `extensions.json`

### Create a Custom Stack

1. Copy an existing stack manifest (e.g., `python-dev.yaml`)
2. Modify the modules list to include/exclude modules
3. Add your own custom modules in the appropriate directories
4. Build with your custom manifest

## Troubleshooting

### Builder Script Errors

**Error: "Manifest not found"**
- Check that the path to the manifest file is correct
- Use absolute paths if relative paths don't work

**Error: "Module not found"**
- Verify that all modules listed in the manifest exist
- Check for typos in module names

### Extension Installation Issues

**Extensions not showing up**
- Restart VS Code
- Check that `extensions.json` exists in `.vscode/`
- Manually search for extensions in the Extensions marketplace

### Task Execution Issues

**Tasks not appearing**
- Check that `tasks.json` exists in `.vscode/`
- Restart VS Code
- Verify the JSON syntax is valid

**Tasks failing**
- Check that required tools are installed (Make, Python, Docker, etc.)
- Verify paths in variables are correct
- Check that you're in the correct working directory

## Next Steps

- Read the full [README](README.md) for detailed documentation
- Explore the [examples](examples/) directory for devcontainer and workspace configurations
- Customize your configuration to fit your workflow
- Share your stack manifests with your team

## Getting Help

- Review module files in the directories to understand what each module does
- Check the [README](README.md) for detailed information on each module
- Examine generated files to see how modules are merged

## Tips

1. **Version Control**: Commit your `.vscode/` directory to share configurations with your team
2. **Regular Updates**: Rebuild your configuration when new modules are added or stack manifests are updated
3. **Minimal Customization**: Try to use stack manifests and avoid manual edits to make updates easier
4. **Team Consistency**: Use the same stack manifest across your team for consistent environments
