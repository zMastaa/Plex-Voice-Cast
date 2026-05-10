from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import entity_registry as er

import voluptuous as vol

from .const import DOMAIN
from .localize import translations


def get_devices(_self):
    devices = []
    registry = er.async_get(_self.hass)
    for entry in registry.entities.values():
        if entry.domain != "media_player":
            continue
        platform = entry.platform or ""
        if not any(x in platform for x in ["plex", "cast"]):
            continue
        state = _self.hass.states.get(entry.entity_id)
        if state is None:
            continue
        name = state.attributes.get("friendly_name")
        if name:
            devices.append(name)
    return devices


def get_servers(_self):
    try:
        return [x.title for x in _self.hass.config_entries.async_entries("plex")]
    except (KeyError, AttributeError):
        return []


def get_schema(_self):
    multi_server_schema = {vol.Optional("server_name"): vol.In(_self.servers)}
    default_schema = {
        vol.Optional("language", default="en"): vol.In(translations.keys()),
        vol.Optional("default_cast"): vol.In(get_devices(_self)),
        vol.Optional("tts_errors", default=True): bool,
    }
    return {**multi_server_schema, **default_schema} if len(_self.servers) > 1 else default_schema


class PlexVoiceCastFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PlexVoiceCastOptionsFlowHandler(config_entry)

    def __init__(self):
        self.servers = None

    async def async_step_user(self, user_input=None):
        self.servers = get_servers(self)

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if len(self.servers) < 1:
            return self.async_abort(reason="no_plex_server")
        if user_input is not None:
            server = user_input["server_name"] if "server_name" in user_input else self.servers[0]
            return self.async_create_entry(title=server, data=user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(get_schema(self)),
        )


class PlexVoiceCastOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        options = dict(self.config_entry.options)
        if user_input is not None:
            options.update(user_input)
            return self.async_create_entry(title="", data=options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "start_script",
                        description={"suggested_value": options.get("start_script", "")},
                        default="",
                    ): str,
                    vol.Optional(
                        "keyword_replace",
                        description={"suggested_value": options.get("keyword_replace", "")},
                        default="",
                    ): str,
                    vol.Required("jump_f", default=options.get("jump_f", 30)): int,
                    vol.Required("jump_b", default=options.get("jump_b", 15)): int,
                }
            ),
        )
