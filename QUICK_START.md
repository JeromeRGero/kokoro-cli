# Kokoro TTS CLI - Quick Start Guide

## One-Line Commands

```powershell
# Male voices (best quality)
python kokoro-tts.py --michael "Your text here"
python kokoro-tts.py --fenrir "Your text here"
python kokoro-tts.py --puck "Your text here"

# Female voices
python kokoro-tts.py --bella "Your text here"
python kokoro-tts.py --sarah "Your text here"
python kokoro-tts.py --heart "Your text here"

# British accent
python kokoro-tts.py --emma "Your text here"

# Read from file
python kokoro-tts.py --michael --file document.txt
```

## Full Path Version

```powershell
python C:\Users\Jerome\kokoro-cli\kokoro-tts.py --michael "Your text"
```

## Output Location

All audio files are saved to:
```
C:\Users\Jerome\kokoro-audio\kokoro_YYYYMMDD_HHMMSS.wav
```

## Create a Shortcut (Optional)

Add this to your PowerShell profile (`$PROFILE`):

```powershell
function kokoro { python C:\Users\Jerome\kokoro-cli\kokoro-tts.py $args }
```

Then just use:
```powershell
kokoro --michael "Hello world"
```

## Best Voices

⭐ **Top 3 Male**: `--fenrir`, `--michael`, `--puck`
⭐ **Default Female**: `--heart`
⭐ **British**: `--emma`

---

For full documentation, see `README.md` or run:
```powershell
python kokoro-tts.py --help
```
