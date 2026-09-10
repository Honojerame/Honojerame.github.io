"""Create a deterministic, standalone archive of the verified RTL collection."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'engineering'
OUTPUT=ROOT/'downloads/circuit-works.zip'
OUTPUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for path in sorted(SOURCE.rglob('*')):
        rel=path.relative_to(SOURCE)
        if not path.is_file() or any(part in ('build','__pycache__','obj_dir') for part in rel.parts) or path.suffix=='.vcd':
            continue
        info=zipfile.ZipInfo('circuit-works/'+rel.as_posix(),date_time=(2026,9,10,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o100644<<16
        archive.writestr(info,path.read_bytes())
with zipfile.ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    print(f'Packaged {len(archive.namelist())} files: {OUTPUT.stat().st_size:,} bytes.')
