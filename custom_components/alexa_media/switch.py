#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: Apache-2.0
"""
Alexa Devices Switches.

For more details about this platform, please refer to the documentation at
https://community.home-assistant.io/t/echo-devices-alexa-as-media-player-testers-needed/58639
"""
import logging
from typing import List  # noqa pylint: disable=unused-import

from homeassistant.components.switch import SwitchDevice
from homeassistant.exceptions import NoEntitySpecifiedError

from . import (
    CONF_EMAIL,
    CONF_EXCLUDE_DEVICES,
    CONF_INCLUDE_DEVICES,
    DATA_ALEXAMEDIA,
    DOMAIN as ALEXA_DOMAIN,
    hide_email,
    hide_serial,
)
from .helpers import _catch_login_errors, add_devices, retry_async

_LOGGER = logging.getLogger(__name__)


@retry_async(limit=5, delay=5, catch_exceptions=True)
async def async_setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Alexa switch platform."""
    devices = []  # type: List[DNDSwitch]
    SWITCH_TYPES = [
        ("dnd", DNDSwitch),
        ("shuffle", ShuffleSwitch),
        ("repeat", RepeatSwitch),
    ]
    account = config[CONF_EMAIL]
    include_filter = config.get(CONF_INCLUDE_DEVICES, [])
    exclude_filter = config.get(CONF_EXCLUDE_DEVICES, [])
    account_dict = hass.data[DATA_ALEXAMEDIA]["accounts"][account]
    _LOGGER.debug("%s: Loading switches", hide_email(account))
    if "switch" not in account_dict["entities"]:
        (hass.data[DATA_ALEXAMEDIA]["accounts"][account]["entities"]["switch"]) = {}
    for key, _ in account_dict["devices"]["media_player"].items():
        if key not in account_dict["entities"]["media_player"]:
            _LOGGER.debug(
                "%s: Media player %s not loaded yet; delaying load",
                hide_email(account),
                hide_serial(key),
            )
            return False
        if key not in (
            hass.data[DATA_ALEXAMEDIA]["accounts"][account]["entities"]["switch"]
        ):
            (
                hass.data[DATA_ALEXAMEDIA]["accounts"][account]["entities"]["switch"][
                    key
                ]
            ) = {}
            for (switch_key, class_) in SWITCH_TYPES:
                if (
                    switch_key == "dnd"
                    and not account_dict["devices"]["switch"][key].get("dnd")
                ) or (
                    switch_key in ["shuffle", "repeat"]
                    and "MUSIC_SKILL"
                    not in account_dict["devices"]["media_player"][key].get(
                        "capabilities"
                    )
                ):
                    _LOGGER.debug(
                        "%s: Skipping %s for %s",
                        hide_email(account),
                        switch_key,
                        hide_serial(key),
                    )
                    continue
                alexa_client = class_(
                    account_dict["entities"]["media_player"][key], account
                )  # type: AlexaMediaSwitch
                _LOGGER.debug(
                    "%s: Found %s %s switch with status: %s",
                    hide_email(account),
                    hide_serial(key),
                    switch_key,
                    alexa_client.is_on,
                )
                devices.append(alexa_client)
                (
                    hass.data[DATA_ALEXAMEDIA]["accounts"][account]["entities"][
                        "switch"
                    ][key][switch_key]
                ) = alexa_client
        else:
            for alexa_client in hass.data[DATA_ALEXAMEDIA]["accounts"][account][
                "entities"
            ]["switch"][key].values():
                _LOGGER.debug(
                    "%s: Skipping already added device: %s",
                    hide_email(account),
                    alexa_client,
                )
    return await add_devices(
        hide_email(account),
        devices,
        add_devices_callback,
        include_filter,
        exclude_filter,
    )


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the Alexa switch platform by config_entry."""
    return await async_setup_platform(
        hass, config_entry.data, async_add_devices, discovery_info=None
    )


async def async_unload_entry(hass, entry) -> bool:
    """Unload a config entry."""
    account = entry.data[CONF_EMAIL]
    account_dict = hass.data[DATA_ALEXAMEDIA]["accounts"][account]
    for key, switches in account_dict["entities"]["switch"].items():
        for device in switches[key].values():
            await device.async_remove()
    return True


