# kb port versus the original Temper keymap

Baseline: `config/temper.keymap` at Temper commit `9f46806`, preserved on
[`backup/pre-kb-port-2026-11-02`](https://github.com/kon-angelo/temper-zmkstudio/tree/backup/pre-kb-port-2026-11-02).
The new source is `config/urchin.keymap` from `kon-angelo/urchin-zmk-firmware`
(`kb`). This comparison uses the original Temper layout, not the intermediate
kb2/Sofle port.

## Behaviors

| Area | Original Temper | kb-based Temper |
| --- | --- | --- |
| Modifier placement | Mainly home-row mods: GUI/Alt/Ctrl/Shift | Bottom-row mods, including Shift on M and GUI on comma |
| Modifier hold-taps | `u_mt`: tap-preferred, 200 ms; no positional or prior-idle rules | `homerow_left`: balanced, 350 ms, 100 ms prior idle; `homerow_right`: balanced, 280 ms, 150 ms prior idle |
| Layer hold-taps | `u_lt`: tap-preferred, 200 ms | `tap_left`: balanced, 280 ms, no prior-idle requirement; strict variant: tap-preferred, 260/100 ms; `master_key`: tap-preferred, 350/100 ms |
| Positional holds | No hand restrictions | Hand-specific triggers and `hold-trigger-on-release`; master thumbs accept all 30 finger positions |
| Layer switching | Ten double-tap dances; a single tap does nothing, double tap switches layers | Direct holds/toggles and combos; dedicated Mouse, Numpad, FN and Nav locked layers survive release of their original holds |
| Sticky modifiers | No custom sticky-key setup | `sk`: lazy + quick-release, 1-second timeout, retains ignore-modifiers; `sk2`: quick-release + ignore-modifiers, 1.5-second timeout |
| Bluetooth | Shift-sensitive profile behaviors: select normally, select-and-clear while shifted | Direct selection on System, separate clear-current-profile key, extra thumb cycles profiles |
| Caps Word | Mod-morph: Caps Word normally, Caps Lock with Shift | Plain Caps Word on the added Master outer thumb |
| Mouse | Keypad direction codes, mouse clicks on thumbs | Actual pointer movement and scrolling, with kb's default speed/acceleration; clicks on M/comma/period |

Balanced hold-taps can resolve as holds during an interrupting key press/release;
tap-preferred behavior waits for the tapping term. The positional restrictions
and prior-idle requirements in kb help distinguish intentional holds from typing.
The exact feel therefore changes as well as the numerical tapping terms.

### Tap-preferred versus balanced for letter-key layers

For S/D/F, **balanced is the current setting**:
an opposite-hand key press and release can activate the layer before the 280 ms
tapping term expires. Positional rules help distinguish these holds from typing.

**Tap-preferred favors typing accuracy over quick layer chords**: other keys
do not trigger an early hold, so an intentional layer hold normally needs the
full tapping term. It can help if nested typing sequences still cause accidental
layer activation. Neither flavor is universally better. The latest tuning uses
tap-preferred for the strict E/R/G holds (260 ms, 100 ms prior idle) and the
Enter/Space thumb holds (350 ms, 100 ms prior idle). Bottom-row modifiers are
balanced at 350/280 ms, retaining positional/prior-idle safeguards. The Sym-layer
Ctrl/Backspace binding also uses the right-hand modifier behavior.

There are **19 declared custom behaviors** in the original and **9** in the kb
port. Of the latter, `qt`, `tap_right`, and `macro_layers` are currently unbound;
the `&mt` override is also unused by the supplied bindings. These definitions are
retained from kb for editor customization. The original likewise declared some
unused actions, including `to_button` and profile 4's `bt_4` behavior.

Temper adds one outer thumb to each hand. The opposite-hand trigger sets include
that extra thumb; kb's four existing thumb bindings map from positions 30–33 to
31–34. Temper's modifier and strict/thumb hold-tap settings have been tuned
independently of kb, as shown above.

## Combos

Original Temper has **5 combos**, all on Base:

| Keys in original Base | Action | Timeout |
| --- | --- | --- |
| Q + W | Escape | 100 ms |
| A + quote | Caps Lock | Default (50 ms) |
| comma + period | Semicolon | Default (50 ms) |
| L + quote | Minus | 150 ms |
| Q + W + E | Alt+F4 | Default (50 ms) |

The port adds J+K to return to Base on every layer except Base and Sym, plus
Base-only R+E / T+E bracket chords (35 ms timeout, 150 ms prior idle) to reduce
accidental activation while typing. The port corrects the Media toggle target
and scopes the duplicate modifier and alternate Mouse combos to their intended
layers. The inherited combos retain kb's timing and positions. Below, keys are identified by their
positions on the new Base layer; the same positions apply on other layers.
“All” means there is no layer restriction. A dash under idle means none is set.

| Combo | Action | Layers | Timeout / prior idle (ms) |
| --- | --- | --- | --- |
| J + K | Escape | Base | 50 / 150 |
| J + K | Return to Base | All except Base and Sym (2–13) | 50 / — |
| I + O | Ctrl+Space | Base | 50 / 350 |
| W + S + X | Toggle System | Base, System | 50 / 250 |
| Q + W + E + R | Return to Base | All | 50 / — |
| W + E | Hold FN | Base, FN | 30 / 280 |
| W + E + R | Toggle FN | Base, FN | 30 / 200 |
| D + F + G | Toggle Mouse | Base, Mouse | 80 / 200 |
| V + B | Hold Media | Base, Media | 30 / 280 |
| E + R + T | Toggle Numpad | Base, Numpad | 30 / 200 |
| H + J | Tab | Base, Sym, Numpad, Numpad Locked | 100 / 30 |
| O + L + period | Toggle System | Base, System | 50 / — |
| P + Backspace + slash | Studio unlock | Base | 50 / 300 |
| X + C | Hold Mouse | Base | 50 / 280 |
| C + V + B (`media_tog`) | Toggle Media | Base, Media | 50 / 280 |
| M + comma + period (`altgui`) | Sticky Alt+GUI | Base | 100 / 280 |
| M + comma + period (`alt_ctrl_gui`) | Sticky Alt+Ctrl+GUI | Master | 50 / — |
| C + V | Hold Mouse | Base | 50 / — |
| U + I | Enter | Base | 50 / 280 |
| H + U | Left bracket | Base | 50 / 280 |
| J + I | Right bracket | Base | 50 / 250 |
| R + E | Left bracket | Base | 35 / 150 |
| T + E | Right bracket | Base | 35 / 150 |
| Y + U | Backspace | Base, Sym | 50 / 250 |

### Corrections applied after comparison

1. **Duplicate modifier combo:** kb's `altgui` and `meh` both applied on Base
   at M/comma/period. `altgui` stays on Base; `meh` is renamed `alt_ctrl_gui`
    to match its actual modifiers and scoped to Master (2). Their layer scopes
   are now disjoint.
2. **Media toggle:** `media_tog` uses `&tog 8` (Media), matching its existing
   Base/Media layer filter, rather than toggling Mouse (7).
3. **N's modifier hold:** N now uses `homerow_right`, matching its physical hand,
   the other right-hand keys' timing, and opposite-hand trigger positions.
4. **Alternate Mouse hold:** C+V (`mouse2`) is limited to Base (0), so it no
   longer intercepts that chord on unrelated layers.

The layer-return macros were also checked: Base is layer 0, so `spc_to_0` and
`enter_to_0` already target the correct layer. `shifted` and `unstick` do not
switch layers.

## Macros

The original declares **5 Bluetooth macros**, `bt_0_clear` through `bt_4_clear`.
Each selects its profile, then clears its pairing, with `wait-ms = <0>`; the
Shift-sensitive profile behaviors invoke these. Only profiles 0–3 are actually
bound on the original Media layer.

kb instead has **4 macros**, copied without behavioral changes:

| Macro | Action |
| --- | --- |
| `unstick` | Taps all eight left/right modifier keys to recover from a stuck-modifier state |
| `shifted` | Holds left Shift, taps its keycode parameter, then releases Shift |
| `spc_to_0` | Returns to Base and sends Space |
| `enter_to_0` | Returns to Base and sends Enter |

These macros use ZMK's default macro timing. Pair clearing is now a separate
`&bt BT_CLR` binding on System; it clears the currently selected host profile.
Select profile 0/1/2 with System+T/G/B, then use System+R to clear it. This is
functionally equivalent to the old select-and-clear macros; the difference is
two button presses instead of a single Shift-modified profile action.

## Temper-specific additions

- The outer-thumb bindings are listed in the [README](../README.md#temper-adaptation).
  They provide Mouse/Nav on Base, editing keys, numeric operators,
  exits, Caps Word, media controls, and profile cycling.
- Numpad and FN use **E / R** holds and have dedicated
  locked layers (11/12), entered with the left inner thumb while the ordinary
  layer is active. That thumb exits the locked layer, just like Mouse Locked.
- Nav Locked occupies index 13, entered with Nav's left inner thumb. Nav is
  reached by holding F or the right outer thumb. Both inner left thumbs provide
  Shift while locked.
- Numpad Locked, FN Locked, and Nav Locked use plain Enter and Space on the right inner/middle
  thumbs, keeping the layer active. The right outer thumb and J+K return to Base.
- Mouse Locked's right thumbs send MB2 / MB1 / MB3 from inner to outer, supporting
  right-click, left-click, and middle-click (including holds/drags). J+K or the
  left inner thumb returns to Base.
- System is 9, Mouse Locked 10, Numpad Locked 11, and FN Locked 12.
  The current layer list is in the [README](../README.md#temper-adaptation).
- Bluetooth supports **three host profiles**. The central's connection and
  pairing limits are each 4 to include the right half; the peripheral retains
  one slot. Host profiles 0–2 are selected with System+T/G/B.
- Studio locking is disabled in the left build. Original Temper required the
  Nav-layer unlock binding; the new firmware can connect directly.

The old bootloader shortcut is **hold Space (left-middle thumb), then Q**.
The new shortcut is **toggle System with W + S + X, then press A**.
