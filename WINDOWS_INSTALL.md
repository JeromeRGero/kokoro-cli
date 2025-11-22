# Windows Installation Guide for Kokoro TTS CLI

This guide provides detailed Windows-specific installation instructions, especially for Python 3.13+ users.

## Prerequisites

- Windows 10 or later
- Python 3.10 or newer
- Git (recommended) - [Download Git for Windows](https://git-scm.com/download/win)
- ~3.5 GB free disk space for dependencies
- Internet connection (for downloading models)

## Python 3.13+ Installation (Recommended Method)

### Why Special Steps?

Python 3.13 is very new, and some dependencies aren't available on PyPI yet for this version. We need to install from GitHub sources instead.

### Step-by-Step Installation

#### 1. Install Python

1. Download Python 3.13 from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```powershell
   python --version
   ```
   Should show: `Python 3.13.x`

#### 2. Install Git (if not already installed)

1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Use default installation settings
3. Verify:
   ```powershell
   git --version
   ```

#### 3. Clone the Repository

Open PowerShell and run:

```powershell
# Navigate to where you want to install (e.g., your home directory)
cd ~

# Clone the CLI repository
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli
```

#### 4. Install PyTorch

This is the largest download (~2.8 GB). Includes CUDA support for GPU acceleration:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Time estimate**: 5-10 minutes depending on your internet connection.

#### 5. Install Core Dependencies

```powershell
pip install soundfile sounddevice huggingface_hub loguru transformers scipy
```

**Note**: `sounddevice` enables audio playback directly in the terminal without opening media player windows.

**Time estimate**: 2-3 minutes

#### 6. Install spaCy

spaCy has pre-built wheels for Windows, so this is straightforward:

```powershell
pip install spacy
```

#### 7. Create Constraints File

This prevents dependency conflicts during installation:

```powershell
echo spacy==3.8.11 > constraints.txt
echo thinc==8.3.10 >> constraints.txt
echo blis==1.3.3 >> constraints.txt
```

#### 8. Install misaki from GitHub

The latest misaki version (0.9.4+) is only on GitHub:

```powershell
pip install git+https://github.com/hexgrad/misaki.git -c constraints.txt
```

**Time estimate**: 1-2 minutes

#### 9. Clone and Install Kokoro

```powershell
# Go up one directory
cd ..

# Clone the kokoro repository
git clone https://github.com/hexgrad/kokoro.git

# Install kokoro from the local clone
pip install .\kokoro -c kokoro-cli\constraints.txt
```

**Time estimate**: 1-2 minutes

#### 10. Clean Up and Test

```powershell
# Remove the constraints file
del kokoro-cli\constraints.txt

# Navigate back to the CLI directory
cd kokoro-cli

# Test the installation!
python kokoro-tts.py --michael "Hello world"
```

If successful, you should hear "Hello world" spoken in a male voice, and a WAV file will be saved to `C:\Users\YourName\kokoro-audio\`.

## Python 3.12 and Below (Simple Installation)

If you're using Python 3.12 or earlier, installation is much simpler:

```powershell
# Install dependencies
pip install kokoro soundfile

# Download the script
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli

# Test
python kokoro-tts.py --michael "Hello world"
```

## Usage

### Basic Commands

```powershell
# Simple text-to-speech
python kokoro-tts.py --michael "Your text here"

# Use different voices
python kokoro-tts.py --fenrir "Best quality male voice"
python kokoro-tts.py --bella "Female voice"
python kokoro-tts.py --emma "British accent"

# Read from a file
python kokoro-tts.py --echo --file document.txt

# Get help
python kokoro-tts.py --help
```

### Creating a Global Command

To use `tts` from anywhere (recommended!), set up a PowerShell function:

#### Automatic Setup (Copy & Paste)

```powershell
# Create profile if it doesn't exist
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -Type File -Force
}

# Add tts function (adjust path if you installed elsewhere)
Add-Content -Path $PROFILE -Value "`n# Kokoro TTS CLI shortcut`nfunction tts { python C:\Users\$env:USERNAME\kokoro-cli\kokoro-tts.py `$args }"

# Reload profile
. $PROFILE

# Test it!
tts --michael "Hello world"
```

#### Manual Setup

**Step 1:** Create or open your PowerShell profile

```powershell
# Create if it doesn't exist
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -Type File -Force
}

