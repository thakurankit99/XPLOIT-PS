# XPLOIT Dungeon - Patch Report

## Overview

The game binary `xploit.exe` is a PyInstaller-packaged Python 3.10 / Pygame dungeon platformer with 6 stages. Each stage contains a deliberate bug that makes it impossible to complete. Below is the analysis and fix for each.

### Reverse Engineering Methodology

1. Identified the binary as a PyInstaller bundle (MZ header + embedded Python 3.10 modules).
2. Extracted the archive using `pyinstxtractor.py`, recovering `xploit.pyc` (the main game script).
3. Decompiled `xploit.pyc` using Decompyle++ (`pycdc.exe`) to obtain readable Python source.
4. Cross-verified every critical code path against the raw CPython 3.10 bytecode disassembly (`pydisasm` via the `xdis` library) to catch decompiler inaccuracies.
5. Identified 6 distinct bugs (one per stage), wrote minimal patches, and rebuilt the executable.

---

## Stage 1 - Impossible Door Lock

### What was broken

The door object (`_Ox`) requires `p.cn >= 9999` coins to open, but the level only contains **3** collectible coins. The player can never accumulate enough coins to unlock the door.

**Bytecode evidence** (`_Ox._c`, line 108):
```
LOAD_CONST  (9999)
COMPARE_OP  (>=)
```

### How I found it

After decompiling, the `_Ox._c` method clearly showed `if p.cn >= 9999`. Cross-referenced with `_S1.__init__` which creates exactly 3 `_Rx` coin objects.

### Exact change

```python
# BEFORE (line 108 in original):
if p.cn >= 9999:
    self.op = True

# AFTER:
if p.cn >= 3:
    self.op = True
```

### Confirmation

Collected all 3 coins; door changed from "LOCKED" to "OPEN"; walked through to complete Stage 1.

---

## Stage 2 - Impossible Timer

### What was broken

The timed obstacle course gives only **5 seconds** (`self.ts = 5`) to traverse the entire level at a movement speed of **2 pixels/frame** (`_SP = 2`). The total distance is ~865 pixels, requiring ~432 frames = ~7.2 seconds at minimum with zero jumps. With obstacle navigation, 5 seconds is physically impossible.

**Bytecode evidence** (`_S2.__init__`):
```
self.ts = 5    # timer duration in seconds
```

### How I found it

Played the stage; timer expired instantly. Calculated: 865px / 2px per frame / 60fps = 7.2s bare minimum, far exceeding 5s.

### Exact change

```python
# BEFORE:
self.ts = 5

# AFTER:
self.ts = 30
```

### Confirmation

Timer now gives 30 seconds. Navigated the obstacle course and reached the EXIT tile before time expired.

---

## Stage 3 - Missing Bridge

### What was broken

The level has a large void (gap) between platforms at x=150 and x=820. The method `_rdb()` exists to generate bridge platforms across this void, but it is **never called** -- not in `__init__`, not in `_u`, nowhere.

**Bytecode evidence** (`_S3.__init__`):
The `__init__` bytecode creates the left platform, right platform, elevated platform, and exit -- but never invokes `_rdb`. The `_rdb` method itself is valid and correctly populates `self.bp` and `self.pf`.

### How I found it

Decompiled `_S3.__init__` and searched for any call to `_rdb`. Found the method defined but unreferenced. Confirmed in bytecode: no `LOAD_METHOD (_rdb)` anywhere in the class except the method definition itself.

### Exact change

```python
# Added to _S3.__init__, after setting up bp and xb:
self._rdb()
```

### Confirmation

Bridge platforms now span the void. Walked across to the right side and reached the EXIT tile.

---

## Stage 4 - Invincible Boss

### What was broken

The boss entity (`_Gx`) has a `_td` (take damage) method that subtracts damage from HP, then **immediately resets HP to max**:

```python
def _td(self, n):
    self.hp -= n       # take damage
    self.hp = self.mh  # BUG: reset to max health
```

**Bytecode evidence** (`_Gx._td`, lines 139-140):
```
139:  INPLACE_SUBTRACT  →  self.hp -= n
140:  LOAD_ATTR (mh), STORE_ATTR (hp)  →  self.hp = self.mh
```

### How I found it

