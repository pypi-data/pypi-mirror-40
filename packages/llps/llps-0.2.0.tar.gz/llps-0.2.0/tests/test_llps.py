"""Test suite for kmer."""

from unittest import TestCase
from os.path import dirname, join

from llps import (
    ProjectSchema,
    InvalidLLPSException,
)


class TestLLPS(TestCase):
    """Test suite for llps."""

    def test_valid_schema(self):
        """Test that we can parse a valid spec without issue."""
        valid_spec_filename = join(dirname(__file__), 'valid_sample_spec.llps.yaml')
        ProjectSchema.from_file(valid_spec_filename)

    def test_invalid_schema(self):
        """Test that parsing an invalid spec throws an error."""
        invalid_spec_filename = join(dirname(__file__), 'invalid_sample_spec.llps.yaml')
        with self.assertRaises(InvalidLLPSException):
            ProjectSchema.from_file(invalid_spec_filename)
