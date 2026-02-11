# Code Review Agent

A specialized agent for performing comprehensive code reviews with focus on code quality, best practices, and maintainability.

## Purpose

This agent assists in reviewing code changes by analyzing:

- Code quality and style consistency
- Best practices adherence
- Potential bugs and logic errors
- Performance considerations
- Documentation completeness

## Capabilities

- **Code Analysis**: Deep analysis of code structure and logic
- **Style Checking**: Ensures consistency with project style guides
- **Bug Detection**: Identifies potential bugs and edge cases
- **Suggestion Generation**: Provides actionable improvement suggestions
- **Documentation Review**: Checks for adequate documentation

## Usage

### Basic Usage

Request a code review by providing the code changes:

```python
Please review this function:

def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total
```

### Advanced Usage

Request specific types of reviews:

```text
Please review this code focusing on:
1. Performance optimization opportunities
2. Error handling
3. Edge case coverage

[paste code here]
```

## Best Practices

1. Provide context about the codebase and requirements
2. Specify areas of concern if any
3. Include related code when reviewing changes
4. Follow up on suggestions with questions

## Limitations

- Cannot execute or test code
- May not understand domain-specific constraints without context
- Best suited for reviewing individual functions or small modules

## Related Agents

- [Security Guardian](../../devops/security-guardian/) - For security-focused reviews
- [SQL Optimizer](../../data/sql-optimizer/) - For query and data performance optimization

## Feedback

Report effectiveness and issues via GitHub Issues with the `agent-feedback` label.
