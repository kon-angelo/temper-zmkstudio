
# Temper custom split ergo keyboard software

Based on [temper](https://github.com/raeedcho/temper), which is itself a
continuation of [chocofi](https://github.com/pashutk/chocofi/).

## Firmware

The firmware targets nRF52840 Pro Micro-compatible controllers using ZMK. A
GitHub Actions workflow builds separate UF2 files for the left and right halves.

### Build locally

Start Docker Desktop, then run from this repository:

```sh
make firmware
```

This uses the same ZMK build image and `build.yaml` matrix as GitHub Actions,
including your local keymap edits. It builds all three targets and saves them
to the gitignored `firmware/` folder in this repository:

- `temper-left-niceview-bongo.uf2` — left/central, with ZMK Studio
- `temper-right-niceview-status.uf2` — right/peripheral
- `settings-reset.uf2` — settings-reset image

The first run downloads ZMK and its dependencies. Later runs reuse the
`temper-zmkstudio-build` Docker volume and compiler cache, with a pristine build
for each target. ZMK and KeyBeacon are pinned in `config/west.yml`.
Dependencies refresh when that file changes; to explicitly refresh the pinned
dependencies, run:

```sh
make firmware UPDATE=1
```

`ZMK_IMAGE` and `ZMK_VOLUME` can be overridden.

### KeyBeacon on macOS

The left/central build enables KeyBeacon and fetches the right half's battery
level. `config/west.yml` uses the privacy-hardened `kon-angelo/zmk-keybeacon`
fork. Run `make firmware`, then put each half into its UF2 bootloader and copy
the matching `temper-left-niceview-bongo.uf2` / `temper-right-niceview-status.uf2`
onto its mounted drive. The generated `settings-reset.uf2` is a separate
recovery image; it is not part of a normal firmware update.

Connect **FunkeeB_Temper** to the Mac over Bluetooth and launch the app:

```sh
open ~/SAPDevelop/dev/src/github.com/kon-angelo/keybeacon/dist/BleWidget.app
```

Allow Bluetooth access when macOS asks. The app lives in the menu bar; its
floating panel shows layers, modifiers, host/profile state and available battery
readings. Select Temper in the app's keyboard menu if several compatible
keyboards are connected. Installing the app in `/Applications` is optional.

The hardened firmware sends layer/modifier information only to the active
Bluetooth typing host. Other hosts, and all Bluetooth hosts while USB is the
selected typing output, see **Private** with no held modifiers. Battery and
connectivity remain available to encrypted, bonded hosts. Normal firmware
updates preserve pairing; if the new service is not discovered, reconnect the
keyboard and restart the app before considering a re-pair.

## Configuring the keymap

The active [`config/temper.keymap`](config/temper.keymap) is plain ZMK
devicetree, ported from `config/urchin.keymap` in
[`urchin-zmk-firmware` (kb)](https://github.com/kon-angelo/urchin-zmk-firmware).
Urchin's 30 finger keys map directly to Temper; its four thumbs occupy Temper
positions 31–34. The port uses kb's bottom-row modifiers, positional layer
holds, macros, combo timing, and dedicated locked layers, including kb v0.2.8's
Nav Locked layer and revised Sym bindings, with corrected combo
targets/scopes, N's right-hand hold behavior, and tuned hold-tap behaviors.
The same firmware source can be edited with either editor below.

See [the comparison with the original Temper keymap](docs/keymap-comparison.md)
for behavior, combo, and macro differences and the fixes applied to kb's layout.

### Temper adaptation

The base thumb keys, ordered from left to right, are:

| Thumb | Tap / press | Hold |
| --- | --- | --- |
| Left outer | Mouse layer | Mouse layer |
| Left middle | Sticky Shift | Shift |
| Left inner | Sym layer | Sym layer |
| Right inner | Enter | Sym layer |
| Right middle | Space | Master layer |
| Right outer | Nav layer | Nav layer |

On Base, holding **E / R** accesses **Numpad / FN**, and holding **S / D / F / G**
accesses **Vi / Master / Nav / Mouse**, using positional hold rules and the
timing below. Backspace is at the right end of the home row. Sym provides the
number row, and FN provides F1–F12.

Bottom-row modifier holds are **balanced**, with a **350 ms** tapping term
on the left and **280 ms** on the right. The positional and prior-idle rules
remain in place. The Sym-layer Ctrl/Backspace binding shares the right-hand
behavior. S/D/F layer holds are **balanced** (280 ms). The strict E/R/G layer
holds are **tap-preferred** (260 ms, 100 ms prior idle), and the Enter/Space
thumb holds are **tap-preferred** (350 ms, 100 ms prior idle).

Temper's two additional outer thumbs have these per-layer actions:

| Layer | Left outer thumb | Right outer thumb |
| --- | --- | --- |
| Base | Hold Mouse | Hold Nav |
| Sym | `&mo 0` | Backspace |
| Master | Caps Word | Escape |
| Vi | Escape | Enter |
| Numpad | Minus | Plus |
| FN | Escape | Return to Base |
| Nav | Tab | Delete |
| Mouse | GUI / Command | Return to Base |
| Media | Stop | Play/pause |
| System | Next Bluetooth profile | Return to Base |
| Mouse Locked | GUI / Command | Middle-click (MB3) |
| Numpad Locked | None | Return to Base |
| FN Locked | Escape | Return to Base |
| Nav Locked | Tab | Return to Base |

On **Mouse, Numpad, or FN**, press the **left inner thumb** to enter that layer's
dedicated locked copy. It stays active after releasing the original G/E/R hold;
press the left inner thumb again to return to Base. Numpad's sticky Shift is on
the left middle thumb.

Hold **F** or the **right outer thumb** to activate **Nav**, then tap the
**left inner thumb** to enter **Nav Locked**. Release the Nav hold to keep
navigating with the same arrow, page, Home/End, and bracket shortcuts. Both inner
left thumbs provide Shift while locked.

On **Numpad Locked, FN Locked, and Nav Locked**, the right thumbs are **Enter /
Space / Return to Base**, ordered from inner to outer. Enter and Space keep the layer locked.
Press the **right outer thumb** or **J + K** to return to Base.

On **Mouse Locked**, the right thumbs are **right-click (MB2) / left-click (MB1) /
middle-click (MB3)**, ordered from inner to outer. Hold a thumb to hold that mouse
button, including for dragging. Return to Base with **J + K** or the **left inner
thumb**.

Frequently used combos (key names refer to their Base-layer positions):

| Combo | Action |
| --- | --- |
| J + K on Base | Escape |
| J + K on any layer except Base or Sym | Return to Base (`&to 0`) |
| U + I | Enter |
| H + J | Tab |
| Y + U | Backspace |
| H + U / J + I | Left / right bracket |
| R + E / T + E on Base | Left / right bracket (`[` / `]`) |
| I + O | Ctrl+Space |
| W + E / W + E + R | Hold / toggle FN |
| X + C or C + V | Hold Mouse |
| D + F + G | Toggle Mouse |
| V + B | Hold Media |
| C + V + B | Toggle Media |
| E + R + T | Toggle Numpad |
| W + S + X or O + L + period | Toggle System |
| M + comma + period on Base | Sticky Alt+GUI |
| M + comma + period on Master | Sticky Alt+Ctrl+GUI |
| Q + W + E + R | Return to Base from any layer |

The **R + E / T + E** bracket combos require the two keys to be pressed within
**35 ms**, following at least **150 ms** without a non-modifier key press.
This favors deliberate chords over ordinary `re` / `te` typing sequences.

Press **W + S + X** on Base to toggle System: **T / G / B** select Bluetooth
profiles **0 / 1 / 2**, **R** clears the current pairing, and **I** invokes the
modifier-reset macro. **Q / A / P** or the home-row **Backspace** key enters the
bootloader. The **Z / slash** keys retain kb's manual Studio unlock action.
To clear a specific host pairing, select it with **System+T/G/B**, then press
**System+R**. This performs the same selection-and-clear sequence as the old
profile-clear macros, using two button presses.

Current layer indices: Base (0), Sym (1), Master (2), Vi (3), Numpad (4),
FN (5), Nav (6), Mouse (7), Media (8), System (9), Mouse Locked (10),
Numpad Locked (11), FN Locked (12), and Nav Locked (13).

### Bluetooth settings (kb3)

- Advertised name: **FunkeeB_Temper**; left half is central, right half is peripheral.
- Transmit power: **+8 dBm** on both halves, configured in their display-shield `.conf` files.
- Three saved host profiles (**0–2**). The left build sets `CONFIG_BT_MAX_PAIRED=4`
  and `CONFIG_BT_MAX_CONN=4`: three host slots plus one split-peripheral slot.
  The right half uses one pairing/connection slot for the left half.
- ZMK's host connection preferences: **7.5–15 ms** interval, peripheral latency
  **30**, supervision timeout **4 seconds**. The split link requests **7.5 ms**,
  latency **30**, and a **4-second** timeout. Actual intervals are negotiated.
- 2M PHY is enabled; experimental Bluetooth options are disabled.
- Idle timeout is **30 seconds**; automatic deep sleep is disabled.

The connection/profile limits and unlocked Studio setting are in `build.yaml`.

### Nick Coutsos' ZMK Keymap Editor

1. Open [ZMK Keymap Editor](https://nickcoutsos.github.io/keymap-editor/).
2. Choose **GitHub** and authorize this repository, or choose **File System**
   and open `config/temper.keymap` locally.
3. Edit the bindings and save the keymap.
4. Let GitHub Actions build the firmware, then flash the new left-half UF2.

The keyboard geometry used by the editor is stored in `config/info.json`.
Custom hold-taps, macros, combos, Bluetooth profile actions, bootloader bindings,
and the Studio unlock binding are declared directly in the keymap so the editor
can preserve them.

### ZMK Studio

The left/central firmware is built with [ZMK Studio](https://zmk.studio/)
support and **locking disabled** (`CONFIG_ZMK_STUDIO_LOCKING=n`). Connect the
left half over USB and connect from Studio directly. The firmware also enables
Studio's BLE transport. The manual unlock bindings are retained from kb.

ZMK Studio stores runtime keymap changes on the keyboard. Those changes do not
flow back into `config/temper.keymap`. After flashing this port or another
source-keymap update, use **Restore Stock Settings** in ZMK Studio so the newly
flashed keymap becomes active.

## Displays

The left half remains the split central and uses the local `nice_view_bongo`
shield to show a Bongo Cat that reacts to key presses from both halves. The
widget uses the current ZMK/LVGL 9 display API and rotates its portrait UI for
the keyboard's display mounting. The right half uses a matching custom
nice!view screen with a large battery gauge, Bluetooth link state, and a
lengthwise `FunkeeB` wordmark. Connect the left half to the host when using USB
or ZMK Studio. After one minute without a key press, the cat closes its eyes and
displays `Zzzz`; the next key press wakes it immediately. A rolling 16-second
WPM graph fills the space between the status indicators and the bottom-aligned
cat. The seven animation frames are adapted from
[SamIAm2000/zmk](https://github.com/SamIAm2000/zmk) (MIT): they are scaled for
this portrait layout and the flower is removed.
