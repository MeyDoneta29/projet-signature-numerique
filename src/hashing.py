from __future__ import annotations

import hashlib
import hmac
from pathlib import Path

# Taille des blocs de lecture : 64 Ko = 65 536 octets
CHUNK_SIZE = 64 * 1024


def sha256_file(file_path: str | Path) -> str:
    """Calcule l'empreinte SHA-256 (hexadécimale) d'un fichier par blocs de 64 Ko."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    hasher = hashlib.sha256()

    # Ouverture en mode binaire ("rb") pour fonctionner sur tout type de fichier (PDF, image, etc.)
    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def sha256_hex(data: bytes | str) -> str:
    """Calcule l'empreinte SHA-256 (hexadécimale) d'un texte ou d'octets."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def compare_digests(digest1: str, digest2: str) -> bool:
    """Compare deux empreintes SHA-256 de manière sécurisée (temps constant)."""
    return hmac.compare_digest(digest1.strip().lower(), digest2.strip().lower())