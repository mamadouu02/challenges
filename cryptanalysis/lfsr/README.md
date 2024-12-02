# [LFSR - Clair connu](https://www.root-me.org/fr/Challenges/Cryptanalyse/LFSR-Clair-connu)

Ce projet implémente un déchiffrement basé sur un registre à décalage à rétroaction linéaire (LFSR) en utilisant l'algorithme de Berlekamp-Massey pour déterminer les coefficients du LFSR à partir d'une séquence binaire connue.

## Utilisation

Pour exécuter le programme et déchiffrer le fichier `challenge.png.encrypt`, utilisez la commande suivante :

```sh
python main.py
```

## Description

### Algorithme de Berlekamp-Massey

L'algorithme de Berlekamp-Massey est utilisé pour trouver le plus court registre à décalage à rétroaction linéaire (LFSR) qui génère une séquence binaire donnée. L'implémentation se trouve dans le fichier [`berlekamp_massey.py`](berlekamp_massey.py).

### Classe LFSR

La classe `LFSR` est utilisée pour générer les bits suivants du LFSR basé sur l'état initial et les coefficients polynomial. L'implémentation se trouve dans le fichier [`main.py`](main.py).

### Fonction principale

La fonction principale lit l'en-tête du fichier PNG chiffré, utilise l'algorithme de Berlekamp-Massey pour déterminer les coefficients du LFSR, et déchiffre le fichier en utilisant le LFSR. L'implémentation se trouve dans le fichier [`main.py`](main.py).
