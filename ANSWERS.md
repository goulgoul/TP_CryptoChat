# TP chat chiffré

## Introduction

1. Ce service a une topologie client-serveur
2. Les messages suivants peuvent être lus depuis le serveur :
INFO:ChatServer:gauche send message : qsdfqsdfqsdf
INFO:ChatServer:message send to droite
3. Le contenu des messages envoyés sont écrits en clair dans les logs, le principe de confidentialité est donc violé
4. La solution la plus simple pour éviter cela est des chiffrer les messages 

## Chiffrement



