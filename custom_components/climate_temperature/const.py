from datetime import timedelta

VERSION = '1.0.1'

DOMAIN = 'climate_temperature'
DATA_CT = f'data_{DOMAIN}'
SIGNAL_UPDATE_CT = f'{DOMAIN}_update'

DEFAULT_NAME = 'Climate Temperature'
TEMPERATURE = 'Temperature'
TEMPERATURE_LOWER = 'temperature'

NOTIFICATION_ID = f'{DOMAIN}_notification'
NOTIFICATION_TITLE = f'{DEFAULT_NAME} Setup'

ATTR_CURRENT_TEMPERATURE = 'current_temperature'
ATTR_FRIENDLY_NAME = 'friendly_name'
ATTR_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

SCAN_INTERVAL = timedelta(seconds=60)
