# utils/pasarImg.py
from pathlib import Path
import os
import shutil

BASE_MEDIA = Path(os.getenv("MEDIA_DIR", "data"))  # p.ej. "data" o "C:/Users/USUARIO/Diven/data"

SRC_PROD = BASE_MEDIA / "img" / "productos"
SRC_SERV = BASE_MEDIA / "img" / "servicios"

DST_PROD = Path("static") / "img" / "productos"
DST_SERV = Path("static") / "img" / "servicios"

def _sync_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    # Copia recursiva preservando estructura (solo archivos)
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)

def setup_static_from_volume() -> None:
    _sync_dir(SRC_PROD, DST_PROD)
    _sync_dir(SRC_SERV, DST_SERV)
