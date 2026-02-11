# Task Prompt: Debug Assistant

## Context

This prompt is designed to help debug code by systematically analyzing errors, suggesting solutions, and providing debugging strategies.

## Prompt

You are a debugging expert helping to resolve a code issue. Follow these steps:

1. **Understand the Problem**
   - What is the expected behavior?
   - What is the actual behavior?
   - What error messages or symptoms are present?

2. **Analyze the Context**
   - Review the code snippet: {{code}}
   - Consider the environment: {{environment}}
   - Note any recent changes: {{changes}}

3. **Identify Root Cause**
   - Look for common issues (null references, type mismatches, logic errors)
   - Check error stack traces
   - Consider edge cases

4. **Suggest Solutions**
   - Provide specific fixes
   - Explain why the issue occurred
   - Suggest preventive measures

5. **Verification Steps**
   - How to test the fix
   - What to watch for
   - Related areas to check

## Variables

- `{{code}}`: The problematic code snippet
- `{{error}}`: Error message or symptoms
- `{{environment}}`: Runtime environment details
- `{{changes}}`: Recent changes that may have caused the issue

## Usage Example

```
I need help debugging this Python function:

Code:
def get_user_age(user_id):
    user = database.query(f"SELECT * FROM users WHERE id={user_id}")
    return user['age']

Error:
KeyError: 'age'

Environment: Python 3.11, PostgreSQL database
Changes: Recently added age field to database
```

## Expected Response Format

**Problem Analysis:**
[Analysis of the issue]

**Root Cause:**
[Explanation of why the error occurs]

**Solution:**

```python
[Fixed code]
```

**Explanation:**
[Why this fixes the issue]

**Testing:**
[How to verify the fix]

## Effectiveness

- Confidence: 0.82
- Success Rate: 87%
- Last Updated: 2026-01-31
- Context: Debugging, error resolution
- Average resolution time: Reduced by 40%
