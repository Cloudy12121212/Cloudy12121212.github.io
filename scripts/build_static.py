"""Build a GitHub Pages site; keep original photos and private files local."""
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'public'
TARGET = ROOT / 'site'
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.avif'}

def build():
    TARGET.mkdir(exist_ok=True)
    for source in SOURCE.iterdir():
        if source.name in {'photos', 'avatars'}:
            continue
        output = TARGET / source.name
        if source.is_dir():
            shutil.copytree(source, output, dirs_exist_ok=True)
        else:
            shutil.copy2(source, output)
    # Publish only the selected character, not unused portrait variants.
    avatars = TARGET / 'avatars'
    if avatars.exists():
        shutil.rmtree(avatars)
    for language in ['en', 'zh']:
        profile = json.loads((SOURCE / 'data' / f'{language}.json').read_text())
        for key in ['avatar', 'about_avatar']:
            path = profile.get(key, '')
            if path.startswith('/avatars/'):
                output = TARGET / path.lstrip('/')
                output.parent.mkdir(exist_ok=True)
                shutil.copy2(SOURCE / path.lstrip('/'), output)
    folder = SOURCE / 'photos'
    manifest = folder / 'photos.json'
    metadata = {}
    if manifest.exists():
        metadata = {p['file']: p for p in json.loads(manifest.read_text()).get('photos', [])}
    output_folder = TARGET / 'photos'
    output_folder.mkdir(exist_ok=True)
    rows = []
    names = set()
    for source in sorted(folder.iterdir() if folder.exists() else []):
        if not source.is_file() or source.is_symlink() or source.suffix.lower() not in EXTENSIONS or source.name.startswith('.'):
            continue
        name = source.stem + '.jpg'
        if name in names:
            raise ValueError('Duplicate photo stem: ' + source.stem)
        names.add(name)
        output = output_folder / name
        if not output.exists() or source.stat().st_mtime > output.stat().st_mtime:
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', '-Z', '2400', str(source), '--out', str(output)], check=True, stdout=subprocess.DEVNULL)
        info = metadata.get(source.name, {})
        rows.append({'id': source.name, 'src': './photos/' + quote(name), 'title': info.get('title', {}), 'alt': info.get('alt', {}), 'location': info.get('location', {}), 'date': info.get('date', '')})
    for stale in output_folder.iterdir():
        if stale.name not in names and stale.is_file():
            stale.unlink()
    (TARGET / 'data' / 'photos.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    (TARGET / '.nojekyll').touch()
    for name in ['admin.html', 'admin.js', 'resume.html', 'resume.js', '_headers']:
        (TARGET / name).unlink(missing_ok=True)
    assert not list(TARGET.rglob('*.pdf')), 'Private PDFs must never be published'
    total = sum(p.stat().st_size for p in TARGET.rglob('*') if p.is_file())
    print(f'Built static site: {len(rows)} photographs, {total / 1024**2:.1f} MiB')

if __name__ == '__main__':
    build()
