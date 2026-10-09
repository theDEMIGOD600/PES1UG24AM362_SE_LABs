# Lab 4 Video Deliverables

Please place the two required 10-second MP4 recordings in this directory:

1. `before_video.mp4` (or `before_bug.mp4`):
   - **What to demonstrate**: The original unmodified game bug.
   - Run: `cd /Users/thedemigod/.gemini/antigravity/scratch/01_frogger/frogger && python3 main.py`
   - Hop into any traffic lane and show the frog standing while vehicles pass right through it without colliding or dying.
   - Duration: ~10 seconds.

2. `after_video.mp4` (or `after_features.mp4`):
   - **What to demonstrate**: All 4 completed features working.
   - Run: `cd /Users/thedemigod/.gemini/antigravity/scratch/PES1UG24AM362_SE_LABs/Lab-4/frogger && python3 main.py`
   - Show:
     1. 30-second countdown timer ticking down in the HUD (`Time: 30s -> 25s...`).
     2. Vehicle collision accurately triggering frog death, losing a life (`Lives: 3 -> 2`), and respawning at the bottom.
     3. Frog hopping all the way across into the green Goal row (row 0).
     4. Win banner displayed (`YOU WON! Final Score: ...`) with score points including the time bonus.
     5. Pressing `R` resetting the game cleanly.
   - Duration: ~10 seconds.
