import appdaemon.plugins.hass.hassapi as hass
import time

#
# Covers Full Automation
# @gnol86
# https://github.com/Gnol86/Covers_Full_Automation
#

class CoversFullAutomation(hass.Hass):

  def initialize(self):
    self.log("#--------------------------#")
    self.log("|  Covers Full Automation  |")
    self.log("#--------------------------#")

    self.error_messages = []
    self.debug      = self.getArg('debug',            default = False)
    self.active     = self.getArg('active',           default = False)
    self.delay      = self.getArg('delay',            default = 0.2)
    self.presence   = self.getArg('presence_entity',  default = None)
    self.alarms     = self.getArg('alarms',           default = [])
    if isinstance(self.alarms, str):
      a = []
      a.append(self.alarms)
      self.alarms = a

    self.covers = {}
    self.initCovers()
    self.triggers = {}
    if len(self.error_messages) == 0:
      self.initTriggers()

    #self.log(self.covers)
    #self.log(self.triggers)

    self.state_handles = []
    if self.error_config():
      if self.active:
        self.listen_state(self.callback,
          self.active,
          new = "on",
          immediate = True)
        self.listen_state(self.callback,
          self.active,
          new = "off",
          immediate = True)
      else:
        self.start()

  def start(self):
    if len(self.alarms) > 0:
      for alarm in self.alarms:
        self.state_handles.append(
          self.listen_state(
            self.callback,
            alarm,
            trigger_type = 'alarms'
            )
          )

    if self.presence != None:
      self.state_handles.append(
        self.listen_state(
          self.callback,
          self.presence,
          trigger_type = 'presence'
          )
        )
    for trigger_type in self.triggers:
      if trigger_type == 'sun_elevation':
        if len(self.triggers['sun_elevation']):
          self.state_handles.append(
            self.listen_state(
              self.callback,
              'sun.sun',
              attribute = "elevation",
              trigger_type = trigger_type
              )
            )
      else:
        for entity in self.triggers[trigger_type]:
          self.state_handles.append(
            self.listen_state(
              self.callback,
              entity,
              trigger_type = trigger_type
              )
            )
    if len(self.state_handles) <= 1:
      self.log(f'{len(self.state_handles)} trigger activated')
    else:
      self.log(f'{len(self.state_handles)} triggers activated')
    self.setCover(self.covers)

  def stop(self):
    while len(self.state_handles) > 0:
      handle = self.state_handles.pop()
      self.cancel_listen_state(handle)
    self.log(f'{len(self.state_handles)} trigger activated')

  def callback(self, entity, attribute, old, new, kwargs):
    if entity == self.active:
      if new == "on":
        self.start()
      else:
        self.stop()
    else:
      self.debug_log(f'---')
      self.debug_log(f'Trigger ({kwargs["trigger_type"]})')
      self.debug_log(f'{entity} : {old} -> {new}')
      listCovers = {}
      for cover in self.covers:
        if kwargs["trigger_type"] == "sun_elevation":
          listCovers = self.covers.copie()
        else:
          if entity in self.covers[cover][kwargs["trigger_type"]]:
            listCovers[cover] = self.covers[cover]
      self.setCover(listCovers, kwargs["trigger_type"])

  def setCover(self, listCovers={}, trigger_type="forced"):
    for cover in listCovers:
      old_position = listCovers[cover]['position']
      current_position = self.get_state(cover,'current_position')
      new_position = current_position
      reason = "nothing"
      valent = None
      if  (
          trigger_type == "forced" or
          old_position == current_position or
          not listCovers[cover]['take_over_control']
          ):

        cover_wait_for_open  =  (
                                len(listCovers[cover]['wait_for_open']) > 0
                                and trigger_type != "wait_for_open"
                                )
        # ALARM
        if not listCovers[cover]['ignore_alarms']:
          for alarm in self.alarms:
            valent = self.get_state(alarm)
            if self.isActive(valent):
              new_position = listCovers[cover]['open']
              reason = f"alarm ({alarm} = {valent})"
        
        # PRESENCE
        if reason == "nothing":
          if not listCovers[cover]['ignore_presence']:
            valent = self.get_state(self.presence)
            if not self.isActive(valent):
              new_position = listCovers[cover]['close']
              reason = f"presence ({self.presence} = {valent})"
        
        # FORCE OPEN
        if reason == "nothing":
          for ent in listCovers[cover]['force_open']:
            valent = self.get_state(ent)
            if self.isActive(valent):
              new_position =  listCovers[cover]['open']
              reason = f"force_open ({ent} = {valent})"
        
        # FORCE AJAR
        if reason == "nothing":
          for ent in listCovers[cover]['force_ajar']:
            valent = self.get_state(ent)
            if self.isActive(valent):
              new_position =  listCovers[cover]['ajar']
              reason = f"force_ajar ({ent} = {valent})"

        # FORCE CLOSE
        if reason == "nothing":
          for ent in listCovers[cover]['force_close']:
            valent = self.get_state(ent)
            if self.isActive(valent):
              new_position =  listCovers[cover]['close']
              reason = f"force_close ({ent} = {valent})"
        
        # SUN ELEVATION
        if reason == "nothing":
          if not listCovers[cover]['ignore_sun_elevation']:
            valent = self.get_state("sun.sun", 'elevation')
            if valent > listCovers[cover]['sun_elevation'] and not cover_wait_for_open:
              new_position =  listCovers[cover]['open']
              reason = f"sun_elevation ({valent} > {listCovers[cover]['sun_elevation']})"
            elif valent <= listCovers[cover]['sun_elevation'] :
              new_position =  listCovers[cover]['close']
              reason = f"sun_elevation ({valent} <= {listCovers[cover]['sun_elevation']})"

      self.debug_log('---')
      self.debug_log(f'  {cover} : {current_position} -> {new_position}')
      self.debug_log('    position set by :')
      self.debug_log(f'    {reason}')
      self.covers[cover]['position'] = new_position

      if new_position != current_position:
        self.call_service("cover/set_cover_position", entity_id = cover, position = new_position)
        if self.delay > 0:
          time.sleep(self.delay)
      

  def isActive(self, val):
    if val in ('on', 'home', 'triggered'):
      return True
    else:
      if val.isnumeric() and val != "0":
        return True
    return False

  def initTriggers(self):
    for cover in self.covers:
      for att in self.covers[cover]:
        if not att in ( 
                        'position',
                        'open',
                        'ajar',
                        'close',
                        'ignore_presence',
                        'ignore_alarms',
                        'ignore_sun_elevation',
                        'take_over_control',
                      ):
          match att:
            case 'sun_elevation':
              if att in self.triggers:
                if not self.covers[cover][att] in self.triggers[att]:
                  self.triggers[att].append(self.covers[cover][att])
              else:
                self.triggers[att] = []
                self.triggers[att].append(self.covers[cover][att])
            case other:
              if att in self.triggers:
                if not self.covers[cover][att] in self.triggers[att]:
                  for e in self.covers[cover][att]:
                    if not e in self.triggers[att]:
                      self.triggers[att].append(e)
              else:
                self.triggers[att] = []
                for e in self.covers[cover][att]:
                  self.triggers[att].append(e)

  def initCovers(self):
    for room in self.args['rooms']:
      for cover in self.args['rooms'][room]['covers']:
        cover_entity = cover['cover']
        if cover_entity in self.covers:
          self.error_config(f'"{cover_entity}" duplicated cover')
        self.covers[cover_entity] = {}
        self.covers[cover_entity]['position'] = self.get_state(cover_entity,'current_position')
        
        #COVER ATTRIBUTES
        listAttr = {}
        listAttr['sun_elevation'] = {'type': 'integer', 'default': 0,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['open'] = {'type': 'integer', 'default': 100,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['ajar'] = {'type': 'integer', 'default': 50,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['close'] = {'type': 'integer', 'default': 0,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['ignore_presence'] = {'type': 'boolean', 'default': False,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['ignore_alarms'] = {'type': 'boolean', 'default': False,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['ignore_sun_elevation'] = {'type': 'boolean', 'default': False,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['take_over_control'] = {'type': 'boolean', 'default': True,
                                        'all': True, 'room': True, 'cover': True}
        listAttr['force_open'] = {'type': 'multiple_entity', 'default': [],
                                        'all': True, 'room': True, 'cover': True}
        listAttr['force_close'] = {'type': 'multiple_entity', 'default': [],
                                        'all': True, 'room': True, 'cover': True}
        listAttr['force_ajar'] = {'type': 'multiple_entity', 'default': [],
                                        'all': True, 'room': True, 'cover': True}
        listAttr['wait_for_open'] = {'type': 'multiple_entity', 'default': [],
                                        'all': True, 'room': True, 'cover': True}
        for attr in listAttr:
          match listAttr[attr]['type']:
            case 'unique_entity':
              self.covers[cover_entity][attr] = listAttr[attr]['default']
              if listAttr[attr]['all'] and self.getValueList(self.args,attr) != '#':
                if isinstance(self.args[attr], str):
                  self.covers[cover_entity][attr].append(self.args[attr])
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['room'] and self.getValueList(self.args['rooms'][room],attr) != '#':
                if isinstance(self.args['rooms'][room][attr], str):
                  self.covers[cover_entity][attr].append(self.args['rooms'][room][attr])
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['cover'] and self.getValueList(cover,attr) != '#':
                if isinstance(cover[attr], str):
                  self.covers[cover_entity][attr].append(cover[attr])
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
            case 'multiple_entity':
              self.covers[cover_entity][attr] = listAttr[attr]['default']
              if listAttr[attr]['all'] and self.getValueList(self.args,attr) != '#':
                if isinstance(self.args[attr], str):
                  self.covers[cover_entity][attr].append(self.args[attr])
                else:
                  for att in self.args[attr]:
                    if isinstance(att, str):
                      self.covers[cover_entity][attr].append(att)
                    else:
                      self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['room'] and self.getValueList(self.args['rooms'][room],attr) != '#':
                if isinstance(self.args['rooms'][room][attr], str):
                  self.covers[cover_entity][attr].append(self.args['rooms'][room][attr])
                else:
                  for att in self.args['rooms'][room][attr]:
                    if isinstance(att, str):
                      self.covers[cover_entity][attr].append(att)
                    else:
                      self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['cover'] and self.getValueList(cover,attr) != '#':
                if isinstance(cover[attr], str):
                  self.covers[cover_entity][attr].append(cover[attr])
                else:
                  for att in cover[attr]:
                    if isinstance(att, str):
                      self.covers[cover_entity][attr].append(att)
                    else:
                      self.error_config(f'"{attr}" does not have a correct value')
            case 'boolean':
              self.covers[cover_entity][attr] = listAttr[attr]['default']
              if listAttr[attr]['all'] and self.getValueList(self.args,attr) != '#':
                if isinstance(self.args[attr], bool) and (self.args[attr] == 0 or self.args[attr] == 1):
                  self.covers[cover_entity][attr] = self.args[attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['room'] and self.getValueList(self.args['rooms'][room],attr) != '#':
                if isinstance(self.args['rooms'][room][attr], bool) and (self.args['rooms'][room][attr] == 0 or self.args['rooms'][room][attr] == 1):
                  self.covers[cover_entity][attr] = self.args['rooms'][room][attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['cover'] and self.getValueList(cover,attr) != '#':
                if isinstance(cover[attr], bool) and (cover[attr] == 0 or cover[attr] == 1):
                  self.covers[cover_entity][attr] = cover[attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
            case 'integer':
              self.covers[cover_entity][attr] = listAttr[attr]['default']
              if listAttr[attr]['all'] and self.getValueList(self.args,attr) != '#':
                if isinstance(self.args[attr], int):
                  self.covers[cover_entity][attr] = self.args[attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['room'] and self.getValueList(self.args['rooms'][room],attr) != '#':
                if isinstance(self.args['rooms'][room][attr], int):
                  self.covers[cover_entity][attr] = self.args['rooms'][room][attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')
              if listAttr[attr]['cover'] and self.getValueList(cover,attr) != '#':
                if isinstance(cover[attr], int):
                  self.covers[cover_entity][attr] = cover[attr]
                else:
                  self.error_config(f'"{attr}" does not have a correct value')

  def getArg(self, arg, multiple = False, default = []):
    value = default
    if self.getValueList(self.args,arg) != '#':
      value = self.args[arg]
    if multiple and isinstance(value, str):
      value = [value]
    return value

  def getValueList(self, list, key):
    try:
        value = list[key]
        return value
    except KeyError:
        return '#'

  def debug_log(self, message):
    if self.debug:
      self.log(message)

  def error_config(self, message="SHOW"):
    if message == "SHOW":
      if len(self.error_messages) > 0:
        for m in self.error_messages:
          self.log(f"ERROR : {m}")
        self.log('!!! Check your configuration !!!')
        return False
      else:
        return True
    self.error_messages.append(message)
    return True
