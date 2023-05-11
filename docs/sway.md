# sway


You may combine output commands into one, like so:

    output HDMI-A-1 mode 1920x1080 pos 1920 0 bg ~/wallpaper.png stretch

You can get a list of output names with swaymsg -t get_outputs. You may also match any
output by using the output name "*". Additionally, "-" can be used to match the focused
output by name and "--" can be used to match the focused output by its identifier.

Some outputs may have different names when disconnecting and reconnecting. To identify
these, the name can be substituted for a string consisting of the make, model and serial
which you can get from swaymsg -t get_outputs. Each value must be separated by one space.
For example:

    output "Some Company ABC123 0x00000000" pos 1920 0

```sh
swaymsg -t get_outputs
```
### output <name> mode|resolution|res [--custom] <WIDTHxHEIGHT>[@<RATE>[Hz]]
    Configures the specified output to use the given mode. Modes are a combination of
    width and height (in pixels) and a refresh rate that your display can be configured to
    use. For a list of available modes for each output, use swaymsg -t get_outputs.

    To set a custom mode not listed in the list of available modes, use --custom. You
    should probably only use this if you know what you're doing.

    Examples:

        output HDMI-A-1 mode 1920x1080

        output HDMI-A-1 mode 1920x1080@60Hz

### output <name> position|pos <X> <Y>
    Places the specified output at the specific position in the global coordinate space.
    The cursor may only be moved between immediately adjacent outputs. If scaling is
    active, it has to be considered when positioning. For example, if the scaling factor
    for the left output is 2, the relative position for the right output has to be divided
    by 2.  The reference point is the top left corner so if you want the bottoms aligned
    this has to be considered as well.

    Example:

        output HDMI1 scale 2

        output HDMI1 pos 0 1020 res 3200x1800

        output eDP1 pos 1600 0 res 1920x1080

    Note that the left x-pos of eDP1 is 1600 = 3200/2 and the bottom y-pos is 1020 + (1800
    / 2) = 1920 = 0 + 1920

### output <name> scale <factor>
    Scales the specified output by the specified scale factor. An integer is recommended,
    but fractional values are also supported. If a fractional value are specified, be
    warned that it is not possible to faithfully represent the contents of your windows -
    they will be rendered at the next highest integer scale factor and downscaled. You may
    be better served by setting an integer scale factor and adjusting the font size of
    your applications to taste. HiDPI isn't supported with Xwayland clients (windows will
    blur).

### output <name> scale_filter linear|nearest|smart
    Indicates how to scale application buffers that are rendered at a scale lower than the
    output's configured scale, such as lo-dpi applications on hi-dpi screens. Linear is
    smoother and blurrier, nearest (also known as nearest neighbor) is sharper and
    blockier. Setting "smart" will apply nearest scaling when the output has an integer
    scale factor, otherwise linear. The default is "smart".

### output <name> subpixel rgb|bgr|vrgb|vbgr|none
    Manually sets the subpixel hinting for the specified output. This value is usually
    auto-detected, but some displays may misreport their subpixel geometry. Using the
    correct subpixel hinting allows for sharper text.  Incorrect values will result in
    blurrier text. When changing this via swaymsg, some applications may need to be
    restarted to use the new value.

### output <name> background|bg <file> <mode> [<fallback_color>]
    Sets the wallpaper for the given output to the specified file, using the given scaling
    mode (one of "stretch", "fill", "fit", "center", "tile"). If the specified file cannot
    be accessed or if the image does fill the entire output, a fallback color may be
    provided to cover the rest of the output.  fallback_color should be specified as
    #RRGGBB. Alpha is not supported.

### output <name> background|bg <color> solid_color
    Sets the background of the given output to the specified color. color should be
    specified as #RRGGBB. Alpha is not supported.

### output <name> transform <transform> [clockwise|anticlockwise]
    Sets the background transform to the given value. Can be one of "90", "180", "270" for
    rotation; or "flipped", "flipped-90", "flipped-180", "flipped-270" to apply a rotation
    and flip, or "normal" to apply no transform. If a single output is chosen and a
    rotation direction is specified (clockwise or anticlockwise) then the transform is
    added or subtracted from the current transform.

### output <name> disable|enable
    Enables or disables the specified output (all outputs are enabled by default).

### output <name> toggle
    Toggle the specified output.

### output <name> dpms on|off
    Enables or disables the specified output via DPMS. To turn an output off (ie. blank
    the screen but keep workspaces as-is), one can set DPMS to off.

