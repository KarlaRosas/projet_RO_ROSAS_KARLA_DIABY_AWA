# M1 MIAGE RO - Sujet projet

*Concepteurs : Rumen Andonov, Victor Epain, Arthur Gontier*

## Problématique

*On appelle route un chemin pour aller d'un point A à un point B. La route A vers B est différente de la route B vers A.*

Une entreprise de transport de matériel informatique dispose de dépôts de stockage et souhaitent fournir ses clients qui sont des *datacenters* en GPU dernier cri. Pour cela, elle dispose d'un seul camion partant d'un dépôt pour aller fournir les clients, en allant s'approvisioner en cours de chemin dans les autres dépôts si besoin est. Le camion reviens ensuite au dépôt de départ.

L'entreprise souhaiterait minimiser le coût total du transport, sachant que le coût de traversée $c_r$ d'une route $r$ est de $c_r = \alpha_r + \beta_r \times q_r$, avec $\alpha_r, \beta_r$ des constantes réelles positives, associées respectivement au coût de l'essence et à la taxe douanière, et $q_r$ la quantité de GPU dans le camion lors de la traversée.

Aussi, chaque client servi doit l'être dans la totalité de sa demande, et payent 1 000 euros chaque GPU vendu.

Le camion emprunte un réseau routier particulier : en effet, une fois la route traversée, le camion ne pourra plus passer dessus. De plus, chaque route $r$ a une limite $cap_r$ sur le nombre de GPU transportés. Egalement, le camion possède une limite $p$ de matériel à son bord.

Toutefois, à cause de la crise économique, l'entreprise peut décider de ne plus utiliser un ou plusieurs dépôt(s) - sans savoir le(s)quel(s), et / ou ne plus servir un ou plusieurs client(s) - sans savoir le(s)quel(s).

Les logisticien·ne·s de l'entreprise ont établi plusieurs scénarios. Ils aimeraient que vous écriviez un programme linéaire qui puisse tous les traiter.

La cheffe comptable vous demande pour chaque scénario de lui dire si le problème est résolvable, et si oui, quel sera le bénéfice net maximal ainsi que la quantité de GPU à transporter sur chacune des routes. Elle vous demandera également de présenter vos résolutions visuellement pour les managers commerciaux qui ont horreur des choses abstraites, et préfèrent des plus jolies représentations.

## Les données

Les logisticien·ne·s utilisent un format de fichier particulier pour instancier les scénarios :

```
p  start  n_clientsuppr  n_depsuppr
ENTITIES {
    id  type  b_entity
    ...
}
ROADS {
    road_start  road_end  cap_road  alpha_r  beta_r
    ...
}
```

### En-tête

- `p` : limite camion
- `start` : depot de départ
- `n_clientsuppr` : nombre de clients à ne pas servir
- `n_depsuppr` : nombre de depot hors service

### Bloc `ENTITIES`

- `id` : identifiant d'entité
- `type` : `depot` ou `customer` (pour client)
- `b_entity` : stock (entier négatif) si depot, demande (entier positif) si client

### Bloc `ROADS`

- `road_start` : origine de la route
- `road_end` : fin de la route
- `cap_road` : limite de GPU sur la route
- `alpha_r` : $\alpha_r$
- `beta_r` : $\beta_r$

## Questions

Ces questions peuvent vous guider lors de la rédaction mais ne sont aucunement suffisantes. Aussi, vous n'êtes pas obligé d'y répondre dans cet ordre, mais assurez vous d'y avoir répondu.

- [ ]  A quel(s) problème(s) théorique(s) est associé celui proposé par l'entreprise ?
- [ ]  Quelle structure de données allez vous utiliser pour représenter les informations des scénarios ?
- [ ]  De quoi doit-on s'assurer pour les clients ? Pour les dépôts ?
- [ ]  De quelle manière allez vous représenter le chemin de votre camion ? La quantité qu'il transporte sur les routes par lesquelles il est passé ?

## Conseils et idées

- Beaucoup d'informations tue l'organisation : classez les informations dans un ordre de priorité (commencez par les tâches basiques)
- Testez l'extraction des données : une bonne extraction, ce sont des bugs en moins
- Créez de plus petits exemples : s'inspirer des données pré-existentes
- Préférez un modèle fonctionnel pour les instances plus simples (savoir lesquelles) plutôt qu'un modèle général qui ne marche pas