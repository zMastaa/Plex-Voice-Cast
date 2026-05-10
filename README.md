# ❱ Plex Voice Cast

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

[Installation](#installation) ｜ [Configuration](#configuration) ｜ [Cast Devices](#cast-devices) ｜ [Commands](#commands)<br>
[Google Assistant Setup](#google-assistant-setup) ｜ [HA Conversation Setup](#home-assistant-conversation-setup) ｜ [Advanced Config](#advanced-configuration)<br><hr>

Plex Voice Cast is a modern Home Assistant integration for casting Plex media to Google Cast devices, Sonos devices, and Plex clients using natural language commands via Google Assistant, HA's conversation integration, or any service that can make an HA service call.

Example: `"Hey Google, tell Plex to play The Walking Dead on the Downstairs TV."`

Commands are sent via the `plex_voice_cast.command` service. You can test it directly from **Developer Tools → Actions** in Home Assistant.

> **Forked from [Plex Assistant](https://github.com/maykar/plex_assistant)** by [@maykar](https://github.com/maykar). Plex Voice Cast is a modernised fork updated for Home Assistant 2024.1+ with full async support, current HA APIs, and ongoing maintenance.

## Requirements

- Home Assistant **2024.1** or newer
- [HA's Plex integration](https://www.home-assistant.io/integrations/plex/) set up and working

## [Troubleshooting](https://github.com/zMastaa/Plex-Voice-Cast/blob/master/troubleshooting.md)

## Installation

* **Install with [HACS](https://hacs.xyz/):** Add this repository as a custom repository in HACS, then search for "Plex Voice Cast", select it, install, and restart.

* **Install Manually:** Copy the `/custom_components/plex_voice_cast/` folder into the `custom_components` folder in your HA config directory and restart.

## Configuration

Make sure [HA's Plex integration](https://www.home-assistant.io/integrations/plex/) is set up before adding Plex Voice Cast. If you want a Plex Client as your default device, make sure it is open and reachable before running setup.

* Go to **Settings → Integrations → Add Integration**
* Search for "Plex Voice Cast" and select it
* Follow the steps to choose your server, language, and default cast device

Your Plex server is automatically retrieved from HA's Plex integration. If you have more than one server it will ask which to use.

After setup, click **Configure** on the Plex Voice Cast card to adjust jump forward/back amounts and access advanced options.

## Cast Devices

Plex Voice Cast automatically detects compatible `media_player` entities: Google Cast devices, Sonos devices, and Plex clients. Set a default device in the configuration to use it when no device is specified in a command. Device names come from the HA friendly name of the entity.

## Google Assistant Setup

You can use either IFTTT or DialogFlow to trigger Plex Voice Cast with Google Assistant.

- **IFTTT** is the simplest option if your language is supported.
- **DialogFlow** supports more languages but requires more setup and always responds with "I'm starting the test version of Plex".

<details>
  <summary><b>IFTTT Setup Guide</b></summary>

## IFTTT Setup

#### In Home Assistant

* Go to **Settings → Integrations → Add Integration**
* Search for "IFTTT" and follow the on-screen instructions
* Copy the webhook URL displayed at the end

#### In IFTTT

Visit [ifttt.com](https://ifttt.com/) and sign in.

* Create a new applet and click **Add** next to "If This"
* Search for and select **Google Assistant** → "Say phrase with text ingredient"
* Set your trigger phrases, e.g. `tell plex to $` or `have plex $`. The `$` is the command sent to this integration.
* Click **Add** next to "Then That" → **Webhooks** → "Make a web request"
* Set the URL to the HA webhook URL from earlier, method **POST**, content type **application/json**
* Paste the following into the body field:

```
{ "action": "call_service", "service": "plex_voice_cast.command", "command": "{{TextField}}" }
```

Click **Create Action → Continue → Finish**.

You can now say "Hey Google, tell Plex to..." or "Hey Google, ask Plex to..."

</details>

<details>
  <summary><b>DialogFlow Setup Guide</b></summary>

## DialogFlow Setup

#### In Home Assistant

* Go to **Settings → Integrations → Add Integration**
* Search for "Dialogflow" and follow the on-screen instructions
* Copy the webhook URL displayed

#### In DialogFlow

Visit [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com) and sign in with the same Google account as your Google Assistant.

* Create an agent named "Plex"
* Click the settings icon next to "Plex" in the sidebar
* Go to **Export and Import** → **Restore from ZIP**
* Use the DialogFlow export from the original Plex Assistant project or create an intent manually
* Click **Fulfillment** in the sidebar and set the URL to your HA DialogFlow webhook
* Click **Save**

For non-English languages:
* Click the **+** next to "en" in the sidebar and add your language
* Click **Intents → Plex**, add "command" as a training phrase, double-click it and set `@sys.any:command`
* Save

To publish, click **Integrations → Test**.

You can now say "Hey Google, tell Plex to..." or "Hey Google, ask Plex to..."

</details>

### Currently Supported Languages

| Language | Code | IFTTT | DialogFlow | Music Support |
|:---------|:----:|:-----:|:----------:|:-------------:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/DK%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Danish**|`"da"`|:x:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/NL%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Dutch**|`"nl"`|:x:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/GB%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**English**|`"en"`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/FR%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**French**|`"fr"`|:heavy_check_mark:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/DE%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**German**|`"de"`|:heavy_check_mark:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/HU%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Hungarian**|`"hu"`|:x:|:heavy_check_mark:|:heavy_check_mark:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/IT%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Italian**|`"it"`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/NO%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Norwegian**|`"nb"`|:x:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/PT%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Portuguese**|`"pt"`|:x:|:heavy_check_mark:|:heavy_check_mark:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/ES%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Spanish**|`"es"`|:heavy_check_mark:|:heavy_check_mark:|:x:|
|<img src='https://raw.githubusercontent.com/yammadev/flag-icons/master/png/SE%402x.png?raw=true' height='12'>&nbsp;&nbsp;&nbsp;**Swedish**|`"sv"`|:x:|:heavy_check_mark:|:x:|

[Help add or improve support for more languages.](translation.md)<hr>

## Home Assistant Conversation Setup

Enable HA's [Conversation integration](https://www.home-assistant.io/integrations/conversation/) and Plex Voice Cast will respond to `"Tell Plex to {command}"` and `"{command} with Plex"` out of the box with no additional config.

To add custom trigger phrases, add them to your `configuration.yaml`:

```yaml
conversation:
  intents:
    Plex:
      - "Plex please would you {command}"
      - "I command plex to {command}"
```

## Commands

### Fuzzy Matching

Media titles and device names are matched using fuzzy search, so you don't need to be exact. `"play walk in deed on the dawn tee"` resolves to `"Play The Walking Dead on the Downstairs TV"`. Partial matches work too — `play Pets 2` will match `The Secret Life of Pets 2`.

For TV shows with no season/episode specified, Plex Voice Cast plays the first unwatched or in-progress episode. For music, if an artist, album, and track share a name, it assumes artist → album → track priority. You can be explicit: `"Play album Whenever You Need Somebody by Rick Astley"` or `"Play track Never Gonna Give You Up by Rick Astley"`.

### Example Commands

* `"play the latest episode of Breaking Bad on the Living Room TV"`
* `"play Breaking Bad"`
* `"play Add it Up by the Violent Femmes"`
* `"play the track Time to Pretend"`
* `"play the album Time to Pretend by MGMT"`
* `"play ondeck"`
* `"play random unwatched TV"`
* `"play season 1 episode 3 of The Simpsons"`
* `"play the first season second episode of Taskmaster on the Theater System"`

### Filter Keywords

* `season, episode, movie, show`
* `artist, album, track, playlist`
* `latest, recent, new`
* `unwatched, next`
* `ondeck`
* `random, shuffle, randomized, shuffled`

Filter keywords can be combined — `"play random unwatched movies"` plays all unwatched movies in random order.

### Control Commands

* `play`
* `pause`
* `stop`
* `next, skip, next track, skip forward`
* `previous, back, go back`
* `jump forward, fast forward, forward`
* `jump back, rewind`

Include the device name for control commands when it isn't the default: `"stop downstairs tv"` or `"previous on the livingroom tv"`.

For play commands, the device must appear at the end of the phrase preceded by `"on"` or `"on the"`: *"play Friends **on** Downstairs TV"*. Control commands don't require this.

## Advanced Configuration

Click **Configure** on the Plex Voice Cast card in **Settings → Integrations** to access these options.

### Keyword Replacements

Map phrases you want to say to commands the integration understands. Format: `"phrase":"replacement"`, comma-separated.

Add aliases for control commands:
```
"full speed ahead":"next", "reverse full power":"previous"
```

Resolve ambiguous titles (e.g. multiple Star Trek series):
```
"star trek":"star trek the next generation"
```

### Start Scripts

Trigger an HA script to launch a Plex client before playback if it isn't already running. Format: `"Friendly Name":"script.entity_id"`, comma-separated.

```
"LivingRoom TV":"script.start_lr_plex", "Bedroom TV":"script.open_br_plex"
```

Plex Voice Cast waits for the script to finish before continuing. The example below opens the Plex app on a Roku and waits until it's available:

```yaml
roku_plex:
  sequence:
    - choose:
        - conditions:
            - condition: template
              value_template: >-
                {{ state_attr('media_player.roku','source') == 'Plex - Stream for Free' }}
          sequence: []
      default:
        - action: media_player.select_source
          target:
            entity_id: media_player.roku
          data:
            source: 'Plex - Stream for Free'
        - repeat:
            while:
              - condition: template
                value_template: >-
                  {{ (state_attr('media_player.roku','source') != 'Plex - Stream for Free' or
                     is_state('media_player.plex_plex_for_roku_roku', 'unavailable')) and
                     repeat.index <= 20 }}
            sequence:
              - action: plex.scan_for_clients
              - delay:
                  seconds: 1
  mode: single
```