### output <name> max_render_time off|<msec>
    When set to a positive number of milliseconds, enables delaying output rendering to
    reduce latency. The rendering is delayed in such a way as to leave the specified
    number of milliseconds before the next presentation for rendering.

    The output rendering normally takes place immediately after a presentation (vblank,
    buffer flip, etc.) and the frame callbacks are sent to surfaces immediately after the
    rendering to give surfaces the most time to draw their next frame. This results in
    slightly below 2 frames of latency between the surface rendering and committing new
    contents, and the contents being shown on screen, on average. When the output
    rendering is delayed, the frame callbacks are sent immediately after presentation, and
    the surfaces have a small timespan (1 / (refresh rate) - max_render_time) to render
    and commit new contents to be shown on the next presentation, resulting in below 1
    frame of latency.

    To set this up for optimal latency:
    1.   Launch some full-screen application that renders continuously, like glxgears.
    2.   Start with max_render_time 1. Increment by 1 if you see frame drops.

    To achieve even lower latency, see the max_render_time surface property in sway(5).

    Note that this property has an effect only on backends which report the presentation
    timestamp and the predicted output refresh rate—the DRM and the Wayland backends.
    Furthermore, under the Wayland backend the optimal max_render_time value may vary
    based on the parent compositor rendering timings.

.config/sway/config.d/output.conf
```
output DP-1 resolution 3440x1440@144Hz position 0,0 adaptive_sync off
output DP-4 resolution 2560x1440@59.951Hz transform 270 position 3440,0
```

.config/sway/definitions.d/custom.conf
```
set $idle_timeout 240
set $locking_timeout 1200
set $screen_timeout 1200
set $swayidle swayidle -w \
    timeout $idle_timeout 'light -G > /tmp/brightness && light -S 10' resume 'light -S $([ -f /tmp/brightness ] && cat /tmp/brightness || echo 100%)' \
    timeout $locking_timeout 'exec $locking' \
    timeout $screen_timeout 'swaymsg "output * dpms off"' \
    resume 'swaymsg "output * dpms on"' \
    before-sleep 'playerctl pause' \
    before-sleep 'exec $locking'
```


