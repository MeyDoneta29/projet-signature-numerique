import hashlib
import pytest

from src.hashing import compare_digests, sha256_file, sha256_hex


def test_sha256_official_vectors():
    """Vecteurs de test officiels SHA-256 (norme NIST)."""
    assert (
        sha256_hex("")
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert (
        sha256_hex("abc")
        == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    assert (
        sha256_hex("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq")
        == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
    )


def test_sha256_file_empty(tmp_path):
    """Test sur un fichier vide (0 octet)."""
    empty_file = tmp_path / "vide.txt"
    empty_file.write_bytes(b"")

    assert (
        sha256_file(empty_file)
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_sha256_file_large(tmp_path):
    """Test sur un gros fichier (~512 Ko > 64 Ko) pour tester la lecture par blocs."""
    large_file = tmp_path / "gros_fichier.bin"
    content = b"0123456789abcdef" * (32 * 1024)
    large_file.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()
    assert sha256_file(large_file) == expected


def test_sha256_file_not_found(tmp_path):
    """Vérifie qu'une erreur est levée si le fichier n'existe pas."""
    with pytest.raises(FileNotFoundError):
        sha256_file(tmp_path / "inexistant.pdf")


def test_compare_digests():
    """Test de la comparaison d'empreintes (majuscules/minuscules et différence)."""
    h1 = sha256_hex("document")
    h2 = h1.upper()
    h3 = sha256_hex("Document")

    assert compare_digests(h1, h2) is True
    assert compare_digests(h1, h3) is False