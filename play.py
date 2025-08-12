#!/usr/bin/env python3
"""
play.py - Recorded interactions player
Usage: python3 play.py file.json [speed]
"""

import pyautogui
import time
import json
import sys
import os
from datetime import datetime

def load_events(filename):
    """Load events from JSON file"""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Support both old and new JSON formats
        events = data.get('events', data.get('eventos', []))
        
        if not events:
            print(f"❌ No events in file: {filename}")
            return None
        
        print(f"📁 File loaded: {filename}")
        print(f"   📊 Total events: {len(events)}")
        
        # Support both old and new duration field names
        duration = data.get('duration_seconds', data.get('duracion_segundos', 'N/A'))
        print(f"   ⏱️  Duration: {duration} seconds")
        
        # Support both old and new event types field names
        event_types = data.get('event_types', data.get('tipos_eventos', {}))
        if event_types:
            print("   📈 Event types:")
            for event_type, count in sorted(event_types.items()):
                emoji = {
                    'mouse_move': '🖱️ ',
                    'mouse_click': '🖱️ ',
                    'mouse_scroll': '🔄',
                    'key_press': '⌨️ ',
                    'key_release': '⌨️ ',
                    'hotkey': '🔥'
                }.get(event_type, '📝')
                print(f"      {emoji} {event_type}: {count}")
        
        return events
        
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON file: {filename}")
        return None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def play_events(events, speed=1.0):
    """Play recorded events"""
    if not events:
        return False
    
    print(f"\n▶️  Playing {len(events)} events...")
    print(f"   🚀 Speed: {speed}x")
    print(f"   ⚠️  WARNING: Real clicks and keystrokes will be reproduced!")
    
    # Countdown to give time to prepare
    print("\nStarting in:")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n▶️  PLAYING!")
    
    try:
        previous_time = 0
        executed_events = 0
        
        for i, event in enumerate(events):
            # Show progress every 20 events
            if i % 20 == 0 and i > 0:
                progress = (i / len(events)) * 100
                print(f"   📊 Progress: {progress:.1f}% ({i}/{len(events)})")
            
            # Calculate delay - support both old and new time field names
            event_time = event.get('time', event.get('tiempo', 0))
            delay = (event_time - previous_time) / speed
            if delay > 0:
                time.sleep(delay)
            
            # Execute event based on type - support both old and new type field names
            event_type = event.get('type', event.get('tipo', ''))
            
            if event_type == 'mouse_move':
                pyautogui.moveTo(event['x'], event['y'])
                
            elif event_type == 'mouse_click':
                if event['pressed']:  # Only reproduce on press
                    button_map = {
                        'Button.left': 'left',
                        'Button.right': 'right',
                        'Button.middle': 'middle'
                    }
                    button = button_map.get(event['button'], 'left')
                    pyautogui.click(event['x'], event['y'], button=button)
                    
            elif event_type == 'mouse_scroll':
                scroll_amount = int(event.get('dy', 0))
                if scroll_amount != 0:
                    pyautogui.scroll(scroll_amount, x=event['x'], y=event['y'])
                    
            elif event_type == 'hotkey':
                # Play key combination
                keys = event.get('keys', [])
                if keys:
                    # Map keys for pyautogui
                    mapped_keys = []
                    for key in keys:
                        key_map = {
                            'super': 'win',  # On Windows/Linux
                            'ctrl': 'ctrl',
                            'alt': 'alt', 
                            'shift': 'shift',
                            'space': 'space',
                            'enter': 'enter',
                            'tab': 'tab',
                            'backspace': 'backspace',
                            'delete': 'delete',
                            'esc': 'esc',
                            'up': 'up',
                            'down': 'down',
                            'left': 'left',
                            'right': 'right',
                            'home': 'home',
                            'end': 'end',
                            'page_up': 'pageup',
                            'page_down': 'pagedown'
                        }
                        mapped_key = key_map.get(key, key)
                        mapped_keys.append(mapped_key)
                    
                    # Use hotkey for combinations
                    try:
                        pyautogui.hotkey(*mapped_keys)
                    except Exception as e:
                        # Fallback: press keys individually
                        print(f"      ⚠️  Hotkey fallback for {'+'.join(keys)}")
                        for key in mapped_keys:
                            pyautogui.keyDown(key)
                        for key in reversed(mapped_keys):
                            pyautogui.keyUp(key)
                    
            elif event_type == 'key_press':
                # Map special keys
                key_map = {
                    'Key.space': 'space',
                    'Key.enter': 'enter',
                    'Key.tab': 'tab',
                    'Key.backspace': 'backspace',
                    'Key.delete': 'delete',
                    'Key.ctrl_l': 'ctrl',
                    'Key.ctrl_r': 'ctrl',
                    'Key.alt_l': 'alt',
                    'Key.alt_r': 'alt',
                    'Key.shift': 'shift',
                    'Key.shift_r': 'shift',
                    'Key.up': 'up',
                    'Key.down': 'down',
                    'Key.left': 'left',
                    'Key.right': 'right',
                    'Key.esc': 'esc',
                    'Key.home': 'home',
                    'Key.end': 'end',
                    'Key.page_up': 'pageup',
                    'Key.page_down': 'pagedown',
                    'Key.insert': 'insert',
                    'Key.f1': 'f1',
                    'Key.f2': 'f2',
                    'Key.f3': 'f3',
                    'Key.f4': 'f4',
                    'Key.f5': 'f5',
                    'Key.f6': 'f6',
                    'Key.f7': 'f7',
                    'Key.f8': 'f8',
                    'Key.f9': 'f9',
                    'Key.f10': 'f10',
                    'Key.f11': 'f11',
                    'Key.f12': 'f12',
                    # Direct mapping for already normalized keys
                    'enter': 'enter',
                    'space': 'space',
                    'tab': 'tab',
                    'backspace': 'backspace',
                    'delete': 'delete',
                    'esc': 'esc',
                    'up': 'up',
                    'down': 'down',
                    'left': 'left',
                    'right': 'right',
                    'home': 'home',
                    'end': 'end',
                    'pageup': 'pageup',
                    'pagedown': 'pagedown'
                }
                
                key = event['key']
                if key in key_map:
                    pyautogui.press(key_map[key])
                elif key and len(key) == 1:  # Normal character
                    pyautogui.press(key)
            
            # Only process key_release for special keys that require it
            # (Most are handled automatically with press())
            
            previous_time = event_time
            executed_events += 1
        
        print(f"\n✅ Playback completed!")
        print(f"   📊 Events executed: {executed_events}/{len(events)}")
        return True
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Playback interrupted by user")
        print(f"   📊 Events executed: {executed_events}/{len(events)}")
        return False
    except Exception as e:
        print(f"\n❌ Error during playback: {e}")
        print(f"   📊 Events executed: {executed_events}/{len(events)}")
        return False

