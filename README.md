# Simple Automation Tool (SAT)

A lightweight Python utility to **record** and **replay** your computer 
interactions — including mouse movements, clicks, and keyboard strokes.

Perfect for automation testing, repetitive task execution, or capturing input 
for later replay.

---

## 📦 Setup

Clone the repository:

```bash
git clone https://github.com/agustfricke/sat.git ~/sat
cd ~/sat
```

Create a Python virtual environment and install dependencies:

```bash
python3 -m venv ~/sat/env
source ~/sat/env/bin/activate
pip install -r ~/sat/requirements.txt
```

---

## 🚀 Usage

### 1. Record Interactions

Run:

```bash
python3 record.py
```

You will be prompted for the duration of the recording. Press **Enter** for the default (10 seconds).
The tool will capture mouse movements, clicks, and keystrokes until the timer runs out.

Example:

```
🎬 INTERACTION RECORDER
========================================

⏱️  How many seconds to record? (Enter for 10):

🔴 Preparing to record for 10.0 seconds...
Will record: mouse movements, clicks and keystrokes

Starting in:
  3...
  2...
  1...

🔴 RECORDING! Interact normally...

✅ Recording completed!
   📊 Total events: 659

   📈 Summary by type:
      🖱️  mouse_move: 659

💾 File saved: 20250812_193039.json
   ⏱️  Duration: 5.79 seconds
   📝 To playback: python3 play.py 20250812_193039.json

🎉 Recording successful!
```

The recording is saved as a `.json` file, ready for playback.

---

### 2. Play a Recording

To replay a recorded file:

```bash
python3 play.py 20250812_193039.json
```

You will see a summary and a warning before playback begins. Confirm with **y** to proceed.

Example:

```
📁 File loaded: 20250812_193039.json
   📊 Total events: 659
   ⏱️  Duration: 5.79 seconds
   📈 Event types:
      🖱️  mouse_move: 659

⚠️  WARNING: 659 real events will be reproduced!
Continue with playback? (y/N): y

▶️  Playing 659 events...
...
✅ Playback completed!
🎉 Playback successful!
```

---

### 3. Batch Playback

Replay multiple recordings in sequence:

```bash
python3 batch.py file1.json file2.json
```

You can set:

* **Playback speed** (`1.0x` default)
* **Pause between files** (in seconds)

Example:

```
🔄 BATCH INTERACTION PLAYER
=============================================

📋 CONFIGURATION:
   📁 Files to process: 2
   🚀 Speed: 1.0x
   ⏸️  Pause between files: 2.0s

📂 FILES:
   1. 20250812_193039.json
   2. 20250812_193217.json
...
🏁 BATCH PLAYBACK FINISHED
🎉 Batch processing completed!
```
