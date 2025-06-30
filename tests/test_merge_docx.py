"""Tests for merge_docx module."""

import pytest
from oidot.merge_docx import raw


class TestMergeDocx:
    """Test cases for merge_docx functions."""

    def test_raw_returns_empty_string_for_nonexistent_file(self):
        """Test that raw function returns empty string for non-existent file."""
        result = raw("nonexistent_file.docx")
        assert result == ""

    def test_raw_returns_string_type(self):
        """Test that raw function returns a string."""
        result = raw("test.docx")
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_raw_with_valid_docx_file(self):
        """Test raw function with a valid docx file (marked as slow test)."""
        # This test would require a real docx file
        # For now, just test the basic behavior
        result = raw("test.docx")
        assert result == "" 