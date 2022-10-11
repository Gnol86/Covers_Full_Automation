<a href="https://www.buymeacoffee.com/gnol86" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Covers Full Automation

## Introduction
Cover Full Automation est une application `AppDaemon` pour `Home Assistant` qui gère vos ouvrants, tel que des volets ou stores en passant par une porte de garage, de façon totalement automatique et simple.

### Example:
- Fermer les volets au couché du soleil.
- Ouvrir le volet si la fenêtre est ouverte.
- Fermer les volets si la maison est vide.
- Ouvrir les volets si l'alarme est déclanchée.
- Fermer les volets si le soleil est présent et chauffe trop la pièce.
- ... 

## Installation
Téléchargez le fichier `CoverFullAutomation.py` dans votre dossier local `apps` d'AppDaemon et configurez le module dans `apps.yaml`.

## App configuration
```yaml
bathroom_wasp:
  module: wasp
  class: Wasp
  device_class: occupancy
  name: Bathroom Occupancy
  delay: 5
  box_sensors:
    - binary_sensor.bathroom_door_sensor
  wasp_sensors:
    - binary_sensor.bathroom_motion_sensor
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`device_class` | True | string | occupancy | The device class of the binary sensor.
`name` | True | string | Defaults to the app name, e.g. Bathroom Wasp | The friendly_name of the sensor. 
`delay` | True | int | 0 | The number of seconds after closing the box before a wasp will be detected.
`box_sensors` | False | list | | A list of sensor entity_ids, e.g. door sensors.
`wasp_sensors` | False | list | | A list of sensor entity_ids, e.g. motion sensors.