def show_help():
    """Show usage help"""
    print("🎮 INTERACTION PLAYER")
    print("=" * 40)
    print("\nUsage:")
    print("  python3 play.py file.json")
    print("  python3 play.py file.json 1.5    # 1.5x speed")
    print("  python3 play.py file.json 0.5    # 0.5x speed (slower)")
    print("\nExamples:")
    print("  python3 play.py 20250115_143022.json")
    print("  python3 play.py my_recording.json 2.0")
    print("\n⚠️  Warnings:")
    print("  • Real clicks and keystrokes will be reproduced")
    print("  • Be careful with high speeds on important actions")

def main():
    """Main function"""
    # Check arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    filename = sys.argv[1]
    
    # Get speed (optional)
    speed = 1.0
    if len(sys.argv) >= 3:
        try:
            speed = float(sys.argv[2])
            if speed <= 0:
                print("❌ Speed must be greater than 0")
                return
        except ValueError:
            print("❌ Invalid speed, using 1.0")
            speed = 1.0
    
    # Load events
    events = load_events(filename)
    if not events:
        return
    
    # Confirm playback
    print(f"\n⚠️  WARNING: {len(events)} real events will be reproduced!")
    if speed != 1.0:
        print(f"   🚀 Configured speed: {speed}x")
    
    try:
        confirm = input("\nContinue with playback? (y/N): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'si', 'sí']:
            print("⏹️  Playback cancelled by user")
            return
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        return
    
    # Play events
    success = play_events(events, speed)
    
    if success:
        print("\n🎉 Playback successful!")
    else:
        print("\n⏹️  Playback ended")

if __name__ == "__main__":
    # pyautogui configuration - FAILSAFE DISABLED
    pyautogui.FAILSAFE = False  # Disabled failsafe (no corner exit)
    pyautogui.PAUSE = 0.01
    
    try:
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n📦 Install dependencies with:")
        print("   pip install pyautogui")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Program interrupted")
