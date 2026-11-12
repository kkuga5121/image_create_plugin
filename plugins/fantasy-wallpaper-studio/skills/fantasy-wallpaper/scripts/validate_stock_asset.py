"""Read-only Adobe Stock raster checks. Technical success never clears rights or quality."""

import argparse
from io import BytesIO
import json
from pathlib import Path
import sys
import warnings

MIN_PIXELS = 4_000_000
MAX_PIXELS = 100_000_000
MAX_BYTES = 45_000_000  # Conservative decimal MB, not MiB.


def _check_srgb(icc, Image, ImageCms):
    if not icc:
        return {'status': 'FAILED', 'description': None, 'reason': 'Embedded sRGB ICC profile missing.'}
    try:
        profile = ImageCms.ImageCmsProfile(BytesIO(icc))
        description = ImageCms.getProfileDescription(profile).strip()
        if profile.profile.xcolor_space.strip() != 'RGB':
            raise ValueError('ICC profile is not RGB')
        # A name alone is insufficient: compare its actual color transform with
        # standard sRGB across a small RGB grid. This is conservative evidence,
        # not an exhaustive colorimetric certification of arbitrary ICC profiles.
        colors = [(r, g, b) for r in (0, 64, 128, 192, 255)
                  for g in (0, 64, 128, 192, 255) for b in (0, 64, 128, 192, 255)]
        with Image.new('RGB', (len(colors), 1)) as sample:
            sample.putdata(colors)
            converted = ImageCms.profileToProfile(sample, profile, ImageCms.createProfile('sRGB'), outputMode='RGB')
            with converted:
                difference = max(abs(a - b) for a, b in zip(sample.tobytes(), converted.tobytes()))
        if 'srgb' not in description.casefold() or difference > 2:
            return {'status': 'FAILED', 'description': description,
                    'reason': 'Embedded profile is not recognized as sRGB; color-managed verification/conversion required.'}
        return {'status': 'VERIFIED', 'description': description,
                'method': 'Parsed RGB ICC, sRGB description, sampled transform within 2 code values.'}
    except ImportError as exc:
        return {'status': 'UNVERIFIED', 'description': None, 'reason': f'Color-management support unavailable: {exc}'}
    except (OSError, ValueError, TypeError, ImageCms.PyCMSError) as exc:
        return {'status': 'FAILED', 'description': None, 'reason': f'Invalid or unsupported ICC profile: {exc}'}


def validate_asset(path):
    """Return measured technical evidence, with explicit unknown nontechnical checks."""
    path = Path(path).absolute()
    report = {
        'file': str(path), 'exists': None, 'readable': False,
        'format': None, 'width': None, 'height': None, 'pixel_count': None,
        'megapixels': None, 'file_size_bytes': None, 'file_size_mb': None,
        'color_profile': {'status': 'UNVERIFIED', 'description': None},
        'technical_validation': 'FAILED', 'visual_quality': 'NOT_INSPECTED',
        'commercial_licensing': 'UNVERIFIED',
        'generation_status': 'UNVERIFIED', 'upscaling_status': 'UNVERIFIED',
        'submission_readiness': 'NOT_READY_TECHNICAL', 'reasons': [],
    }
    try:
        from PIL import Image, ImageCms
    except ImportError:
        report['technical_validation'] = 'UNVERIFIED'
        report['reasons'].append('Pillow with LittleCMS support is required; no file checks completed.')
        return report
    try:
        report['exists'] = path.is_file()
        if not report['exists']:
            raise ValueError('File is missing or is not a regular file.')
        report['file_size_bytes'] = path.stat().st_size
        report['file_size_mb'] = report['file_size_bytes'] / 1_000_000
        if not 0 < report['file_size_bytes'] <= MAX_BYTES:
            report['reasons'].append('File size must be greater than zero and no more than 45 MB (45,000,000 bytes).')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', Image.DecompressionBombWarning)
            with Image.open(path) as image:
                report['format'] = image.format
                report['width'], report['height'] = image.size
                report['pixel_count'] = image.width * image.height
                report['megapixels'] = report['pixel_count'] / 1_000_000
                if image.format != 'JPEG':
                    report['reasons'].append('Actual file format must be JPEG; renaming the extension does not convert it.')
                if not MIN_PIXELS <= report['pixel_count'] <= MAX_PIXELS:
                    report['reasons'].append('Actual resolution must be 4–100 MP (4,000,000–100,000,000 pixels).')
                if image.mode != 'RGB':
                    report['reasons'].append(f'Image mode must be RGB for this sRGB workflow; observed {image.mode}.')
                report['color_profile'] = _check_srgb(image.info.get('icc_profile'), Image, ImageCms)
                if report['color_profile']['status'] != 'VERIFIED':
                    report['reasons'].append(report['color_profile']['reason'])
                # Do not decode an oversized raster just to confirm an already
                # failed asset. Full decoding catches truncated JPEGs in range.
                if report['pixel_count'] <= MAX_PIXELS:
                    image.load()
                    report['readable'] = True
        if not report['reasons'] and report['readable']:
            report['technical_validation'] = 'VERIFIED'
            report['submission_readiness'] = 'PENDING_MANUAL_VERIFICATION'
            report['reasons'].append('Technical checks passed only; actual visual review, rights, releases, current policy, and metadata remain to be verified.')
        elif (report['readable'] and report['color_profile']['status'] == 'UNVERIFIED'
              and report['reasons'] == [report['color_profile']['reason']]):
            report['technical_validation'] = 'UNVERIFIED'
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        report['reasons'].append(f'File validation failed: {exc}')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    report = validate_asset(parser.parse_args().image)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['technical_validation'] == 'VERIFIED' else 1


if __name__ == '__main__':
    sys.exit(main())
