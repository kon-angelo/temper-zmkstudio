
# Temper custom split ergo keyboard software

Based on [temper](https://github.com/raeedcho/temper), which is itself a
continuation of [chocofi](https://github.com/pashutk/chocofi/).

## Firmware

The firmware targets nRF52840 Pro Micro-compatible controllers using ZMK. A
GitHub Actions workflow builds separate UF2 files for the left and right halves.

## Configuring the keymap

The active [`config/temper.keymap`](config/temper.keymap) is plain ZMK
devicetree, ported from `config/urchin.keymap` in
[`urchin-zmk-firmware` (kb)](https://github.com/kon-angelo/urchin-zmk-firmware).
Urchin's 30 finger keys map directly to Temper; its four thumbs occupy Temper
positions 31–34. The port uses kb's bottom-row modifiers, positional layer
holds, macros, combo timing, and dedicated locked layers, including kb v0.2.8's
Nav Locked layer and revised Sym bindings, with corrected combo
targets/scopes, N's right-hand hold behavior, and tap-preferred modifier holds.
The same firmware source can be edited with either editor below.

See [the comparison with the original Temper keymap](docs/keymap-comparison.md)
for behavior, combo, and macro differences and the fixes applied to kb's layout.

### Temper adaptation

The base thumb keys, ordered from left to right, are:

| Thumb | Tap / press | Hold |
| --- | --- | --- |
| Left outer | System layer | System layer |
| Left middle | Sticky Shift | Shift |
| Left inner | Symbols layer | Symbols layer |
| Right inner | Enter | Symbols layer |
| Right middle | Space | Master layer |
| Right outer | Original Temper Symbols layer | Original Temper Symbols layer |

On Base, holding **T / R** accesses **Numpad / FN**, and holding **S / D / F / G**
accesses **Vi / Master / Nav / Mouse**, using kb's positional hold rules and
timing. Backspace is at the right end of the home row. Symbols provides the
number row, and FN provides F1–F12.

Bottom-row modifier holds are **tap-preferred**, with a **350 ms** tapping term
on the left and **280 ms** on the right. The positional and prior-idle rules
remain in place. The Sym-layer Ctrl/Backspace binding shares the right-hand
behavior. Letter-key layer holds and Enter/Space thumb holds remain **balanced**.

Temper's two additional outer thumbs have these per-layer actions:

| Layer | Left outer thumb | Right outer thumb |
| --- | --- | --- |
| Base | Hold System | Hold original Temper Symbols |
| Sym | Hold Shifted | Backspace |
| Shifted | Transparent (keeps the Sym-layer hold) | Delete |
| Master | Caps Word | Escape |
| Vi | Escape | Enter |
| Numpad | Minus | Plus |
| FN | Escape | Return to Base |
| Nav | Tab | Delete |
| Mouse | GUI / Command | Return to Base |
| Media | Stop | Play/pause |
| System | Next Bluetooth profile | Return to Base |
| Mouse Locked | GUI / Command | Return to Base |
| Numpad Locked | Minus | Plus |
| FN Locked | Escape | Return to Base |
| Nav Locked | Tab | Delete |
| Symbols | Left parenthesis | Transparent (keeps the Base-layer hold) |

On **Mouse, Numpad, or FN**, press the **left inner thumb** to enter that layer's
dedicated locked copy. It stays active after releasing the original G/T/R hold;
press the left inner thumb again to return to Base. Numpad's sticky Shift is on
the left middle thumb. Mouse and Numpad retain their Enter/Space return macros;
FN's right thumbs return directly to Base.

On **Nav**, the left inner thumb enters **Nav Locked**. As in kb v0.2.8, both
inner left thumbs provide Shift while locked; the right inner thumb returns to
Base and sends Enter, and the right middle thumb returns to Base.

The **right outer thumb** opens a second symbol layout copied from the original
Temper/Miryoku keymap: symbol keys on the left (`{ & * ( }`, `: $ % ^ +`,
`~ ! @ # |`), modifiers on the right, and `(` / `)` / `_` on the left thumbs.
The original kb **Sym** and **Shifted** layers remain accessible as before.

Frequently used combos (key names refer to their Base-layer positions):

| Combo | Action |
| --- | --- |
| J + K | Escape |
| U + I | Enter |
| H + J | Tab |
| Y + U | Backspace |
| H + U / J + I | Left / right bracket |
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

Hold the **left outer thumb** on Base for System: **T / G / B** select Bluetooth
profiles **0 / 1 / 2**, **R** clears the current pairing, and **I** invokes the
modifier-reset macro. **Q / A / P** or the home-row **Backspace** key enters the
bootloader. The **Z / slash** keys retain kb's manual Studio unlock action.
To clear a specific host pairing, select it with **System+T/G/B**, then press
**System+R**. This performs the same selection-and-clear sequence as the old
profile-clear macros, using two button presses.

Layer indices are aligned with kb through Nav Locked: Base (0), Sym (1),
Shifted (2), Master (3), Vi (4), Numpad (5), FN (6), Nav (7), Mouse (8), Media (9),
System (10), Mouse Locked (11), Numpad Locked (12), FN Locked (13), and
Nav Locked (14). Original Temper Symbols occupies layer 15. Mod has been removed.

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
