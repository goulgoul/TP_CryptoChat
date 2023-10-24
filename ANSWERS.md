# TP chat chiffré

## Introduction

1. Ce service a une topologie client-serveur
2. Les messages suivants peuvent être lus depuis le serveur :
INFO:ChatServer:gauche send message : qsdfqsdfqsdf
INFO:ChatServer:message send to droite
3. Le contenu des messages envoyés sont écrits en clair dans les logs, le principe de confidentialité est donc violé
4. La solution la plus simple pour éviter cela est des chiffrer les messages 

## Chiffrement

5. La fonction `os.urandom()` est un bon choix pour la cryptographie car, contrairement à `os.random()`, qui requiert une graine et génère une sortie pseudo-aléatoire, elle se base sur un grand nombre de facteurs imprévisibles (comme la fréquence des frappes de clavier de l'utilisateur), sans pour autant se baser sur une source de bruit physique (tension amplifiée d'une broche analogique flottante).

6. Les primitives cryptographiques sont dangereuses car elles proviennent de modules dits "hazardous", potentiellement peu sécurisés en soi ou dont l'implémentation requiert plus de connaissances sur les outils que l'on utilise.

7. Un serveur malveillant, aussi chiffré puisse-t-il être, peut tout-de-même collecter diverses données sur les utilisateurs et leurs activités dans le but de leur proposer de la publicité ciblée. De plus, rien n'empêcherait un serveur de contenir un virus envoyé à travers les échanges entre utilisateurs, notamment au sein de fichiers comme des images (ce qui s'est déjà vu plusieurs fois sur WhatsApp notamment).

8.

## Authenticated Symetric Encryption

9. Fernet est moins risqué que les modules hazmat car son implémentation est plus sécurisée et plus simple à écrire.

10. Un serveur malveillant peut attaquer avec des messages d'arnaque, comme le font certains en nous prévenant que notre colis a un problème à la douane et qu'il faut le récupérer en payant des taxes, par exemple. Il existe force autres types d'arnaques similaires. Le phishing pourraît être un cité mais on en retrouve sur les serveurs de mails. Enfin il est possible d'injecter du code malveillant comme du SQL ou du Javascript à l'aide d'attaques XSS (sur internet dans les formulaires) ou d'autres méthodes pour les serveurs comme celui que nous avons développé ici.

11. Pour s'affranchir d'attaques similaires, une bonne méthode consiste à changer le format du message récupéré par le client. Par exemple, dans le cas d'une attaque XSS stockée en Javascript, transformer le script `<script>console.log("BONJOUR VOUS ÊTES EN TRAIN DE VOUS FAIRE PIRATER")</script>` en chaîne de caractètes qui ne seront que cités réduit le script à l'état de simple citation, le neutralisant entièrement.

## TTL