`.config/waybar/config.jsonc`
```json
// =============================================================================
//
// Waybar configuration
//
// Configuration reference: https://github.com/Alexays/Waybar/wiki/Configuration
//
// =============================================================================

{
    "include": [
        "/usr/share/sway/templates/waybar/config.jsonc"
    ],
    // -------------------------------------------------------------------------
    // Global configuration
    // -------------------------------------------------------------------------

    "layer": "top",

    // If height property would be not present, it'd be calculated dynamically
    "height": 30,
    "position": "top",

    "modules-left": ["custom/menu", "sway/workspaces", "custom/scratchpad"],
    "modules-center": ["custom/wf-recorder", "sway/mode", "custom/weather"],
    "modules-right": [
        // informational
        "sway/language",
        "custom/github",
        "custom/clipboard",
        "custom/zeit",
        "cpu",
        "memory",
        "battery",
        "temperature",

        // connecting
        "network",
        "bluetooth",

        // media
        "custom/playerctl",
        "idle_inhibitor",
        "custom/dnd",
        "pulseaudio",
        "backlight",

        // system
        "custom/adaptive-light",
        "custom/sunset",
        "custom/pacman",

        "tray",
        "clock"
    ],

    // -------------------------------------------------------------------------
    // Modules
    // -------------------------------------------------------------------------

    "battery": {
        "interval": 30,
        "states": {
            "warning": 30,
            "critical": 15
        },
        "format-charging": " {capacity}%",
        "format": "{icon} {capacity}%",
        "format-icons": ["", "", "", "", "", ""],
        "tooltip": true
    },

    "clock": {
        "interval": 60,
        "format": "{:%e %b %Y %H:%M}",
        "tooltip": true,
        "tooltip-format": "<big>{:%B %Y}</big>\n<tt>{calendar}</tt>",
        "on-click": "swaymsg exec \\$calendar"
    },

    "cpu": {
        "interval": 5,
        "format": "﬙ {usage}%",
        "states": {
            "warning": 70,
            "critical": 90
        },
        "on-click": "swaymsg exec \\$term_float htop"
    },

    "memory": {
        "interval": 5,
        "format": " {}%",
        "states": {
            "warning": 70,
            "critical": 90
        },
        "on-click": "swaymsg exec \\$term_float htop"
    },

    "network": {
        "interval": 5,
        "format-wifi": " ",
        "format-ethernet": "",
        "format-disconnected": "睊",
        "tooltip-format": "{ifname} ({essid}): {ipaddr}",
        "on-click": "swaymsg exec \\$term_float nmtui"
    },

    "sway/mode": {
        "format": "<span style=\"italic\">{}</span>",
        "tooltip": false
    },

    "idle_inhibitor": {
        "format": "{icon}",
        "format-icons": {
            "activated": "零",
            "deactivated": "鈴"
        },
        "tooltip": true,
        "tooltip-format-activated": "power-saving disabled",
        "tooltip-format-deactivated": "power-saving enabled"
    },

    "backlight": {
        "format": "{icon} {percent}%",
        "format-icons": ["", "", ""],
        "on-scroll-up": "swaymsg exec \\$brightness_up",
        "on-scroll-down": "swaymsg exec \\$brightness_down"
    },

    "pulseaudio": {
        "scroll-step": 5,
        "format": "{icon} {volume}%{format_source}",
        "format-muted": "婢 {format_source}",
        "format-source": "",
        "format-source-muted": " ",
        "format-icons": {
            "headphone": "",
            "headset": "",
            "default": ["奄", "奔", "墳"]
        },
        "tooltip-format": "{icon} {volume}% {format_source}",
        "on-click": "swaymsg exec \\$pulseaudio",
        "on-click-middle": "swaymsg exec \\$volume_mute",
        "on-scroll-up": "swaymsg exec \\$volume_up",
        "on-scroll-down": "swaymsg exec \\$volume_down"
    },

    "temperature": {
        "critical-threshold": 90,
        "interval": 5,
        "format": "{icon} {temperatureC}°",
        "format-icons": ["", "", ""],
        "tooltip": false,
        "on-click": "swaymsg exec \"\\$term_float watch sensors\""
    },

    "tray": {
        "icon-size": 21,
        "spacing": 5
    },

    "custom/pacman": {
        "format": " {}",
        "interval": 3600,
        "exec-if": "[ $(pamac checkupdates -q | wc -l) -gt 0 ]",
        "exec": "pamac checkupdates -q | wc -l",
        "on-click": "pamac-manager --updates; pkill -RTMIN+4 waybar",
        "signal": 4
    },

    "custom/menu": {
        "format": "",
        "on-click": "swaymsg exec \\$menu",
        "tooltip": false
    },

    "bluetooth": {
        "format": "",
        "format-disabled": "",
        "on-click": "swaymsg exec \\$bluetooth",
        "on-click-right": "rfkill toggle bluetooth",
        "tooltip-format": "{}"
    },

    "sway/language": {
        "format": " {}",
        "min-length": 5,
        "tooltip": false,
        "on-click": "swaymsg input $(swaymsg -t get_inputs --raw | jq '[.[] | select(.type == \"keyboard\")][0] | .identifier') xkb_switch_layout next"
    },

    "custom/scratchpad": {
        "interval": "once",
        "return-type": "json",
        "format": "{icon}",
        "format-icons": {
            "one": "类",
            "many": "缾"
        },
        "exec": "/bin/sh /usr/share/sway/scripts/scratchpad.sh",
        "on-click": "swaymsg 'scratchpad show'",
        "signal": 7
    },

    "custom/sunset": {
        "interval": "once",
        "tooltip": true,
        "return-type": "json",
        "format": "{icon}",
        "format-icons": {
            "on": "",
            "off": ""
        },
        "exec": "fallback_latitude=50.1 fallback_longitude=8.7 latitude= longitude= /usr/share/sway/scripts/sunset.sh",
        "on-click": "/usr/share/sway/scripts/sunset.sh toggle; pkill -RTMIN+6 waybar",
        "exec-if": "/usr/share/sway/scripts/sunset.sh check",
        "signal": 6
    },

    "custom/wf-recorder": {
        "interval": "once",
        "return-type": "json",
        "format": "{}",
        "tooltip-format": "{tooltip}",
        "exec": "echo '{\"class\": \"recording\",\"text\":\"雷\",\"tooltip\":\"press $mod+Esc to stop recording\"}'",
        "exec-if": "pgrep wf-recorder",
        "on-click": "killall -s SIGINT wf-recorder",
        "signal": 8
    },

    "custom/github": {
        "interval": 300,
        "tooltip": false,
        "return-type": "json",
        "format": " {}",
        "exec": "gh api '/notifications' -q '{ text: length }' | cat -",
        "exec-if": "[ -x \"$(command -v gh)\" ] && gh auth status 2>&1 | grep -q -m 1 'Logged in' && gh api '/notifications' -q 'length' | grep -q -m 1 '0' ; test $? -eq 1",
        "on-click": "xdg-open https://github.com/notifications && sleep 30 && pkill -RTMIN+4 waybar",
        "signal": 4
    },

    "custom/playerctl": {
        "interval": "once",
        "tooltip": true,
        "return-type": "json",
        "format": "{icon}",
        "format-icons": {
            "Playing": "",
            "Paused": "奈"
        },
        "exec": "playerctl metadata --format '{\"alt\": \"{{status}}\", \"tooltip\": \"{{playerName}}:  {{markup_escape(title)}} - {{markup_escape(artist)}}\" }'",
        "on-click": "playerctl play-pause; pkill -RTMIN+5 waybar",
        "on-click-right": "playerctl next; pkill -RTMIN+5 waybar",
        "on-scroll-up": "playerctl position 10+; pkill -RTMIN+5 waybar",
        "on-scroll-down": "playerctl position 10-; pkill -RTMIN+5 waybar",
        "signal": 5
    },

    "custom/clipboard": {
        "format": "",
        "interval": "once",
        "return-type": "json",
        "on-click": "swaymsg -q exec '$clipboard'; pkill -RTMIN+9 waybar",
        "on-click-right": "swaymsg -q exec '$clipboard-del'; pkill -RTMIN+9 waybar",
        "on-click-middle": "rm -f ~/.cache/cliphist/db; pkill -RTMIN+9 waybar",
        "exec": "printf '{\"tooltip\":\"%s\"}' $(cliphist list | wc -l)' item(s) in the clipboard\r(Mid click to clear)'",
        "exec-if": "[ -x \"$(command -v cliphist)\" ] && [ $(cliphist list | wc -l) -gt 0 ]",
        "signal": 9
    },

    "custom/weather": {
        "icon-size": 42,
        "format": "{icon} {}",
        "tooltip": true,
        "interval": 3600,
        // accepts -c/--city <city> -t/--temperature <C/F> -d/--distance <km/miles>
        "exec": "/usr/share/sway/scripts/weather.py -c sg",
        "return-type": "json",
        "format-icons": {
            "Unknown": "",
            "Cloudy": "摒",
            "Fog": "",
            "HeavyRain": "",
            "HeavyShowers": "",
            "HeavySnow": "",
            "HeavySnowShowers": "ﰕ",
            "LightRain": "",
            "LightShowers": "",
            "LightSleet": "",
            "LightSleetShowers": "",
            "LightSnow": "",
            "LightSnowShowers": "ﭽ",
            "PartlyCloudy": "",
            "Sunny": "",
            "ThunderyHeavyRain": "ﭼ",
            "ThunderyShowers": "",
            "ThunderySnowShowers": "",
            "VeryCloudy": ""
        }
    },

    "custom/zeit": {
        "return-type": "json",
        "interval": "once",
        "format": "{icon}",
        "format-icons": {
            "tracking": "華",
            "stopped": ""
        },
        "exec": "/bin/sh /usr/share/sway/scripts/zeit.sh status",
        "on-click": "/bin/sh /usr/share/sway/scripts/zeit.sh click; pkill -RTMIN+10 waybar",
        "exec-if": "[ -x \"$(command -v zeit)\" ]",
        "signal": 10
    },

    "custom/dnd": {
        "interval": "once",
        "return-type": "json",
        "format": "{}{icon}",
        "format-icons": {
            "default": "",
            "dnd": "ﮡ"
        },
        "on-click": "makoctl mode | grep 'do-not-disturb' && makoctl mode -r do-not-disturb || makoctl mode -a do-not-disturb; pkill -RTMIN+11 waybar",
        "on-click-right": "makoctl restore",
        "exec": "printf '{\"alt\":\"%s\",\"tooltip\":\"mode: %s\"}' $(makoctl mode | grep -q 'do-not-disturb' && echo dnd || echo default) $(makoctl mode | tail -1)",
        "signal": 11
    },

    "custom/adaptive-light": {
        "interval": "once",
        "tooltip": true,
        "return-type": "json",
        "format": "{icon}",
        "format-icons": {
            "on": "",
            "off": ""
        },
        "exec": "/usr/share/sway/scripts/wluma.sh",
        "on-click": "/usr/share/sway/scripts/wluma.sh toggle; pkill -RTMIN+12 waybar",
        "exec-if": "/usr/share/sway/scripts/wluma.sh check",
        "signal": 12
    }
}

```