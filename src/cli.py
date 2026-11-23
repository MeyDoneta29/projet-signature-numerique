from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.hashing import sha256_file


def build_parser() -> argparse.ArgumentParser:
    """Construit l'analyseur d'arguments en ligne de commande (argparse)."""
    parser = argparse.ArgumentParser(
        prog="sigtool",
        description="Outil de signature numérique de documents (SHA-256 + RSA-PSS).",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Commande à exécuter",
    )

    # 1. Commande : hash
    hash_parser = subparsers.add_parser(
        "hash",
        help="Calculer l'empreinte SHA-256 d'un fichier",
    )
    hash_parser.add_argument("file", help="Chemin du fichier à hacher")

    # 2. Commande : keygen
    keygen_parser = subparsers.add_parser(
        "keygen",
        help="Générer une paire de clés RSA 2048 bits (PEM)",
    )
    keygen_parser.add_argument(
        "--private",
        default="private_key.pem",
        help="Chemin de sauvegarde de la clé privée (défaut: private_key.pem)",
    )
    keygen_parser.add_argument(
        "--public",
        default="public_key.pem",
        help="Chemin de sauvegarde de la clé publique (défaut: public_key.pem)",
    )
    keygen_parser.add_argument(
        "--password",
        default=None,
        help="Mot de passe pour protéger la clé privée",
    )

    # 3. Commande : sign
    sign_parser = subparsers.add_parser(
        "sign",
        help="Signer un fichier avec une clé privée RSA",
    )
    sign_parser.add_argument("file", help="Chemin du fichier à signer")
    sign_parser.add_argument(
        "-k", "--key",
        required=True,
        help="Chemin de la clé privée (.pem)",
    )
    sign_parser.add_argument(
        "-o", "--output",
        default=None,
        help="Chemin du fichier signature .sig (défaut: <fichier>.sig)",
    )
    sign_parser.add_argument(
        "--password",
        default=None,
        help="Mot de passe de la clé privée",
    )

    # 4. Commande : verify
    verify_parser = subparsers.add_parser(
        "verify",
        help="Vérifier la signature d'un fichier avec une clé publique",
    )
    verify_parser.add_argument("file", help="Chemin du fichier original")
    verify_parser.add_argument(
        "-s", "--signature",
        default=None,
        help="Chemin du fichier signature .sig (défaut: <fichier>.sig)",
    )
    verify_parser.add_argument(
        "-k", "--key",
        required=True,
        help="Chemin de la clé publique (.pem)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée principal de la CLI. Retourne un code de sortie (0 = succès, 1 = erreur)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "hash":
            digest = sha256_file(args.file)
            print(f"SHA-256 ({args.file}) : {digest}")
            return 0

        if args.command == "keygen":
            # TODO: brancher avec src/keys.py de Luce
            print("Commande 'keygen' prête, en attente de src/keys.py.", file=sys.stderr)
            return 1

        if args.command == "sign":
            sig_path = args.output or f"{args.file}.sig"
            # TODO: brancher avec src/signer.py de Luce
            print(
                f"Commande 'sign' prête (sortie prévue: {sig_path}), en attente de src/signer.py.",
                file=sys.stderr,
            )
            return 1

        if args.command == "verify":
            sig_path = args.signature or f"{args.file}.sig"
            # TODO: brancher avec src/verifier.py de Luce
            print(
                f"Commande 'verify' prête (signature: {sig_path}), en attente de src/verifier.py.",
                file=sys.stderr,
            )
            return 1

    except FileNotFoundError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Erreur inattendue : {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())