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

## Configuration
### Exemple simple
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
`debug` | True | boelaen | False | Active le mode débug.
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
`id de la pièce` | False | | | The module name of the app.
`covers` | False | | | Liste des ouvrants.
`open` | True | int | 100 | Valeur en pourcentage pour ouvrir les ouvrants de la pièce.
`close` | True | int | 0 | Valeur en pourcentage pour fermer les ouvrants de la pièce.
`ajar` | True | int | 50 | Valeur en pourcentage pour entrouvrir les ouvrants de la pièce.
`sun_elevation` | True | int | | Elevation du soleil à laquelle les ouvrants de la pièce s’ouvrent ou se ferment.
`ignore_presence` | True | string | False | Définir à « True » pour ignoré le mode de la maison pour les ouvrants de la pièce.
`ignore_alarms` | True | string | False | Définir à « True » pour ignoré les alarmes pour les ouvrants de la pièce.
`ignore_sun_elevation` | True | string | False | Définir à « True » pour ignoré l’élévation du soleil pour les ouvrants de la pièce.
`force_open` | True | string | | Force l’ouverture de tout les ouvrants de la pièce si une ou plusieurs est active.
`force_close` | True | string | | Force la fermeture de tout les ouvrants de la pièce si une ou plusieurs est active.
`force_ajar` | True | string | | Force l’entrouverture de tout les ouvrants de la pièce si une ou plusieurs est active.
`wait_for_open` | True | string | | Si une ou plusieurs entités sont définies, les ouvrant de la pièce ne s’ouvriront qu’au moment où une de celle-ci est activée.
`take_over_control` | True | string | True | Si un des ouvrants de la pièce est modifié manuellement, le script ne le modifiera plus ce dernier jusqu’à ce qu’il retourne à sa position normalement voulue par l’automatisation.
### covers
key | optional | type | default | description
-- | -- | -- | -- | --
`cover` | False | | | Entité de l’ouvrant « cover.salon_1 ».
`open` | True | int | 100 | Valeur en pourcentage pour ouvrir cet ouvrant.
`close` | True | int | 0 | Valeur en pourcentage pour fermer cet ouvrant.
`ajar` | True | int | 50 | Valeur en pourcentage pour entrouvrir cet ouvrant.
`sun_elevation` | True | int | | Elevation du soleil à laquelle cet ouvrant s’ouvre ou se ferme.
`ignore_presence` | True | string | False | Définir à « True » pour ignoré le mode de la maison pour cet ouvrant.
`ignore_alarms` | True | string | False | Définir à « True » pour ignoré les alarmes pour cet ouvrant.
`ignore_sun_elevation` | True | string | False | Définir à « True » pour ignoré l’élévation du soleil pour cet ouvrant.
`force_open` | True | string | | Force l’ouverture de cet ouvrant si une ou plusieurs est active.
`force_close` | True | string | | Force la fermeture de cet ouvrant si une ou plusieurs est active.
`force_ajar` | True | string | | Force l’entrouverture de cet ouvrant si une ou plusieurs est active.
`wait_for_open` | True | string | | Si une ou plusieurs entités sont définies, cet ouvrant ne s’ouvrira qu’au moment où une de celle-ci est activée.
`take_over_control` | True | string | True | Si cet ouvrant est modifié manuellement, le script ne le modifiera plus ce dernier jusqu’à ce qu’il retourne à sa position normalement voulue par l’automatisation.
### Exemple complexe
```yaml
CFA:
  module: CoversFullAutomation
  class: CoversFullAutomation
  debug: true
  active: input_boolean.volets_automatiques
  alarms: alarm_control_panel.alarmo
  presence_entity: zone.home
  rooms:
    stores_cuisine:
      wait_for_open:
        - binary_sensor.sensor_cuisine_motion
        - binary_sensor.porte_cuisine_contact
        - binary_sensor.porte_salon_contact
      sun_elevation: 2
      covers:
        - cover: cover.store_cuisine_1
          force_open: binary_sensor.fenetre_cuisine_1_contact
        - cover: cover.store_cuisine_2
          force_open: binary_sensor.fenetre_cuisine_2_contact
        - cover: cover.store_cuisine_3
          force_open: binary_sensor.fenetre_cuisine_3_contact
    salon:
      force_ajar: binary_sensor.trop_de_soleil_dans_salon
      sun_elevation: -2
      covers:
        - cover: cover.volet_salon_1
          force_close: binary_sensor.fenetre_salon_1_contact
        - cover: cover.volet_salon_2
          force_open: binary_sensor.fenetre_salon_2_contact
        - cover: cover.volet_salon_3
          force_open: binary_sensor.fenetre_salon_3_contact
        - cover: cover.volet_salon_4
          force_open: binary_sensor.fenetre_salon_4_contact
        - cover: cover.volet_salon_5
          force_open: binary_sensor.fenetre_salon_5_contact
    cuisine:
      covers:
        - cover: cover.volet_cuisine_1
          force_open: binary_sensor.fenetre_cuisine_1_contact
        - cover: cover.volet_cuisine_2
          force_open: binary_sensor.fenetre_cuisine_2_contact
        - cover: cover.volet_cuisine_3
          force_open: binary_sensor.fenetre_cuisine_3_contact
    chambre:
      ajar: 0
      force_ajar: binary_sensor.trop_de_soleil_dans_chambre
      force_close:
        - input_boolean.arnaud_dort
        - input_boolean.isabelle_dort
      covers:
        - cover: cover.volet_chambre_1
          force_open: binary_sensor.fenetre_chambre_1_contact
        - cover: cover.volet_chambre_2
          force_open: binary_sensor.fenetre_chambre_2_contact
        - cover: cover.volet_chambre_3
          force_open: binary_sensor.fenetre_chambre_3_contact
```
