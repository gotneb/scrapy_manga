import pytest
from errors.api_error import ApiError
from ..throw_api_error import _throw_api_error


def test_throw_api_error(results: any):
    with pytest.raises(ApiError, "API error"):
        _throw_api_error(results={"error": "API error"})
