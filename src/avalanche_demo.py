from __future__ import annotations

from src.hashing import sha256_hex


def analyze_avalanche(text1: str, text2: str) -> None:
    """Compare les empreintes SHA-256 de deux textes et mesure l'effet avalanche."""
    hash1 = sha256_hex(text1)
    hash2 = sha256_hex(text2)

    # Nombre de caractères hexadécimaux différents (sur 64)
    diff_chars = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

    # Nombre de bits différents (sur 256) grâce au XOR (^)
    diff_bits = bin(int(hash1, 16) ^ int(hash2, 16)).count("1")
    pct_bits = (diff_bits / 256) * 100

    print("=== Démonstration de l'effet avalanche (SHA-256) ===\n")
    print(f"Texte 1 : {text1!r}")
    print(f"SHA-256 : {hash1}\n")
    print(f"Texte 2 : {text2!r}")
    print(f"SHA-256 : {hash2}\n")
    print(f"Caractères hexadécimaux différents : {diff_chars} / 64")
    print(f"Bits différents                    : {diff_bits} / 256 ({pct_bits:.1f} %)")


if __name__ == "__main__":
    # Exemple parlant pour une signature de contrat : 1 seul chiffre change
    texte_original = "Contrat de paiement : 1000 EUR"
    texte_modifie = "Contrat de paiement : 1001 EUR"
    analyze_avalanche(texte_original, texte_modifie)