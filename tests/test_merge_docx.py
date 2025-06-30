"""Tests for merge_docx module."""

import pytest
import tempfile
import zipfile
import os
from pathlib import Path
from oidot.merge_docx import raw


@pytest.fixture
def sample_docx():
    """Create a sample docx file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            zip_file.writestr('word/document.xml', '<w:document><w:body><w:p><w:r><w:t>Test content</w:t></w:r></w:p></w:body></w:document>')
            zip_file.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>')
        yield tmp_file.name
        os.unlink(tmp_file.name)


@pytest.fixture
def empty_docx_file():
    """Create an empty docx file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            zip_file.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>')
        
        yield tmp_file.name
        
        # Cleanup
        os.unlink(tmp_file.name)


def test_raw_returns_string():
    """Test that raw function returns a string."""
    result = raw("nonexistent.docx")
    assert isinstance(result, str)


def test_raw_handles_nonexistent_file():
    """Test that raw function handles non-existent files."""
    result = raw("nonexistent.docx")
    assert "Error opening docx file" in result


def test_raw_extracts_files(sample_docx):
    """Test that raw function extracts files from docx."""
    result = raw(sample_docx)
    assert 'word/document.xml' in result
    assert 'Test content' in result


def test_raw_format_correct(sample_docx):
    """Test that raw function returns correct format."""
    result = raw(sample_docx)
    sections = result.split('\n\n')
    assert len(sections) > 1
    for section in sections[:-1]:
        if section.strip():
            lines = section.split('\n')
            assert len(lines) >= 2


def test_raw_handles_unicode():
    """Test that raw function handles unicode content."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            zip_file.writestr('test.xml', '<content>测试内容 🚀</content>')
        result = raw(tmp_file.name)
        assert '测试内容' in result
        os.unlink(tmp_file.name)


def test_raw_handles_invalid_file():
    """Test that raw function handles invalid files gracefully."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
        tmp_file.write(b"This is not a docx file")
        tmp_file.flush()
        
        result = raw(tmp_file.name)
        assert "Error opening docx file" in result
        
        os.unlink(tmp_file.name)


def test_raw_extracts_all_files_from_docx(sample_docx):
    """Test that raw function extracts all files from a valid docx."""
    result = raw(sample_docx)
    
    # Check that all expected files are present
    expected_files = [
        'word/document.xml',
        '[Content_Types].xml'
    ]
    
    for file_name in expected_files:
        assert file_name in result


def test_raw_format_is_correct(sample_docx):
    """Test that raw function returns content in the correct format."""
    result = raw(sample_docx)
    
    # Check format: filename\ncontent\n\n
    lines = result.split('\n')
    
    # Should have multiple sections separated by double newlines
    sections = result.split('\n\n')
    assert len(sections) > 1
    
    # Each section should start with a filename
    for section in sections[:-1]:  # Skip last empty section
        if section.strip():
            lines = section.split('\n')
            assert len(lines) >= 2  # filename + content


def test_raw_handles_empty_docx(empty_docx_file):
    """Test that raw function handles empty docx files."""
    result = raw(empty_docx_file)
    
    # Should contain the minimal file
    assert '[Content_Types].xml' in result
    assert 'Types xmlns' in result


def test_raw_handles_binary_files():
    """Test that raw function handles binary files in docx."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            # Add a binary file (simulating an image)
            zip_file.writestr('word/media/image1.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
            zip_file.writestr('word/document.xml', '<w:document><w:body></w:body></w:document>')
        
        result = raw(tmp_file.name)
        
        # Should handle binary content gracefully
        assert 'word/media/image1.png' in result
        assert 'word/document.xml' in result
        
        os.unlink(tmp_file.name)


def test_raw_handles_file_read_errors():
    """Test that raw function handles individual file read errors gracefully."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            # Add a normal file
            zip_file.writestr('word/document.xml', '<w:document><w:body></w:body></w:document>')
            # Add a file that might cause issues (empty file)
            zip_file.writestr('word/empty.xml', '')
        
        result = raw(tmp_file.name)
        
        # Should still extract the normal file
        assert 'word/document.xml' in result
        assert 'word/empty.xml' in result
        
        os.unlink(tmp_file.name)


@pytest.mark.parametrize("file_content", [
    "Simple text content",
    "<xml>Complex XML content</xml>",
    "Content with\nnewlines",
    "Content with\t\ttabs",
    ""
])
def test_raw_preserves_file_content(file_content):
    """Test that raw function preserves various file content types."""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
            zip_file.writestr('test.xml', file_content)
        
        result = raw(tmp_file.name)
        
        # Should preserve the original content
        assert file_content in result
        
        os.unlink(tmp_file.name) 