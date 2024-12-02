# [ECDSA - Introduction](https://www.root-me.org/fr/Challenges/Cryptanalyse/ECDSA-Introduction)

Ce projet consiste à utiliser l'algorithme de signature numérique à courbe elliptique (ECDSA) pour signer un message.

## Lire la clé publique

Utilisez la commande suivante pour lire la clé publique :

```bash
openssl ec -in public.pem -pubin -text -noout
```

Sortie attendue :

```
read EC key
Public-Key: (521 bit)
pub:
    04:01:bf:f9:f3:d2:fe:a7:ac:e9:87:28:1a:ba:48:
    10:6f:25:a7:37:f8:20:f0:f6:9f:28:c9:53:ba:11:
    f4:c0:2a:9c:b7:ba:1f:ca:52:8f:89:ea:64:58:21:
    ed:f2:85:b8:6f:7c:72:06:b2:81:9d:30:ce:c2:15:
    6f:f7:61:fe:eb:f7:36:00:51:f3:42:fa:07:47:5f:
    71:0c:22:f6:98:69:77:f4:9a:88:41:2a:05:61:31:
    05:f6:c2:47:22:40:5d:85:17:7b:2c:99:d5:57:34:
    98:9d:b5:3a:bc:81:05:c5:91:a3:03:8a:6d:28:6a:
    ec:e9:29:cd:6f:62:42:ae:c2:c4:3a:d1:c3
ASN1 OID: secp521r1
NIST CURVE: P-521
```

## Calculer et générer la clé privée

Pour calculer la clé privée, utilisez le script SageMath :

```bash
sage load("calculate_privkey.sage")
```

Pour générer la clé privée, utilisez le script Python :

```bash
python3 generate_privkey.py
```

## Vérifier la clé privée

Pour vérifier la clé privée, utilisez la commande suivante :

```bash
openssl ec -in private.pem -pubout -out public_generated.pem
```

Verifiez que la clé publique générée correspond à la clé publique fournie [public.pem](public.pem).

## Créer une signature

Pour créer une signature pour le message, utilisez :

```bash
openssl dgst -sha256 -sign private.pem message > signature.bin
```

## Vérifier la signature

Pour vérifier la signature, utilisez :

```bash
openssl dgst -sha256 -verify public.pem -signature signature.bin message
```

## Encoder la signature en Base64

Pour encoder la signature au format Base64, utilisez :

```bash
base64 -w 0 signature.bin > signature_b64
```

## Soumettre la signature

Pour soumettre la signature, utilisez :

```bash
nc challenge01.root-me.org 51044 < signature_b64
```

## Mot de passe

Le mot de passe est `cant_wait_for_the_next_DLC_of_this_game`.
