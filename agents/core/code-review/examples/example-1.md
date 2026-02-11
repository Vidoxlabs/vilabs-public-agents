# Example: Python Function Review

## Input

Review this Python function for quality, performance, and best practices:

```python
def get_user_data(user_id):
    import requests
    r = requests.get(f'https://api.example.com/users/{user_id}')
    data = r.json()
    return data
```

## Output

### Code Review Report

**File**: `user_service.py`
**Lines Changed**: 1-6

#### Issues Found

**High Priority** 🔴

- **No Type Hints**: Python 3.10+ requires type annotations for all function parameters and return values
- **Exception Handling Missing**: No handling for network errors, invalid JSON, or missing users
- **Hardcoded URL**: API endpoint should be configured via environment variables
- **Import Inside Function**: Module imports should be at the top of the file

**Medium Priority** 🟡

- **No Timeout**: HTTP request could hang indefinitely without timeout
- **Unclear Response Status**: No verification that response.status_code is 200
- **Poor Variable Name**: `r` should be `response` for clarity

**Low Priority** 🟢

- **Missing Docstring**: Function purpose and parameters should be documented

#### Suggestions for Improvement

**Improved Implementation**

```python
import os
import requests
from typing import Dict, Any
from requests.exceptions import RequestException

class UserServiceError(Exception):
    """Raised when user service operations fail."""
    pass

def get_user_data(user_id: int) -> Dict[str, Any]:
    """
    Fetch user data from the API service.

    Args:
        user_id: The unique identifier for the user

    Returns:
        Dictionary containing user data

    Raises:
        UserServiceError: If the user cannot be retrieved
    """
    api_url = os.getenv('API_BASE_URL', 'https://api.example.com')
    endpoint = f'{api_url}/users/{user_id}'

    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except RequestException as e:
        error_msg = f"Failed to fetch user {user_id}: {str(e)}"
        raise UserServiceError(error_msg) from e
    except ValueError as e:
        error_msg = f"Invalid JSON response for user {user_id}: {str(e)}"
        raise UserServiceError(error_msg) from e
```

#### Key Improvements

| Aspect            | Before       | After                    |
| ----------------- | ------------ | ------------------------ |
| Type Safety       | ❌ None      | ✅ Full type hints       |
| Error Handling    | ❌ None      | ✅ Comprehensive         |
| Configuration     | ❌ Hardcoded | ✅ Environment variables |
| Documentation     | ❌ Missing   | ✅ Docstring included    |
| Timeout           | ❌ No        | ✅ 5-second timeout      |
| Status Validation | ❌ No        | ✅ raise_for_status()    |

#### Testing Suggestions

```python
import pytest
from unittest.mock import patch, MagicMock

def test_get_user_data_success():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 123, 'name': 'John Doe'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_user_data(123)
        assert result['id'] == 123

def test_get_user_data_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError()

        with pytest.raises(UserServiceError):
            get_user_data(123)
```

#### Overall Assessment

- **Complexity**: Low ✓
- **Test Coverage**: Needs Improvement ⚠️
- **Documentation**: Needs Updates ⚠️
- **Recommendation**: **Request Changes** - Address high-priority issues before merging

## Context

This example demonstrates:

- Identifying missing type hints in Python
- Proper exception handling patterns
- Security concerns (hardcoded values)
- Code clarity and maintainability
- Testing considerations

## Effectiveness

- **Issues Identified**: ✓ 7 issues found and categorized
- **Constructive Feedback**: ✓ Specific improvements provided
- **Actionable**: ✓ Clear path to resolve issues
- **Best Practices**: ✓ Aligned with PEP 8 and Python standards

**Notes**: This review demonstrates a complete analysis cycle from problem identification through suggested solutions with test examples.