# Open in notepad
notepad $PROFILE
```

**Step 2:** Add this line (adjust path to your installation):

```powershell
# Kokoro TTS CLI shortcut
function tts { python C:\Users\YourName\kokoro-cli\kokoro-tts.py $args }
```

**Step 3:** Save and reload your profile

```powershell
. $PROFILE
```

#### Usage

Now you can use `tts` from **any directory**:

```powershell
# From anywhere
tts --michael "Hello world"

# In your Downloads folder
cd Downloads
tts --fenrir --file .\story.txt

# Quick test
tts --bella "It's working perfectly!"
```

The command works in all new PowerShell windows automatically!

## Output Files

Audio files are saved to:
```
C:\Users\YourName\kokoro-audio\kokoro_YYYYMMDD_HHMMSS.wav
```

To open the folder:
```powershell
explorer $HOME\kokoro-audio
```

## Troubleshooting

### "pip is not recognized"

Python wasn't added to PATH during installation. Reinstall Python and check "Add Python to PATH".

### "git is not recognized"

Install Git for Windows from [git-scm.com](https://git-scm.com/download/win).

### Build errors (blis, spaCy, curated-tokenizers)

This happens when trying to install dev versions of spaCy. Solution:
1. Follow the Python 3.13+ installation steps above
2. Use the constraints file to lock spaCy version
3. Install from GitHub sources

### "TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'"

Your misaki version is outdated. Reinstall from GitHub:

```powershell
pip uninstall misaki -y
pip install git+https://github.com/hexgrad/misaki.git
```

### First run is very slow

This is normal! The first run downloads:
- Kokoro TTS model (~327 MB)
- Voice model files (~523 KB per voice)
- spaCy English model (~12 MB)

All files are cached locally, so subsequent runs are much faster.

### Audio doesn't play automatically

Make sure `sounddevice` is installed:

```powershell
pip install sounddevice
```

If it still doesn't work, the file is always saved. You can:
- Double-click the WAV file in File Explorer
- Open the folder: `explorer $HOME\kokoro-audio`
- Play manually: Right-click → Open with → Windows Media Player

**Note**: With `sounddevice`, audio plays directly in the terminal without opening any windows!

### Permission errors during installation

Run PowerShell as Administrator:
1. Search for "PowerShell" in Start Menu
2. Right-click → "Run as Administrator"
3. Run the installation commands

### "WARNING: scripts not on PATH"

This is just a warning and doesn't affect functionality. You can safely ignore it, or add the Scripts directory to your PATH:

```powershell
$ScriptsPath = "$env:APPDATA\Python\Python313\Scripts"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$ScriptsPath", "User")
```

## Uninstallation

To completely remove Kokoro TTS:

```powershell
# Remove the repositories
cd ~
rmdir -Recurse -Force kokoro-cli
rmdir -Recurse -Force kokoro

# Remove the audio output folder
rmdir -Recurse -Force $HOME\kokoro-audio

# Uninstall packages
pip uninstall kokoro misaki soundfile torch -y

# Remove cached models (optional, saves ~340 MB)
rmdir -Recurse -Force $HOME\.cache\huggingface
```

## Technical Notes

### Why is PyTorch so large?

PyTorch includes CUDA support for GPU acceleration, which makes TTS generation much faster. If you don't have an NVIDIA GPU, you can use the CPU-only version (smaller):

```powershell
pip install torch torchvision torchaudio
```

However, generation will be slower.

### Internet Requirements

After initial setup, kokoro works offline except:
- First time using a new voice (downloads ~523 KB)
- Model updates (rare)

### GPU Acceleration

If you have an NVIDIA GPU with CUDA support, PyTorch will automatically use it for faster generation. No additional configuration needed.

## Getting Help

- **CLI Issues**: [GitHub Issues](https://github.com/JeromeRGero/kokoro-cli/issues)
- **Model Issues**: [Kokoro GitHub](https://github.com/hexgrad/kokoro)
- **Voice Samples**: [HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)

## Version Information

This guide was written for:
- Windows 10/11
- Python 3.13+
- PowerShell 5.1+
- kokoro 0.9.4
- misaki 0.9.4

Last updated: November 2025
