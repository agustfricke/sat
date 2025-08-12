#!/usr/bin/env python3
"""
batch.py - Batch interaction player
Usage: python3 batch.py file1.json file2.json [speed]
       python3 batch.py *.json [speed]
"""

import pyautogui
import time
import json
import sys
import os
import glob
from datetime import datetime

def load_events(filename):
    """Load events from JSON file"""
    if not os.path.exists(filename):
        return None, f"File not found: {filename}"
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Support both old and new JSON formats
        events = data.get('events', data.get('eventos', []))
        
        if not events:
            return None, f"No events in file: {filename}"
        
        return events, data
        
    except json.JSONDecodeError:
        return None, f"Invalid JSON file: {filename}"
    except Exception as e:
        return None, f"Error loading file: {e}"

def play_events(events, speed=1.0, show_progress=True):
    """Play recorded events"""
    if not events:
        return False
    
    try:
        previous_time = 0
        executed_events = 0
        total_events = len(events)
        
        for i, event in enumerate(events):
            # Show progress every 50 events
            if show_progress and i % 50 == 0 and i > 0:
                progress = (i / total_events) * 100
                print(f"      📊 Progress: {progress:.1f}% ({i}/{total_events})")
            
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
                if event['pressed']:
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
                    except Exception:
                        # Fallback: press keys individually
                        for key in mapped_keys:
                            pyautogui.keyDown(key)
                        for key in reversed(mapped_keys):
                            pyautogui.keyUp(key)
                    
            elif event_type == 'key_press':
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
                elif key and len(key) == 1:
                    pyautogui.press(key)
            
            previous_time = event_time
            executed_events += 1
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n      ⏹️  Interrupted - Executed: {executed_events}/{len(events)}")
        return False
    except Exception as e:
        print(f"\n      ❌ Error: {e} - Executed: {executed_events}/{len(events)}")
        return False

