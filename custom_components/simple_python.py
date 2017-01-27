# modified from tutorial at https://home-assistant.io/cookbook/python_component_simple_alarm/

"""Simple alarm component."""
import logging

import homeassistant.loader as loader
from homeassistant.components import input_boolean, notify
from homeassistant.helpers.event import track_state_change
from homeassistant.const import STATE_ON, STATE_OFF

DOMAIN = "simple_python"

DEPENDENCIES = ['input_boolean']

# Attribute to tell which bit to toggle when activated
# If omitted will flash all.
PY_OUTPUT = "output_bit"


# Services to test the alarms
SERVICE_TEST_FLASH = "test_flash"


def setup(hass, config):
    # """ Sets up the simple alarms. """
    # logger = logging.getLogger(__name__)

    # light_ids = []

    # for conf_key in (CONF_KNOWN_LIGHT, CONF_UNKNOWN_LIGHT):
        # light_id = config[DOMAIN].get(conf_key, light.ENTITY_ID_ALL_LIGHTS)

        # if hass.states.get(light_id) is None:
            # logger.error(
                # 'Light id %s could not be found in state machine', light_id)

            # return False

        # light_ids.append(light_id)

 #   # pylint: disable=unbalanced-tuple-unpacking
    # known_light_id, unknown_light_id = light_ids

    # if hass.states.get(input_boolean.ENTITY_ID_ALL_DEVICES) is None:
        # logger.error('No devices are being tracked, cannot setup alarm')

        # return False

    def test_flash():
        """ Fire an alarm if a known person arrives home. """
	#	input_boolean.turn_on(hass, input_boolean.sun_debug)

        # Send a message to the user
        notify.send_message(
            hass, "The lights just got turned on while no one was home.")

    # Setup services to test the effect
    hass.services.register(
        DOMAIN, SERVICE_TEST_FLASH, lambda call: test_flash())
   # hass.services.register(
  #      DOMAIN, SERVICE_TEST_UNKNOWN_ALARM, lambda call: unknown_alarm())

    # def unknown_alarm_if_lights_on(entity_id, old_state, new_state):
        # """ Called when a light has been turned on. """
        # if not device_tracker.is_on(hass):
            # unknown_alarm()

    # track_state_change(
        # hass, light.ENTITY_ID_ALL_LIGHTS,
        # unknown_alarm_if_lights_on, STATE_OFF, STATE_ON)

    # def ring_known_alarm(entity_id, old_state, new_state):
        # """ Called when a known person comes home. """
        # if light.is_on(hass, known_light_id):
            # known_alarm()

    # Track home coming of each device
    # track_state_change(
        # hass, hass.states.entity_ids(device_tracker.DOMAIN),
        # ring_known_alarm, STATE_NOT_HOME, STATE_HOME)

    return True