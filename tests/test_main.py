"""Tests for main module."""

import pytest
from unittest.mock import patch
from oidot.main import main


class TestMain:
    """Test cases for main function."""

    @patch('builtins.print')
    def test_main_prints_hello_message(self, mock_print):
        """Test that main function prints the expected message."""
        main()
        mock_print.assert_called_once_with("Hello from oidot!")

    def test_main_returns_none(self):
        """Test that main function returns None."""
        result = main()
        assert result is None 