def process_files(files, speed=1.0, pause_between_files=2.0):
    """Process multiple files in sequence"""
    valid_files = []
    files_info = []
    
    print("📂 Validating files...")
    
    # Validate all files first
    for file in files:
        events, data = load_events(file)
        if events:
            valid_files.append(file)
            if isinstance(data, dict):
                # Support both old and new field names
                duration = data.get('duration_seconds', data.get('duracion_segundos', 'N/A'))
                event_types = data.get('event_types', data.get('tipos_eventos', {}))
                info = {
                    'file': file,
                    'events': len(events),
                    'duration': duration,
                    'types': event_types
                }
            else:
                info = {
                    'file': file,
                    'events': len(events),
                    'duration': 'N/A',
                    'types': {}
                }
            files_info.append(info)
            print(f"   ✅ {file} - {len(events)} events")
        else:
            print(f"   ❌ {file} - {data}")
    
    if not valid_files:
        print("\n❌ No valid files to process")
        return False
    
    # Show summary
    total_events = sum(info['events'] for info in files_info)
    total_duration = sum(float(info['duration']) for info in files_info if info['duration'] != 'N/A')
    
    print(f"\n📊 SUMMARY:")
    print(f"   📁 Valid files: {len(valid_files)}")
    print(f"   📝 Total events: {total_events:,}")
    print(f"   ⏱️  Total duration: {total_duration:.1f} seconds")
    print(f"   🚀 Speed: {speed}x")
    print(f"   ⏸️  Pause between files: {pause_between_files}s")
    
    # Confirm execution
    print(f"\n⚠️  WARNING: {total_events:,} real events will be reproduced!")
    try:
        confirm = input("Continue with batch playback? (y/N): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'si', 'sí']:
            print("⏹️  Batch playback cancelled by user")
            return False
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        return False
    
    # Initial countdown
    print(f"\nStarting batch playback in:")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n🚀 STARTING BATCH PLAYBACK!")
    print("    Press Ctrl+C to cancel\n")
    
    # Process each file
    successful_files = 0
    total_start_time = time.time()
    
    try:
        for i, info in enumerate(files_info):
            file = info['file']
            events_count = info['events']
            
            print(f"📁 [{i+1}/{len(files_info)}] Processing: {os.path.basename(file)}")
            print(f"    📊 Events: {events_count}")
            
            # Load events
            events, _ = load_events(file)
            
            if events:
                # Play events
                file_start_time = time.time()
                success = play_events(events, speed, show_progress=True)
                file_time = time.time() - file_start_time
                
                if success:
                    successful_files += 1
                    print(f"    ✅ Completed in {file_time:.1f}s")
                else:
                    print(f"    ⏹️  Ended after {file_time:.1f}s")
                    # Ask if continue
                    try:
                        continue_choice = input("    Continue with next file? (y/N): ").lower().strip()
                        if continue_choice not in ['y', 'yes', 's', 'si', 'sí']:
                            break
                    except KeyboardInterrupt:
                        break
                
                # Pause between files (except the last one)
                if i < len(files_info) - 1:
                    print(f"    ⏸️  Pausing {pause_between_files}s before next file...")
                    time.sleep(pause_between_files)
            else:
                print(f"    ❌ Error loading events")
            
            print()
    
    except KeyboardInterrupt:
        print("\n⏹️  Batch playback interrupted by user")
    
    # Final summary
    total_time = time.time() - total_start_time
    print(f"🏁 BATCH PLAYBACK FINISHED")
    print(f"   ✅ Files processed successfully: {successful_files}/{len(files_info)}")
    print(f"   ⏱️  Total time: {total_time:.1f} seconds")
    
    return successful_files > 0

def show_help():
    """Show usage help"""
    print("🔄 BATCH INTERACTION PLAYER")
    print("=" * 45)
    print("\nUsage:")
    print("  python3 batch.py file1.json file2.json")
    print("  python3 batch.py *.json")
    print("  python3 batch.py file1.json file2.json 1.5    # 1.5x speed")
    print("  python3 batch.py *.json 0.5                    # 0.5x speed")
    print("\nExamples:")
    print("  python3 batch.py 20250115_*.json")
    print("  python3 batch.py session1.json session2.json session3.json")
    print("  python3 batch.py *.json 2.0")
    print("\nOptions:")
    print("  speed    Speed factor (default: 1.0)")
    print("           0.5 = slower, 2.0 = faster")
    print("\n⚠️  Warnings:")
    print("  • Real clicks and keystrokes will be reproduced")
    print("  • Use high speeds with caution")

def expand_files(arguments):
    """Expand patterns like *.json"""
    files = []
    for arg in arguments:
        if '*' in arg or '?' in arg:
            # It's a pattern, expand it
            expanded_files = glob.glob(arg)
            if expanded_files:
                files.extend(sorted(expanded_files))
            else:
                print(f"⚠️  No files found matching: {arg}")
        else:
            # It's a specific file
            files.append(arg)
    return files

def main():
    """Main function"""
    print("🔄 BATCH INTERACTION PLAYER")
    print("=" * 45)
    
    # Check arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    arguments = sys.argv[1:]
    
    # Get speed (last argument if it's a number)
    speed = 1.0
    files_args = arguments
    
    try:
        # Check if last argument is speed
        last_arg = arguments[-1]
        speed_test = float(last_arg)
        if speed_test > 0:
            speed = speed_test
            files_args = arguments[:-1]  # All except last
    except (ValueError, IndexError):
        # Last argument is not valid speed
        pass
    
    if not files_args:
        print("❌ No files specified")
        show_help()
        return
    
    # Expand file patterns
    files = expand_files(files_args)
    
    if not files:
        print("❌ No valid files found")
        return
    
    # Configure pause between files
    pause_between_files = 2.0
    if len(files) > 5:
        pause_between_files = 1.0  # Less pause for many files
    
    print(f"\n📋 CONFIGURATION:")
    print(f"   📁 Files to process: {len(files)}")
    print(f"   🚀 Speed: {speed}x")
    print(f"   ⏸️  Pause between files: {pause_between_files}s")
    
    # Show file list
    print(f"\n📂 FILES:")
    for i, file in enumerate(files, 1):
        print(f"   {i}. {file}")
    
    # Process files
    success = process_files(files, speed, pause_between_files)
    
    if success:
        print("\n🎉 Batch processing completed!")
    else:
        print("\n⏹️  Batch processing ended")

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