class AlexaMediaSwitch(SwitchDevice):
    """Representation of a Alexa Media switch."""

    def __init__(self, client, switch_property, switch_function, account, name="Alexa"):
        """Initialize the Alexa Switch device."""
        # Class info
        self._client = client
        self._login = client._login
        self._account = account
        self._name = name
        self._switch_property = switch_property
        self._state = False
        self._switch_function = switch_function

    async def async_added_to_hass(self):
        """Store register state change callback."""
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        # Register event handler on bus
        self._listener = self.hass.bus.async_listen(
            f"{ALEXA_DOMAIN}_{hide_email(self._login.email)}"[0:32], self._handle_event
        )

    async def async_will_remove_from_hass(self):
        """Prepare to remove entity."""
        # Register event handler on bus
        self._listener()

    def _handle_event(self, event):
        """Handle events.

        This will update PUSH_MEDIA_QUEUE_CHANGE events to see if the switch
        should be updated.
        """
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        if "queue_state" in event.data:
            queue_state = event.data["queue_state"]
            if queue_state["dopplerId"]["deviceSerialNumber"] == self._client.unique_id:
                self._state = getattr(self._client, self._switch_property)
                self.async_schedule_update_ha_state()

    @_catch_login_errors
    async def _set_switch(self, state, **kwargs):
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        success = await self._switch_function(state)
        # if function returns  success, make immediate state change
        if success:
            setattr(self._client, self._switch_property, state)
            _LOGGER.debug(
                "Switch set to %s based on %s",
                getattr(self._client, self._switch_property),
                state,
            )
            self.async_schedule_update_ha_state()
        elif self.should_poll:
            # if we need to poll, refresh media_client
            _LOGGER.debug(
                "Requesting update of %s due to %s switch to %s",
                self._client,
                self._name,
                state,
            )
            await self._client.async_update()

    @property
    def is_on(self):
        """Return true if on."""
        return self.available and getattr(self._client, self._switch_property)

    async def async_turn_on(self, **kwargs):
        """Turn on switch."""
        await self._set_switch(True, **kwargs)

    async def async_turn_off(self, **kwargs):
        """Turn off switch."""
        await self._set_switch(False, **kwargs)

    @property
    def available(self):
        """Return the availabilty of the switch."""
        return getattr(self._client, self._switch_property) is not None

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._client.unique_id + "_" + self._name

    @property
    def name(self):
        """Return the name of the switch."""
        return "{} {} switch".format(self._client.name, self._name)

    @property
    def device_class(self):
        """Return the device_class of the switch."""
        return "switch"

    @property
    def hidden(self):
        """Return whether the switch should be hidden from the UI."""
        return not self.available

    @property
    def should_poll(self):
        """Return the polling state."""
        return not (
            self.hass.data[DATA_ALEXAMEDIA]["accounts"][self._account]["websocket"]
        )

    @_catch_login_errors
    async def async_update(self):
        """Update state."""
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        try:
            self.async_schedule_update_ha_state()
        except NoEntitySpecifiedError:
            pass  # we ignore this due to a harmless startup race condition

    @property
    def device_info(self):
        """Return device_info for device registry."""
        return {
            "identifiers": {(ALEXA_DOMAIN, self._client.unique_id)},
            "via_device": (ALEXA_DOMAIN, self._client.unique_id),
        }

    @property
    def icon(self):
        """Return the icon of the switch."""
        return self._icon()

    def _icon(self, on=None, off=None):
        return on if self.is_on else off


class DNDSwitch(AlexaMediaSwitch):
    """Representation of a Alexa Media Do Not Disturb switch."""

    def __init__(self, client, account):
        """Initialize the Alexa Switch."""
        # Class info
        super().__init__(
            client,
            "dnd_state",
            client.alexa_api.set_dnd_state,
            account,
            "do not disturb",
        )

    @property
    def icon(self):
        """Return the icon of the switch."""
        return super()._icon("mdi:do-not-disturb", "mdi:do-not-disturb-off")

    def _handle_event(self, event):
        """Handle events.

        This will update PUSH_EQUALIZER_STATE_CHANGE events to see if the DND switch
        should be updated.
        """
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        if "player_state" in event.data:
            queue_state = event.data["player_state"]
            if queue_state["dopplerId"]["deviceSerialNumber"] == self._client.unique_id:
                self._state = getattr(self._client, self._switch_property)
                self.async_schedule_update_ha_state()


class ShuffleSwitch(AlexaMediaSwitch):
    """Representation of a Alexa Media Shuffle switch."""

    def __init__(self, client, account):
        """Initialize the Alexa Switch."""
        # Class info
        super().__init__(
            client, "shuffle", client.alexa_api.shuffle, account, "shuffle"
        )

    @property
    def icon(self):
        """Return the icon of the switch."""
        return super()._icon("mdi:shuffle", "mdi:shuffle-disabled")


class RepeatSwitch(AlexaMediaSwitch):
    """Representation of a Alexa Media Repeat switch."""

    def __init__(self, client, account):
        """Initialize the Alexa Switch."""
        # Class info
        super().__init__(
            client, "repeat_state", client.alexa_api.repeat, account, "repeat"
        )

    @property
    def icon(self):
        """Return the icon of the switch."""
        return super()._icon("mdi:repeat", "mdi:repeat-off")
