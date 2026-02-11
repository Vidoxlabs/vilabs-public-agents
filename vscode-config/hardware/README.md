# Hardware-Optimized Settings

This directory contains settings modules optimized for specific hardware configurations.

## m4-16gb.json

Settings optimized for lower-end hardware (e.g., M4 MacBook with 16GB RAM).

### Overrides from Base Configuration

These settings intentionally override base.json to improve performance:

- **`editor.minimap.enabled: false`** - Overrides base.json (true). Disables minimap to reduce memory usage.
- **`editor.bracketPairColorization.enabled: false`** - Overrides base.json (true). Disables bracket colorization for better performance.
- **`editor.smoothScrolling: false`** - Overrides base.json (true). Disables smooth scrolling to reduce CPU usage.
- **`workbench.editor.enablePreview: true`** - Overrides base.json (false). Enables preview mode to reduce open editor count.

### Additional Performance Settings

- Disables search-on-type and symlink following for faster searches
- Disables suggestion features that can be memory-intensive
- Extends file watcher exclusions for reduced file system monitoring

## Usage

Include this module in your stack manifest when working on hardware with limited resources:

```yaml
hardware:
  - m4-16gb.json
```

These settings will merge with and override base settings to optimize for your hardware.
