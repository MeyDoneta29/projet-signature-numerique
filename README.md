# Signature numerique de documents (SHA-256 + RSA)
Projet Cryptographie - Master Cybersecurite - Mondiapolis - Groupe 3 (Luce et Fatimata)

## Avec Docker
    docker compose build
    docker compose run --rm app python -m pytest

## Sans Docker (plan B)
    py -3.11 -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt
    python -m pytest