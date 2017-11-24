"""
Allows to configure a switch using RPi GPIO.
"""
import logging
import RPi.GPIO as GPIO

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.helpers.entity import ToggleEntity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PULL_MODE = 'pull_mode'
CONF_PORTS = 'ports'
CONF_INVERT_LOGIC = 'invert_logic'

DEFAULT_INVERT_LOGIC = False

_SWITCHES_SCHEMA = vol.Schema({
    cv.positive_int: cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PORTS): _SWITCHES_SCHEMA,
    vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
})

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Raspberry PI GPIO devices."""
    invert_logic = config.get(CONF_INVERT_LOGIC)

    switches = []
    ports = config.get(CONF_PORTS)
    for port, name in ports.items():
        switches.append(RPiGPIOSwitch(name, port, invert_logic))
    add_devices(switches)

class RPiGPIOSwitch(ToggleEntity):
    """Representation of a  Raspberry Pi GPIO."""

    def __init__(self, name, port, invert_logic):
        """Initialize the pin."""
        self._name = name or DEVICE_DEFAULT_NAME
        self._port = port
        self._invert_logic = invert_logic
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name
     
    @property     
    def is_on(self):
        """Return true if device is on."""
        GPIO.setup(self._port, GPIO.OUT)
        return GPIO.input(self._port)

    def turn_on(self, **kwargs):
        """Turn the device on."""
        GPIO.output(self._port, 0 if self._invert_logic else 1)

    def turn_off(self, **kwargs):
        """Turn the device off."""
        GPIO.output(self._port, 1 if self._invert_logic else 0)
