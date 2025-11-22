#!/usr/bin/env python3
"""
Kokoro TTS - Terminal Text-to-Speech
Usage: python3 kokoro-tts.py "Your text here"
"""
import sys
from kokoro import KPipeline
import soundfile as sf
import subprocess
import os
from datetime import datetime
import platform

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

def speak(text, voice='af_heart'):
    """Convert text to speech and play it"""
    pipeline = KPipeline(lang_code='a')  # 'a' = American English
    
    # Create output directory
    output_dir = os.path.expanduser('~/kokoro-audio')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"kokoro_{timestamp}.wav"
    output_path = os.path.join(output_dir, filename)
    
    print(f"🗣️  Speaking: {text[:50]}...")
    print(f"🎵  Generating audio segments...")
    
    # Generate audio - collect all segments
    generator = pipeline(text, voice=voice)
    all_audio = []
    
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"   Segment {i+1}...")
        all_audio.append(audio)
    
    # Concatenate all segments
    import numpy as np
    full_audio = np.concatenate(all_audio)
    
    # Save complete audio
    sf.write(output_path, full_audio, 24000)
    print(f"💾 Saved complete audio ({len(all_audio)} segments)")
    
    # Play audio using platform-specific command
    system = platform.system()
    try:
        if system == 'Darwin':  # macOS
            print(f"▶️  Playing...")
            subprocess.run(['afplay', output_path], check=True)
        elif system == 'Linux':
            print(f"▶️  Playing...")
            # Try common Linux audio players
            for player in ['paplay', 'aplay', 'ffplay', 'mpv']:
                try:
                    subprocess.run([player, output_path], check=True, stderr=subprocess.DEVNULL)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
        elif system == 'Windows':
            print(f"▶️  Playing...")
            # Use sounddevice for in-terminal playback (no GUI window)
            if HAS_SOUNDDEVICE:
                sd.play(full_audio, 24000)
                sd.wait()  # Wait for playback to finish
            else:
                # Fallback to opening default player (VLC, etc.)
                os.startfile(output_path)
        else:
            print(f"⚠️  Auto-play not supported on {system}. File saved.")
    except Exception as e:
        print(f"⚠️  Could not auto-play audio: {e}")
    
    print(f"✅ Done! Saved to: {output_path}")

def show_help():
    print("Kokoro TTS - Terminal Text-to-Speech")
    print("\nUsage:")
    print("  kokoro [OPTIONS] <text>")
    print("  kokoro [OPTIONS] --file <file>")
    print("\nOptions:")
    print("  --voice, -v VOICE    Choose a voice (default: af_heart)")
    print("  --file, -f FILE      Read text from a file")
    print("  --help, -h           Show this help message")
    print("\nVoice Shortcuts:")
    print("  --michael, --adam, --echo, --fenrir (male voices)")
    print("  --bella, --sarah, --heart, --sky, --nicole (female voices)")
    print("\nAvailable Voices:")
    print("  Male:   am_adam, am_michael, am_echo, am_fenrir (⭐ best),")
    print("          am_eric, am_liam, am_onyx, am_puck, am_santa")
    print("  Female: af_heart, af_bella, af_sarah, af_sky, af_nicole,")
    print("          af_nova, af_alloy, af_aoede, af_jessica, af_river, af_kore")
    print("  British: bf_emma")
    print("\nExamples:")
    print("  kokoro --michael \"Hello world\"")
    print("  kokoro --echo --file README.md")
    print("  kokoro -v am_fenrir \"This is a test\"")
    print("\nAudio files are saved to: ~/kokoro-audio/")

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        sys.exit(0 if '--help' in sys.argv or '-h' in sys.argv else 1)
    
    # Parse arguments
    voice = 'af_heart'
    filename = None
    args = sys.argv[1:]
    
    # Voice shortcuts
    voice_shortcuts = {
        '--michael': 'am_michael', '--adam': 'am_adam', '--echo': 'am_echo',
        '--fenrir': 'am_fenrir', '--eric': 'am_eric', '--liam': 'am_liam',
        '--onyx': 'am_onyx', '--puck': 'am_puck', '--santa': 'am_santa',
        '--bella': 'af_bella', '--sarah': 'af_sarah', '--heart': 'af_heart',
        '--sky': 'af_sky', '--nicole': 'af_nicole', '--nova': 'af_nova',
        '--emma': 'bf_emma'
    }
    
    for shortcut, voice_name in voice_shortcuts.items():
        if shortcut in args:
            voice = voice_name
            args.remove(shortcut)
            break
    
    if '--voice' in args or '-v' in args:
        key = '--voice' if '--voice' in args else '-v'
        idx = args.index(key)
        if idx + 1 < len(args):
            voice = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    if '--file' in args or '-f' in args:
        key = '--file' if '--file' in args else '-f'
        idx = args.index(key)
        if idx + 1 < len(args):
            filename = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    # Get text from file or command line
    if filename:
        # Try multiple encodings to handle different file types
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        text = None
        last_error = None
        
        for encoding in encodings:
            try:
                with open(os.path.expanduser(filename), 'r', encoding=encoding) as f:
                    text = f.read()
                break  # Success! Exit the loop
            except (UnicodeDecodeError, LookupError) as e:
                last_error = e
                continue  # Try next encoding
        
        if text is None:
            print(f"Error reading file: Could not decode file with any standard encoding.")
            print(f"Last error: {last_error}")
            print(f"Tried encodings: {', '.join(encodings)}")
            sys.exit(1)
    else:
        text = ' '.join(args)
    
    if not text.strip():
        print("Error: No text provided")
        sys.exit(1)
    
    speak(text, voice=voice)
