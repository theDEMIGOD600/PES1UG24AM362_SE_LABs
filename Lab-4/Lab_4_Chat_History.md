# Software Engineering Lab 4: Vibe Coding Report
**AI-Assisted Pair Programming & Feature Implementation for Frogger**

---

### Student & Lab Information
- **Student ID:** PES1UG24AM362
- **Repository:** `https://github.com/theDEMIGOD600/PES1UG24AM362_SE_LABs`
- **Lab Directory:** `Lab-4/`
- **Assigned Base Repository:** `https://github.com/SETAPESU26/01_frogger`
- **Vibe Coding Assistant:** Gemini 3.8 Flash
- **Status:** All 4 Tasks Completed with Separate Commits

---

## 1. Overview & Objectives

This lab explores **Vibe Coding**—using LLM conversational assistants for debugging and incremental software feature engineering. Starting from the starter Pygame implementation of Frogger provided in `01_frogger`, we identify broken collision detection logic, implement a 3-life respawn system, engineer goal reaching with score tracking and a win state, and add a 30-second attempt countdown timer.

Each step was executed using specific, targeted prompts, followed by code verification and isolated Git commits.

---

## 2. Tasks & Vibe Coding Prompts

### 2.1 Task 1: Fix Vehicle Collision Detection

#### Prompt
> *"Inspect game/collisions.py and vehicle.py in the Frogger game. The frog is passing through moving vehicles without collisions triggering reliably. Diagnose why the collision logic fails and provide an accurate fix using Pygame's bounding box collision system."*

#### AI Diagnosis & Analysis
- **Root Cause:** In the starter `game/collisions.py`, collisions were evaluated using:
  ```python
  vehicle_col = int(v.x // CELL_SIZE)
  if vehicle_col == frog.col and v.row == frog.row:
      return True
  ```
- **Flaw:** Vehicles move continuously in float pixels (e.g. speeds like `1.5` or `-2.5`) and have widths of 40–70px, which span multiple grid cells. Checking only the integer cell division of the vehicle's left edge causes the frog and vehicles to clip through each other on virtually every frame.

#### Implemented Solution
In `game/collisions.py`, we replaced the heuristic column division with Pygame's native axis-aligned bounding box collision detection:
```python
def check_collision(frog, vehicles):
    frog_rect = frog.get_rect(CELL_SIZE)
    for v in vehicles:
        if v.row == frog.row and v.get_rect(CELL_SIZE).colliderect(frog_rect):
            return True
    return False
```

#### Git Commit
- `Task 1: Fix vehicle collision detection using bounding box intersection`

---

### 2.2 Task 2: Implement Lives and Respawn System

#### Prompt
> *"Implement a 3-life system for Frogger with proper respawn behaviour. When a collision occurs, the frog should respawn at its starting position and lose 1 life. When all 3 lives are exhausted, trigger a Game Over state, lock frog movement, and display a game-over banner. Allow pressing 'R' to restart."*

#### AI Diagnosis & Analysis
- Extended `GameEngine` with `max_lives = 3`, `lives = 3`, and `game_over = False`.
- Integrated collision response inside `update()`: decrementing life count and calling `frog.reset()`.
- Implemented `restart()` to restore 3 lives and rebuild entities upon pressing `R`.
- Added game-over banner rendering and HUD display in `renderer.py`.

#### Git Commit
- `Task 2: Implement 3-life system, frog respawn, and game over state`

---

### 2.3 Task 3: Implement Goal Completion and Score Tracking

#### Prompt
> *"Implement goal detection when the frog reaches row 0 (the goal zone). Add score tracking (+100 points on reaching the goal), display the score in the HUD, and trigger an appropriate win state with a banner. Pressing 'R' should reset the game and score."*

#### AI Diagnosis & Analysis
- Added `score = 0` and `game_won = False` to `GameEngine`.
- In `update()`, detected when `frog.row == GOAL_ROW` (row 0), awarding points and transitioning to `game_won = True`.
- Added input guards in `handle_keydown()` to prevent movement during win state.
- Rendered `Lives: X   Score: Y` in the top HUD and a celebratory victory banner.

#### Git Commit
- `Task 3: Implement goal completion detection, score tracking, and win state`

---

### 2.4 Task 4: Add 30-Second Countdown Timer & Timeout Handling

#### Prompt
> *"Add a 30-second countdown timer for each attempt in Frogger. The timer should display in the HUD and count down in real-time. If the timer reaches 0, the frog must lose a life, respawn at start, and reset the attempt timer to 30s. If lives reach 0, trigger Game Over. If the frog wins, award a time bonus based on seconds remaining."*

#### AI Diagnosis & Analysis
- Added `attempt_time_limit = 30.0` and `time_remaining = 30.0` to `GameEngine`.
- In `main.py`, measured frame delta time using Pygame clock (`dt = clock.tick(60) / 1000.0`) and passed to `engine.update(dt)`.
- Centralized life-loss logic in `_handle_life_lost()` to consistently handle both collisions and timeouts.
- Added time bonus calculation: `score += 100 + int(round(time_remaining)) * 10`.
- HUD dynamically formats remaining seconds (`Time: 30s`) and highlights red when under 5 seconds.

#### Git Commit
- `Task 4: Add 30-second countdown timer per attempt and timeout handling`

---

## 3. Git Commit History
```text
* 0fbccac Task 4: Add 30-second countdown timer per attempt and timeout handling
* eddb403 Task 3: Implement goal completion detection, score tracking, and win state
* 5e76bdb Task 2: Implement 3-life system, frog respawn, and game over state
* e9e2e25 Task 1: Fix vehicle collision detection using bounding box intersection
* f93c2db Initialize Lab-4 with original Frogger game starter code
```

---

## 4. Deliverables Checklist
- [x] **Task 1 Completed**: Vehicle collision detection fixed and validated.
- [x] **Task 2 Completed**: 3-life system, respawn, and Game Over handled.
- [x] **Task 3 Completed**: Goal row win state and score tracking implemented.
- [x] **Task 4 Completed**: 30-second attempt countdown timer and time bonus active.
- [x] **Separate Commits**: Individual commits for each task with descriptive messages.
- [x] **Updated Code**: Present in `Lab-4/frogger/`.
- [x] **Chat History / Report**: Available as `Lab_4_Chat_History.pdf` and `Lab_4_Chat_History.docx`.
- [ ] **Demonstration Videos**: Place recordings in `Lab-4/videos/` (`before_video.mp4` and `after_video.mp4`).
