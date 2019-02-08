# hass-aarlo

Asynchronous Arlo Component for Home Assistant.

The component operates in a similar way to the [Arlo](https://arlo.netgear.com/#/cameras) web site - it opens a single event stream to the Arlo backend and monitors events and state changes for all base stations, cameras and doorbells in a system. Currently it only lets you set base station modes.

The component supports:
* base station mode changes
* camera motion detection
* camera audio detection
* door bell motion detection
* door bell button press
* on the Lovelace UI it will report camera streaming state on the picture entity - ie, a clip is being recorded or somebody is view a stream on the Arlo app or if the camera is too cold to operate
* saving of state across restarts

It provides a custom lovelace resource that is a specialised version of a picture-glance that allows you to see the last snapshot taken and give quick access to clip counts, the last recorded video and signal and battery levels.

**This is an alpha release - it's working great for me - 3 base stations, 11 cameras, 2 doorbells - but I haven't had chance to test it against many different configurations!**
**If I had to say where stuff might blow up I'd guess at the resource card, I've only really tested it on Chrome!**

## Notes
Wherever you see `/config` in this README it refers to your home-assistant configuration directory. For me, for example, it's `/home/steve/ha` that is mapped to `/config` inside my docker container.

## Installation

### Manually
Copy the `aarlo`, `alarm_control_panel`, `binary_sensor`, `camera` and `sensor` directories into your `/config/custom_components` directory.

Copy the www directory into you `/config` directory.

### Script
Run the install script. Run it once to make sure the operations look sane and run it a second time with the `go` paramater to do the actual work. If you update just rerun the script, it will overwrite all installed files.

```sh
install /config
# check output looks good
install go /config
```

## Component Configuration
For the simplest use replace all instances of the `arlo` with `aalro` in your home-assistant configuration files. To support motion and audio capture add `aarlo` as a platform to the `binary_sensor` list.

The following is an example configuration:

```yaml
aarlo:
  username: !secret arlo_username
  password: !secret arlo_password

camera:
  - platform: aarlo
    ffmpeg_arguments: '-pred 1 -q:v 2'

alarm_control_panel:
  - platform: aarlo
    home_mode_name: Home
    away_mode_name: Armed

binary_sensor:
  - platform: aarlo
    monitored_conditions:
    - motion
    - sound
    - ding

sensor:
  - platform: aarlo
    monitored_conditions:
    - last_capture
    - total_cameras
    - battery_level
    - captured_today
    - signal_strength
```

The following new parameters can be specified against the aarlo platform:

```yaml
aarlo:
  username: !secret arlo_username
  password: !secret arlo_password
  packet_dump: True
  db_motion_time: 30
  db_ding_time: 10
  recent_time: 10
```
* If `packet_dump` is True `aarlo` will store all the packets it sees in `/config/.aarlo/packets.dump` file.
* `db_motion_time` sets how long a doorbell motion will last. Arlo doorbell only indicates motion is present not that it stops. You can adjust the stop time out here.
* `db_ding_time` sets how long a doorbell button press will last. As with motion Arlo doorbell only tells us it's pressed not released.
* `recent_time` is used to hold the cameras in a `recent activity` state after a recording or streaming event. The actually streaming or recording can be over in a few seconds and without this the camera will revert back to idle possible looking like nothing has happend.

Now restart your home assistant system.

## Resource Configuration

The new resource `aarlo-glance` is based on `picture-glance` but tailored for the Arlo component to simplify the configuration. To enable it add the following to the top of your UI configuration file.

```yaml
resources:
  - type: module
    url: /local/aarlo-glance.js
```
You configure a camera with the following yaml. The `show` parameters are optional but you must have atleast one.

```yaml
type: 'custom:aarlo-glance'
camera: front_door_camera
name: Front Door
show:
  - motion
  - sound
  - battery
  - signal_strength
  - captured
```

You don't need to reoboot to see the GUI changes, a reload is sufficient. And if all goes will see a card that looks like this:

![Aarlo Glance](/images/aarlo-glance-02.png)

Reading from left to right you have the camera name, motion detection indicator, captured clip indicator, battery levels, signal level and current state. If you click the captured clip icon the last video will play directly on the card. (The video streams directly from Arlo which solves some weird speed issues I was seeing.)

See the [Lovelace Custom Card](https://developers.home-assistant.io/docs/en/lovelace_custom_card.html) page for further information.

## To Do

* turn cameras on/off
* custom mode - like SmartThings to better control motion detection
* live streaming???
* last-seen custom format