Shot the boss repeatedly; health bar never decreased. Disassembled `_td` and saw the two consecutive `STORE_ATTR (hp)` instructions -- the second one overwrites the first.

### Exact change

```python
# BEFORE:
def _td(self, n):
    self.hp -= n
    self.hp = self.mh   # REMOVED this line

# AFTER:
def _td(self, n):
    self.hp -= n
```

### Confirmation

Shot the boss 10 times (hp=10, damage=1 per bullet). Boss died, "PROCEED" message appeared. Walked to EXIT tile.

---

## Stage 5 - Unreachable Exit

### What was broken

The exit (`_Ux`) teleports to a random location when the player gets within **50 pixels**. However, the collision check (`colliderect`) in `_S5._u` happens **after** the teleport call. Since `colliderect` requires overlapping rectangles (~35px center distance), and the exit flees at 50px, collision can **never** be detected.

**Bytecode evidence** (`_S5._u`, lines 320-322):
```
320:  self.wx._u(p)                    # EXIT FLEES (at 50px distance)
322:  p.r.colliderect(self.wx.r)       # CHECK COLLISION (needs <35px)
```

### How I found it

Chased the exit; it always teleported away. Read the bytecode and saw `_u` (flee) at offset 46 executes before `colliderect` at offset 96. The 50px flee threshold is larger than the ~35px collision threshold, creating a dead zone.

### Exact change

```python
# BEFORE (order in _S5._u):
self.wx._u(p)                          # flee first
if p.r.colliderect(self.wx.r):         # check after (too late)

# AFTER:
if p.r.colliderect(self.wx.r):         # check collision FIRST
    self.cp = True
    return
self.wx._u(p)                          # then flee
```

Additionally reduced the flee distance from 50 to 20 in `_Ux._u` to make the exit catchable but still challenging.

### Confirmation

Chased the exit in the inverted-gravity stage. It still moves when close, but collision is now detected before teleport. Stage completes on contact.

---

## Stage 6 - Sealed Box

### What was broken

The EXIT tile is placed at (460, 255), which is **inside a fully sealed box** made of 4 wall segments (top, bottom, left, right). All 4 walls are collision platforms in `self.pf`, so the player physically cannot enter the box to reach the exit.

**Box construction** (`_S6.__init__`):
```
Top:    Rect(330, 140, 300, 40)
Bottom: Rect(330, 370, 300, 40)   ← seals the box
Left:   Rect(330, 140,  40, 270)
Right:  Rect(590, 140,  40, 270)
```

### How I found it

Visualized the box geometry from the constructor parameters. All 4 walls form a closed rectangle with no gap. The exit at (460, 255) is inside. Confirmed by playing: the player bounces off all sides.

### Exact change

```python
# BEFORE: 4 walls (fully sealed)
for rx, ry, rw, rh in (
    (self._BX, self._BY, self._BW, self._WT),                         # top
    (self._BX, self._BY + self._BH - self._WT, self._BW, self._WT),   # bottom
    (self._BX, self._BY, self._WT, self._BH),                         # left
    (self._BX + self._BW - self._WT, self._BY, self._WT, self._BH),   # right
):

# AFTER: 3 walls (bottom removed = opening)
for rx, ry, rw, rh in (
    (self._BX, self._BY, self._BW, self._WT),                         # top
    # bottom wall REMOVED to create entrance
    (self._BX, self._BY, self._WT, self._BH),                         # left
    (self._BX + self._BW - self._WT, self._BY, self._WT, self._BH),   # right
):
```

### Confirmation

Jumped up into the box from below through the opening. Reached the EXIT tile. Stage 6 cleared.

---

## Summary

| Stage | Bug | Root Cause | Patch Type |
|-------|-----|-----------|------------|
| 1 | Door needs 9999 coins, only 3 exist | Wrong threshold constant | Changed `9999` to `3` |
| 2 | 5-second timer at speed 2 | Timer too short | Changed `5` to `30` |
| 3 | Bridge never built | `_rdb()` never called | Added `self._rdb()` to `__init__` |
| 4 | Boss HP resets after damage | Extra assignment `self.hp = self.mh` | Removed the reset line |
| 5 | Exit flees before collision check | Wrong execution order | Moved collision check before flee |
| 6 | Exit sealed inside closed box | 4 walls, no opening | Removed bottom wall |

All 6 stages are now completable start to finish.
