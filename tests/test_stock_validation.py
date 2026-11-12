"""Measured-file regression tests; fixtures are synthetic, not reviewed stock art."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/scripts/validate_stock_asset.py'


class StockValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('stock_validator', SCRIPT)
        cls.validator = importlib.util.module_from_spec(spec)
        # Import the packaged helper without contaminating its distributable tree.
        with patch.object(sys, 'dont_write_bytecode', True):
            spec.loader.exec_module(cls.validator)
        cls.srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def image(self, name='asset.jpg', size=(2000, 2000), **options):
        path = self.folder / name
        with Image.new('RGB', size, '#718eaa') as image:
            image.save(path, icc_profile=self.srgb, **options)
        return path

    def test_valid_jpeg_measured_but_never_submission_ready(self):
        path = self.image()
        report = self.validator.validate_asset(path)
        self.assertEqual(report['technical_validation'], 'VERIFIED')
        self.assertEqual((report['width'], report['height']), (2000, 2000))
        self.assertEqual(report['megapixels'], 4)
        self.assertEqual(report['file_size_bytes'], path.stat().st_size)
        self.assertEqual(report['color_profile']['status'], 'VERIFIED')
        self.assertEqual(report['submission_readiness'], 'PENDING_MANUAL_VERIFICATION')
        self.assertEqual(report['visual_quality'], 'NOT_INSPECTED')
        self.assertEqual(report['commercial_licensing'], 'UNVERIFIED')

    def test_scenario_c_insufficient_pixels_even_with_high_dpi(self):
        path = self.image(size=(1068, 736), dpi=(1200, 1200))
        report = self.validator.validate_asset(path)
        self.assertEqual(report['pixel_count'], 786048)
        self.assertAlmostEqual(report['megapixels'], 0.786048)
        self.assertEqual(report['technical_validation'], 'FAILED')
        self.assertEqual(report['submission_readiness'], 'NOT_READY_TECHNICAL')
        self.assertTrue(any('4–100 MP' in reason for reason in report['reasons']))

    def test_png_disguised_as_jpeg_fails_actual_format(self):
        report = self.validator.validate_asset(self.image(name='fake.jpg', format='PNG'))
        self.assertEqual(report['format'], 'PNG')
        self.assertEqual(report['technical_validation'], 'FAILED')

    def test_missing_or_broken_profile_is_not_verified(self):
        for profile in (None, b'not an ICC profile'):
            with self.subTest(profile=profile):
                path = self.folder / 'profile.jpg'
                Image.new('RGB', (2000, 2000)).save(path, icc_profile=profile)
                report = self.validator.validate_asset(path)
                self.assertEqual(report['technical_validation'], 'FAILED')
                self.assertNotEqual(report['color_profile']['status'], 'VERIFIED')

    def test_non_rgb_jpeg_is_rejected(self):
        path = self.folder / 'cmyk.jpg'
        Image.new('CMYK', (2000, 2000)).save(path, icc_profile=self.srgb)
        self.assertEqual(self.validator.validate_asset(path)['technical_validation'], 'FAILED')

    def test_file_size_limit_uses_bytes_on_disk(self):
        path = self.image()
        with path.open('ab') as output:
            output.truncate(45_000_000)
        self.assertEqual(self.validator.validate_asset(path)['technical_validation'], 'VERIFIED')
        with path.open('ab') as output:
            output.write(b'0')
        report = self.validator.validate_asset(path)
        self.assertEqual(report['file_size_bytes'], 45_000_001)
        self.assertEqual(report['technical_validation'], 'FAILED')

    def test_below_minimum_and_above_maximum_pixels_fail(self):
        small = self.image(size=(1999, 2000))
        self.assertEqual(self.validator.validate_asset(small)['technical_validation'], 'FAILED')
        # Change a real JPEG SOF header to test the upper gate without allocating
        # a 300 MB raster. Oversized headers must be rejected before full decode.
        large = self.image(name='large.jpg', size=(1, 1))
        data = bytearray(large.read_bytes())
        marker = data.index(b'\xff\xc0')
        data[marker + 5:marker + 9] = (10000).to_bytes(2, 'big') + (10001).to_bytes(2, 'big')
        large.write_bytes(data)
        report = self.validator.validate_asset(large)
        self.assertEqual(report['pixel_count'], 100_010_000)
        self.assertEqual(report['technical_validation'], 'FAILED')
        self.assertFalse(report['readable'])

    def test_srgb_name_alone_does_not_verify_color_transform(self):
        # Keep the ICC description but alter the red colorant in its real tag.
        profile = bytearray(self.srgb)
        count = int.from_bytes(profile[128:132], 'big')
        for index in range(count):
            start = 132 + index * 12
            if profile[start:start + 4] == b'rXYZ':
                offset = int.from_bytes(profile[start + 4:start + 8], 'big')
                profile[offset + 8:offset + 12] = (10000).to_bytes(4, 'big')
                break
        else:
            self.fail('sRGB fixture lacks red colorant')
        path = self.folder / 'false-srgb.jpg'
        Image.new('RGB', (2000, 2000)).save(path, icc_profile=bytes(profile))
        report = self.validator.validate_asset(path)
        self.assertEqual(report['color_profile']['status'], 'FAILED')
        self.assertEqual(report['technical_validation'], 'FAILED')

    def test_dependency_absence_fails_closed_with_json(self):
        path = self.image()
        result = subprocess.run([sys.executable, '-S', str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report['technical_validation'], 'UNVERIFIED')
        self.assertEqual(report['submission_readiness'], 'NOT_READY_TECHNICAL')
        self.assertIsNone(report['width'])

    def test_unavailable_color_management_is_unverified_not_a_crash(self):
        path = self.image()
        with patch.object(ImageCms, 'ImageCmsProfile', side_effect=ImportError('LittleCMS unavailable')):
            report = self.validator.validate_asset(path)
        self.assertEqual(report['color_profile']['status'], 'UNVERIFIED')
        self.assertEqual(report['technical_validation'], 'UNVERIFIED')
        self.assertEqual(report['submission_readiness'], 'NOT_READY_TECHNICAL')

    def test_inaccessible_ancestor_reports_failure_without_traceback(self):
        with patch.object(Path, 'is_file', side_effect=PermissionError('ancestor access denied')):
            report = self.validator.validate_asset(self.folder / 'unreadable.jpg')
        self.assertEqual(report['technical_validation'], 'FAILED')
        self.assertEqual(report['submission_readiness'], 'NOT_READY_TECHNICAL')
        self.assertIsNone(report['width'])
        self.assertTrue(any('ancestor access denied' in reason for reason in report['reasons']))

    def test_missing_directory_and_corrupt_file_fail_without_invented_dimensions(self):
        broken = self.folder / 'broken.jpg'
        broken.write_bytes(b'not an image')
        for path in (self.folder / 'missing.jpg', self.folder, broken):
            with self.subTest(path=path):
                report = self.validator.validate_asset(path)
                self.assertEqual(report['technical_validation'], 'FAILED')
                self.assertIsNone(report['width'])
                self.assertTrue(report['reasons'])

    def test_truncated_jpeg_fails_full_decode(self):
        path = self.image()
        path.write_bytes(path.read_bytes()[:-500])
        report = self.validator.validate_asset(path)
        self.assertEqual(report['technical_validation'], 'FAILED')
        self.assertFalse(report['readable'])

    def test_cli_json_and_failure_exit(self):
        for size, code in (((2000, 2000), 0), ((1068, 736), 1)):
            path = self.image(size=size)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertNotEqual(json.loads(result.stdout)['submission_readiness'], 'READY_FOR_SUBMISSION')


if __name__ == '__main__':
    unittest.main()
