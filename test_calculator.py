"""Run with python -m unittest -v. No GUI needed."""
import csv
import tempfile
import unittest
from pathlib import Path
from fuel_calculator import calculate, export_csv

BASE = dict(distance_km='600', speed_kmh='300', consumption_lph='80', reserve_percent='15', available_l='200')

class CalculatorTests(unittest.TestCase):
    def test_proposal_example(self):
        result = calculate(BASE)
        for key, value in dict(duration_h=2, trip_fuel_l=160, reserve_fuel_l=24, required_fuel_l=184, balance_l=16).items():
            self.assertAlmostEqual(result[key], value)
        self.assertEqual(result['status'], 'Surplus')

    def test_shortfall_and_exact(self):
        for fuel, expected, status in [('100', -84, 'Shortfall'), ('184', 0, 'Exact requirement'), ('0', -184, 'Shortfall')]:
            result = calculate(dict(BASE, available_l=fuel))
            self.assertEqual(result['balance_l'], expected)
            self.assertEqual(result['status'], status)

    def test_zero_reserve(self):
        self.assertEqual(calculate(dict(BASE, reserve_percent='0'))['required_fuel_l'], 160)

    def test_invalid_inputs(self):
        for key in BASE:
            for value in ('', 'hello', '-1', 'nan', 'inf', '-inf'):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    calculate(dict(BASE, **{key: value}))
        for key in ('distance_km', 'speed_kmh', 'consumption_lph'):
            with self.assertRaises(ValueError):
                calculate(dict(BASE, **{key: '0'}))

    def test_overflow(self):
        with self.assertRaises(ValueError):
            calculate(dict(BASE, distance_km='1e308', speed_kmh='1e-308'))

    def test_csv_snapshot(self):
        result = calculate(BASE)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'result.csv'
            export_csv(path, result)
            with path.open(encoding='utf-8-sig', newline='') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(float(rows[0]['required_fuel_l']), 184)
            self.assertEqual(float(rows[0]['available_l']), 200)
            self.assertEqual(rows[0]['status'], 'Surplus')
            self.assertIn('saved_at', rows[0])

if __name__ == '__main__':
    unittest.main()
