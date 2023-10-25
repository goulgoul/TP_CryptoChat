# TP chat chiffré

Antoine Goulin, 5A GPSE et MSc IoT

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

10. Sur un serveur malveillant, il est possible d'injecter du code comme du SQL ou du Javascript à l'aide d'attaques XSS (sur internet dans les formulaires) ou d'autres méthodes pour les serveurs comme celui que nous avons développé ici.

11. Pour s'affranchir d'attaques similaires, une bonne méthode consiste à changer le format du message récupéré par le client. Par exemple, dans le cas d'une attaque XSS stockée en Javascript, transformer le script `<script>alert("BONJOUR VOUS ÊTES EN TRAIN DE VOUS FAIRE PIRATER")</script>` en chaîne de caractètes qui ne seront que cités réduit le script à l'état de simple citation, le neutralisant entièrement.

## TTL

12. Dans l'utilisation, cette dernière version du GUI de chat est exactement la même que les autres.

13. Si l'on soustrait 45 au temps d'émission du message, la réception considère que le TTL du message est dépassé. Par conséquent, l'exception InvalidToken est levée.

14. Si une injection de code est une attaque lente, alors ajouter un TTL est une solution permettant de la pallier.

15. Une limite de cette solution est que si l'attaquant trouve un moyen de rendre son attaque rapide ou que la connexion entre les utilisateurs est trop lente, des situations indésirables se produisent. Dans le premier cas, l'attaque passe inaperçue tandis que dans le second, l'utilisateur perd la connexion alors que son usage était normal.
