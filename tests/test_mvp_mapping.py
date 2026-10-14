"""MVP labels must not imply a reviewed provider allocation."""
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]


class MVPMappingTests(unittest.TestCase):
    def test_kubernetes_scope_and_provisional_responsibility(self):
        data = yaml.safe_load((ROOT / 'mapping/ism-mapping.yaml').read_text())
        schema = json.loads((ROOT / 'mapping/schema/ism-mapping.schema.json').read_text())
        validator = Draft202012Validator(schema)
        validator.validate(data)
        for row in data['controls']:
            self.assertTrue(all(check['engine'] in {'kyverno', 'kubescape'} for check in row['checks']))
            self.assertEqual(row['responsibility']['source'], 'provisional')
            self.assertIn(row['responsibility']['eks'], {'customer-platform', 'customer-workload', 'shared'})
        data['controls'][0]['responsibility']['eks'] = 'certified'
        self.assertTrue(list(validator.iter_errors(data)))

    def test_public_responsibility_contract_matches_mapping_validator(self):
        schema = json.loads((ROOT / 'mapping/schema/ism-mapping.schema.json').read_text())
        contract = json.loads((ROOT / 'schemas/responsibility.v2.json').read_text())
        contract.pop('$id')
        contract.pop('$schema')
        self.assertEqual(contract, schema['$defs']['responsibility'])

    def test_collected_records_require_an_unassessed_source(self):
        schema = json.loads((ROOT / 'schemas/evidence-record.v2.json').read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual(schema['properties']['schema']['const'], 'latticework.evidence-record/v2')
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        record = {
            'schema': 'latticework.evidence-record/v2',
            'record_id': 'a' * 64,
            'ism_control': 'ISM-0041',
            'system_id': 'fixture',
            'source': {'type': 'records', 'detector': 'fixture', 'detector_version': '1'},
            'resource': {'kind': 'fixture', 'name': 'fixture', 'namespace': '', 'uri': 'https://example.test/source'},
            'result': 'collected',
            'observed_at': '2026-10-14T00:00:00Z',
            'mapping': {'file_sha256': 'b' * 64, 'git_sha': 'c' * 40, 'ism_catalogue_release': '2026.09.4'},
            'responsibility': 'customer-platform',
            'evidence_ref': 'https://example.test/evidence',
        }
        for source in ['records', 'pipeline']:
            with self.subTest(source=source):
                record['source']['type'] = source
                validator.validate(record)
        for source in ['kubernetes', 'host', 'cloud']:
            with self.subTest(source=source):
                record['source']['type'] = source
                self.assertTrue(list(validator.iter_errors(record)))


if __name__ == '__main__':
    unittest.main()
