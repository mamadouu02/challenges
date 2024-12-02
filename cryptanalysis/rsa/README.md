# [RSA - Factorisation](https://www.root-me.org/fr/Challenges/Cryptanalyse/RSA-Factorisation)

Ce projet implémente une attaque de factorisation sur une clé publique RSA pour récupérer le texte en clair à partir d'un texte chiffré.

## Installation

Installez les dépendances nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Placez la clé publique RSA dans le fichier `pubkey.pem`.
2. Placez le texte chiffré dans le fichier `ciphertext.txt`.
3. Exécutez le script `main.py` :

    ```bash
    python main.py
    ```

4. Le texte en clair sera généré dans le fichier `plaintext.txt`.

## Description

Le script [`main.py`](main.py) effectue les étapes suivantes :
1. Lit la clé publique RSA depuis `pubkey.pem`.
2. Extrait les paramètres `n` et `e` de la clé publique.
3. Utilise l'API de FactorDB pour factoriser `n` en ses deux facteurs premiers `p` et `q`.
4. Calcule `phi` et l'exposant privé `d`.
5. Reconstruit la clé privée RSA.
6. Déchiffre le texte chiffré depuis `ciphertext.txt` et écrit le texte en clair dans `plaintext.txt`.
