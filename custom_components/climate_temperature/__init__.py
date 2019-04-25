"""
This component provides support for Climate Temperature.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/ham/
"""
import logging

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN

from .const import *
from .climate_temperature_data import ClimateTemperatureData

DEPENDENCIES = [CLIMATE_DOMAIN]

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Set up an Climate Temperature component."""

    try:
        scan_interval = SCAN_INTERVAL

        dt_data = ClimateTemperatureData(hass, scan_interval)

        was_initialized = dt_data.was_initialized()

        if was_initialized:
            hass.data[DATA_CT] = dt_data

            _LOGGER.debug(f'Climate Temperature config: {config}')

        return was_initialized

    except Exception as ex:
        _LOGGER.error(f'Error while initializing BL, exception: {str(ex)}')

        hass.components.persistent_notification.create(
            f'Error: {ex}<br />You will need to restart hass after fixing.',
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)

        return False
