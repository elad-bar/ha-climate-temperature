"""
This component provides support for Climate Temperature.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/ham/
"""
import logging
from homeassistant.const import (EVENT_HOMEASSISTANT_START)
from homeassistant.helpers.event import track_time_interval

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

from .const import *

_LOGGER = logging.getLogger(__name__)


class ClimateTemperatureData:
    """The Class for handling the data retrieval."""

    def __init__(self, hass, scan_interval):
        """Initialize the data object."""
        _LOGGER.debug("ClimateTemperatureData initialization")

        self._hass = hass
        self._was_initialized = False
        self._entity_ids = []

        def ct_refresh(event_time):
            """Call to refresh information."""
            _LOGGER.debug(f'Updating {DEFAULT_NAME} component, at {event_time}')
            self.update()

        self._ct_refresh = ct_refresh

        # register service
        hass.services.register(DOMAIN, 'update', ct_refresh)

        # register scan interval
        track_time_interval(hass, ct_refresh, scan_interval)

        hass.bus.listen_once(EVENT_HOMEASSISTANT_START, ct_refresh)

        self._was_initialized = True

    def was_initialized(self):
        return self._was_initialized

    def create_persistent_notification(self, message):
        self._hass.components.persistent_notification.create(
                    message,
                    title=NOTIFICATION_TITLE,
                    notification_id=NOTIFICATION_ID)

    def load_domain_entities(self, domain):
        entity_ids = self._hass.states.entity_ids(domain)

        for entity_id in entity_ids:
            state = self._hass.states.get(entity_id)
            entity_friendly_name = state.attributes[ATTR_FRIENDLY_NAME]

            if ATTR_CURRENT_TEMPERATURE in state.attributes:
                ct_entity_id = f'{entity_id}_{TEMPERATURE_LOWER}'
                ct_entity_id = ct_entity_id.replace(f'{CLIMATE_DOMAIN}.', f'{SENSOR_DOMAIN}.')

                ct_state = state.attributes[ATTR_CURRENT_TEMPERATURE]
                ct_friendly_name = f'{entity_friendly_name} {TEMPERATURE}'
                ct_attributes = {
                    ATTR_FRIENDLY_NAME:  ct_friendly_name,
                    ATTR_UNIT_OF_MEASUREMENT: 'C'
                    }

                should_update = True

                log_message = f'Sensor {ct_friendly_name} of entity_id: {entity_friendly_name}'
                if ct_entity_id in self._entity_ids:
                    current_temp_state = self._hass.states.get(ct_entity_id).state

                    if str(current_temp_state) == str(ct_state):
                        _LOGGER.debug(f'{log_message} was not updated')
                        should_update = False
                    else:
                        _LOGGER.info(f'{log_message} updated from {current_temp_state}c to {ct_state}c')
                else:
                    _LOGGER.info(f'{log_message}, Temperature: {ct_state}c')
                    self._entity_ids.append(ct_entity_id)

                if should_update:
                    self._hass.states.set(ct_entity_id, ct_state, ct_attributes)

    def update(self):
        try:
            _LOGGER.debug(f'Updating {DEFAULT_NAME}')

            self.load_domain_entities(CLIMATE_DOMAIN)

            _LOGGER.debug("update - Completed")
        except Exception as ex:
            _LOGGER.error(f'Error while updating {DOMAIN}, exception: {str(ex)}')
