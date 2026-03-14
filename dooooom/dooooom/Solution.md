# DOOM — Friendly Fire: Companion Bot Writeup

---

## 📹 Video Demonstration

**Complete video walkthrough of the solution:**  
🔗 **[Watch Video on Google Drive](https://drive.google.com/drive/folders/115YtlDNdq66g7jkymnAku5ePvdggAZxc?usp=sharing)** 

---


## What We Built

A **companion bot** that spawns alongside the player at the beginning of each level, follows the player through the map, and engages hostile monsters in combat.

The bot uses the **Imp (MT_TROOP)** as its base monster type, inheriting all its sprites, animations, melee/ranged attacks, and sound effects. It is visually distinguished from regular Imps by a **green color translation palette**.

---

## Which Parts of the Existing Codebase We Used

The core design philosophy was to **reuse existing DOOM engine systems** with minimal new code. Here's what the companion bot leverages:

### Movement & Pathfinding
- **`P_Move()`** — Standard monster movement function, handles collision with walls, steps up stairs (max 24 units), and activates door line specials when blocked
- **`P_NewChaseDir()`** — The original DOOM pathfinding algorithm. Calculates optimal direction toward `actor->target`, tries diagonal, then cardinal, then random directions
- **`P_TryMove()`** — Physics-level collision detection

### Combat
- **`P_CheckMeleeRange()`** — Determines if the bot is close enough for melee attack
- **`P_CheckMissileRange()`** — Determines if the bot should fire a ranged projectile
- **`P_SpawnMissile()`** — Creates projectiles (Imp fireballs) aimed at the target
- **`A_TroopAttack()`** — The Imp's existing melee/ranged attack action, called through the state machine

### Sensing & Detection
- **`P_CheckSight()`** — Line-of-sight checks between the bot and potential targets
- **`P_AproxDistance()`** — Fast distance approximation for finding nearest enemies
- **Thinker list iteration** — Scanning all active entities (same pattern used by `A_VileChase`, `A_BrainAwake`, `A_PainShootSkull`)

### Animation & State Machine
- All Imp sprite states (`S_TROO_STND`, `S_TROO_RUN1-8`, `S_TROO_ATK1-3`, `S_TROO_PAIN`, `S_TROO_DIE1-5`) are reused directly
- `P_SetMobjState()` and `P_MobjThinker()` handle animation frame cycling

### Spawning
- **`P_SpawnMobj()`** — Standard entity spawning
- **`MT_TFOG`** — Teleport fog visual effect at spawn location

---

## How It Works

### Custom AI: `A_CompanionChase()`

The companion's behavior is governed by a **3-priority decision system** that runs every game tick:

1. **Attack enemies** (Priority 1): Scans all thinkers for hostile monsters (`MF_COUNTKILL` flag, alive, within 1024 units, line-of-sight visible). Engages the nearest one using the Imp's existing melee/missile attack system.

2. **Follow the player** (Priority 2): If no enemy is nearby and the bot is more than 196 map units from the player, it targets the player's position and uses `P_NewChaseDir()` + `P_Move()` to navigate toward them.

3. **Idle** (Priority 3): When close to the player and no enemies are visible, the bot faces the same direction as the player and stops moving.

### Friendly Fire Prevention

Three locations were modified to prevent player↔companion damage:

- **`P_DamageMobj()` (p_inter.c)** — Blocks direct damage between player and companion
- **`PIT_CheckThing()` (p_map.c)** — Player missiles pass through the companion and vice versa
- **`P_KillMobj()` (p_inter.c)** — Clears the global companion pointer when the bot dies

---

## Files Modified

| File | Lines Changed | What |
|------|--------------|------|
| `src/doom/p_local.h` | +13 | Added `companion_bot` global, `IsCompanion()` macro, function declarations |
| `src/doom/p_enemy.c` | +225 | Added `P_FindNearestEnemy()`, `A_CompanionChase()`, `P_SpawnCompanion()` |
| `src/doom/p_mobj.c` | +20 | Hooked companion AI into `P_MobjThinker()`, spawn call in `P_SpawnPlayer()` |
| `src/doom/p_inter.c` | +23 | Friendly fire prevention in `P_DamageMobj()` and `P_KillMobj()` |
| `src/doom/p_map.c` | +11 | Missile pass-through in `PIT_CheckThing()` |

---

## What Broke During Development (and How We Fixed It)

### Problem: Bot gets stuck in idle animation
When the bot was spawned, it started in `S_TROO_STND` (the idle state with `A_Look` callback). Since `A_Look` only searches for players, it would never transition to a run state on its own. **Fix:** Set initial state to `seestate` (`S_TROO_RUN1`) at spawn time.

### Problem: Bot targets the player
The existing `A_Look` → `P_LookForPlayers` code makes monsters chase players. If we let the normal AI run, the bot would attack the player. **Fix:** Completely override the AI in `P_MobjThinker()` — when the companion is detected, we call `A_CompanionChase()` instead of letting the normal state machine callbacks run.

### Problem: Player can kill companion / companion can kill player
Without special handling, the player's shotgun would damage the companion, and the companion's fireballs would hurt the player. **Fix:** Added checks in three locations — `P_DamageMobj` (direct damage), `PIT_CheckThing` (missile collision), and proper pointer cleanup in `P_KillMobj`.

### Problem: Kill counter affected
Without removing `MF_COUNTKILL`, the companion would count toward the level's kill percentage statistics. **Fix:** Clear `MF_COUNTKILL` flag at spawn.

---

## Build Instructions

```bash
cd chocolate-doom
mkdir build && cd build
cmake ..
make
./src/chocolate-doom -iwad freedoom1.wad
```

The companion bot will automatically spawn behind the player at the start of each level with a teleport fog effect.
