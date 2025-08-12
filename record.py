#!/usr/bin/env python3
"""
record.py - Interaction recorder (mouse, keyboard, clicks)
Usage: python3 record.py
"""

import pyautogui
import time
import json
import sys
from datetime import datetime
from pynput import mouse, keyboard

class CompleteRecorder:
    def __init__(self):
        self.recording = False
        self.events = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.previous_position = None
        self.pressed_keys = set()  # To track key combinations
    
    def add_event(self, event_type, **data):
        """Add an event with timestamp"""
        if not self.recording:
            return
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        event = {
            'type': event_type,
            'time': elapsed_time,
            **data
        }
        self.events.append(event)
    
    def on_mouse_move(self, x, y):
        """Callback for mouse movement - only record if there's significant change"""
        current_position = (x, y)
        if self.previous_position != current_position:
            self.add_event('mouse_move', x=x, y=y)
            self.previous_position = current_position
    
    def on_mouse_click(self, x, y, button, pressed):
        """Callback for mouse clicks"""
        self.add_event(
            'mouse_click',
            x=x, y=y,
            button=str(button),
            pressed=pressed
        )
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Callback for mouse scroll"""
        self.add_event(
            'mouse_scroll',
            x=x, y=y,
            dx=dx, dy=dy
        )
    
    def normalize_key(self, key):
        """Normalize key name for comparison"""
        try:
            return key.char
        except AttributeError:
            # Map special keys to consistent names
            key_str = str(key)
            key_map = {
                'Key.ctrl_l': 'ctrl',
                'Key.ctrl_r': 'ctrl', 
                'Key.alt_l': 'alt',
                'Key.alt_r': 'alt',
                'Key.shift': 'shift',
                'Key.shift_r': 'shift',
                'Key.cmd': 'super',
                'Key.cmd_r': 'super',
                'Key.space': 'space',
                'Key.enter': 'enter',
                'Key.tab': 'tab',
                'Key.backspace': 'backspace',
                'Key.delete': 'delete',
                'Key.esc': 'esc',
                'Key.up': 'up',
                'Key.down': 'down',
                'Key.left': 'left',
                'Key.right': 'right',
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
                'Key.f12': 'f12'
            }
            return key_map.get(key_str, key_str)
    
    def detect_combination(self):
        """Detect if there's an active key combination"""
        modifiers = {'ctrl', 'alt', 'shift', 'super'}
        special_keys = {'enter', 'space', 'tab', 'backspace', 'delete', 'esc', 
                       'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown',
                       'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'}
        
        modifier_keys = [k for k in self.pressed_keys if k in modifiers]
        normal_keys = [k for k in self.pressed_keys if k not in modifiers and 
                      (len(k) == 1 or k in special_keys)]
        
        # If there are modifiers + normal/special key, it's a combination
        if modifier_keys and normal_keys:
            return sorted(modifier_keys) + sorted(normal_keys)
        
        # If it's just Enter, Space, Tab, etc. without modifiers, handle as normal key_press
        if len(self.pressed_keys) == 1 and list(self.pressed_keys)[0] in special_keys:
            return None  # Let it be handled as normal key_press
            
        return None
    
    def on_key_press(self, key):
        """Callback for key presses - improved for combinations"""
        key_name = self.normalize_key(key)
        
        # Avoid None or empty keys
        if not key_name:
            return
            
        # Add to pressed keys
        self.pressed_keys.add(key_name)
        
        # Detect combination
        combination = self.detect_combination()
        
        if combination and len(combination) > 1:
            # It's a combination - record as hotkey
            self.add_event('hotkey', keys=combination)
        else:
            # Individual key
            self.add_event('key_press', key=key_name)
    
    def on_key_release(self, key):
        """Callback for key releases - improved for combinations"""
        key_name = self.normalize_key(key)
        
        # Avoid None or empty keys
        if not key_name:
            return
            
        # Remove from pressed keys
        self.pressed_keys.discard(key_name)
        
        # Only record key_release for non-modifier keys when alone
        if key_name not in {'ctrl', 'alt', 'shift', 'super'}:
            self.add_event('key_release', key=key_name)
    
    def start_listeners(self):
        """Start mouse and keyboard listeners"""
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
    
    def stop_listeners(self):
        """Stop listeners"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
    
    def record_events(self, duration):
        """Record all events for a specified duration"""
        print(f"\n🔴 Preparing to record for {duration} seconds...")
        print("Will record: mouse movements, clicks and keystrokes")
        print("\nStarting in:")
        
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        
        print("\n🔴 RECORDING! Interact normally...")
        
        # Reset events
        self.events = []
        self.pressed_keys = set()  # Clear pressed keys
        self.recording = True
        self.start_time = time.time()
        self.previous_position = pyautogui.position()
        
        # Start listeners
        self.start_listeners()
        
        try:
            # Wait for specified duration
            time.sleep(duration)
        except KeyboardInterrupt:
            print("\n⏹️  Recording cancelled by user")
            return None
        
        # Stop recording
        self.recording = False
        self.stop_listeners()
        
        print(f"\n✅ Recording completed!")
        print(f"   📊 Total events: {len(self.events)}")
        
        # Show summary
        event_types = {}
        for event in self.events:
            event_type = event['type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        if event_types:
            print("\n   📈 Summary by type:")
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
        
        return self.events

def save_events(events):
    """Save events to a JSON file with timestamp"""
    if not events:
        print("❌ No events to save")
        return None
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"
    
    try:
        # Calculate statistics
        event_types = {}
        for event in events:
            event_type = event['type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        data = {
            'recording_date': datetime.now().isoformat(),
            'total_events': len(events),
            'duration_seconds': round(events[-1]['time'], 2) if events else 0,
            'event_types': event_types,
            'events': events
        }
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        print(f"\n💾 File saved: {filename}")
        print(f"   ⏱️  Duration: {data['duration_seconds']} seconds")
        print(f"   📝 To playback: python3 play.py {filename}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def main():
    """Main function"""
    print("🎬 INTERACTION RECORDER")
    print("=" * 40)
    
    # Request recording time
    while True:
        try:
            time_str = input("\n⏱️  How many seconds to record? (Enter for 10): ").strip()
            
            if not time_str:
                duration = 10.0
            else:
                duration = float(time_str)
            
            if duration <= 0:
                print("❌ Time must be greater than 0")
                continue
            
            break
            
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            sys.exit(0)
    
    # Create recorder and record
    recorder = CompleteRecorder()
    
    try:
        events = recorder.record_events(duration)
        
        if events:
            saved_file = save_events(events)
            if saved_file:
                print(f"\n🎉 Recording successful!")
            else:
                print("\n❌ Error saving recording")
        else:
            print("\n⏹️  Recording cancelled or no events")
            
    except KeyboardInterrupt:
        print("\n⏹️  Recording interrupted by user")
        recorder.stop_listeners()
    except Exception as e:
        print(f"\n❌ Error during recording: {e}")
        recorder.stop_listeners()

if __name__ == "__main__":
    # pyautogui configuration - FAILSAFE DISABLED
    pyautogui.FAILSAFE = False  # Disabled failsafe (no corner exit)
    pyautogui.PAUSE = 0.01
    
    try:
        main()
    except ImportError as e:
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
