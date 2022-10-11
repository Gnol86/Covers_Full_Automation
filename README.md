<a href="https://www.buymeacoffee.com/gnol86" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Covers Full Automation

## Introduction
`Cover Full Automation` est une application `AppDaemon` pour `Home Assistant` qui gère vos ouvrants, tel que des volets ou stores en passant par une porte de garage, de façon totalement automatique et simple.

### Examples
- Fermer les volets au couché du soleil.
- Ouvrir le volet si la fenêtre est ouverte.
- Fermer les volets si la maison est vide.
- Ouvrir les volets si l'alarme est déclanchée.
- Fermer les volets si le soleil est présent et chauffe trop la pièce.
- ... 

### Prérequis
Vos ouvrants doivent pouvoir être contrôlés via le poucetage d'ouverture `cover.set_cover_position`.

## Installation
Téléchargez le fichier `CoverFullAutomation.py` dans votre dossier local `apps` d'AppDaemon et configurez le module dans `apps.yaml`.

## App configuration
```yaml
CoversFullAutomation:
  module: CoversFullAutomation
  class: CoversFullAutomation
  rooms:
    living_room:
      sun_elevation: 2
      covers:
        - cover: cover.living
```
### CoversFullAutomation
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`rooms` | False | string | | Liste des pièces.
`open` | True | int | 100 | Valeur en pourcentage pour ouvrir les ouvrants.
`close` | True | int | 0 | Valeur en pourcentage pour fermer les ouvrants.
`ajar` | True | int | 50 | Valeur en pourcentage pour entrouvrir les ouvrants.
`active` | True | string | | Interrupteur pour activer/désactiver l’automatisation.
`alarms` | True | string | | Liste des alarmes pour ouvrir tous volets en cas d’état « Triggered ».
`presence_entity` | True | string | | Entité qui contient la valeur du mode actuel de la mainson.
`sun_elevation` | True | int | | Elevation du soleil à laquelle tous les ouvrants s’ouvrent ou se ferment.
`ignore_presence` | True | string | False | Définir à « True » pour ignoré le mode de la maison pour tous les ouvrants.
`ignore_alarms` | True | string | False | Définir à « True » pour ignoré les alarmes pour tous les ouvrants.
`ignore_sun_elevation` | True | string | False | Définir à « True » pour ignoré l’élévation du soleil pour tous les ouvrants.
`force_open` | True | string | | Force l’ouverture de tout les ouvrants si une ou plusieurs est active.
`force_close` | True | string | | Force la fermeture de tout les ouvrants si une ou plusieurs est active.
`force_ajar` | True | string | | Force l’entrouverture de tout les ouvrants si une ou plusieurs est active.
`wait_for_open` | True | string | | Si une ou plusieurs entités sont définies, tous les ouvrant ne s’ouvriront qu’au moment où une de celle-ci est activée.
`take_over_control` | True | string | True | Si un des ouvrants est modifié manuellement, le script ne le modifiera plus ce dernier jusqu’à ce qu’il retourne à sa position normalement voulue par l’automatisation.
### rooms
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`rooms` | False | string | | Liste des pièces.
`open` | True | int | 100 | Valeur en pourcentage pour ouvrir les ouvrants.
`close` | True | int | 0 | Valeur en pourcentage pour fermer les ouvrants.
`ajar` | True | int | 50 | Valeur en pourcentage pour entrouvrir les ouvrants.
`active` | True | string | | Interrupteur pour activer/désactiver l’automatisation.
`alarms` | True | string | | Liste des alarmes pour ouvrir tous volets en cas d’état « Triggered ».
`presence_entity` | True | string | | Entité qui contient la valeur du mode actuel de la mainson.
`sun_elevation` | True | int | | Elevation du soleil à laquelle tous les ouvrants s’ouvrent ou se ferment.
`ignore_presence` | True | string | False | Définir à « True » pour ignoré le mode de la maison pour tous les ouvrants.
`ignore_alarms` | True | string | False | Définir à « True » pour ignoré les alarmes pour tous les ouvrants.
`ignore_sun_elevation` | True | string | False | Définir à « True » pour ignoré l’élévation du soleil pour tous les ouvrants.
`force_open` | True | string | | Force l’ouverture de tout les ouvrants si une ou plusieurs est active.
`force_close` | True | string | | Force la fermeture de tout les ouvrants si une ou plusieurs est active.
`force_ajar` | True | string | | Force l’entrouverture de tout les ouvrants si une ou plusieurs est active.
`wait_for_open` | True | string | | Si une ou plusieurs entités sont définies, tous les ouvrant ne s’ouvriront qu’au moment où une de celle-ci est activée.
`take_over_control` | True | string | True | Si un des ouvrants est modifié manuellement, le script ne le modifiera plus ce dernier jusqu’à ce qu’il retourne à sa position normalement voulue par l’automatisation.




