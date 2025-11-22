# Installation Guide

Detailed installation instructions for Kokoro TTS CLI on all platforms.

## Table of Contents

- [Windows (Python 3.13+)](#windows-python-313)
- [Windows (Python 3.12 and below)](#windows-python-312-and-below)
- [macOS](#macos)
- [Linux](#linux)
- [Troubleshooting](#troubleshooting)

---

## Windows (Python 3.13+)

Python 3.13 is very new, and some dependencies aren't available as pre-built packages on PyPI yet. We need to install from GitHub sources.

### Prerequisites

- Windows 10 or later
- ~3.5 GB free disk space for dependencies
- Internet connection for downloading models

### Step-by-Step Installation

#### 1. Install Python 3.13

1. Download Python 3.13 from [python.org](https://www.python.org/downloads/)
2. **Important**: Check **"Add Python to PATH"** during installation
3. Verify installation:
   ```powershell
   python --version
   ```
   Should show: `Python 3.13.x`

#### 2. Install Git

1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Use default installation settings
3. Verify:
   ```powershell
   git --version
   ```

#### 3. Clone the Repository

```powershell
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli
```

#### 4. Install PyTorch

Install PyTorch with CUDA support for GPU acceleration (~2.8 GB download):

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

⏱️ **Time estimate**: 5-10 minutes depending on internet speed.

**Note**: For CPU-only installation (smaller, but slower):
```powershell
pip install torch torchvision torchaudio
```

#### 5. Install Core Dependencies

```powershell
pip install soundfile sounddevice huggingface_hub loguru transformers scipy
```

⏱️ **Time estimate**: 2-3 minutes

**Note**: `sounddevice` enables audio playback directly in the terminal without opening media player windows.

#### 6. Install spaCy

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

#### 8. Install Misaki from GitHub

The latest misaki version (text-to-phoneme conversion) is only available on GitHub:

```powershell
pip install git+https://github.com/hexgrad/misaki.git -c constraints.txt
```

⏱️ **Time estimate**: 1-2 minutes

#### 9. Clone and Install Kokoro

```powershell
cd ..
git clone https://github.com/hexgrad/kokoro.git
pip install .\kokoro -c kokoro-cli\constraints.txt
```

⏱️ **Time estimate**: 1-2 minutes

#### 10. Clean Up and Test

```powershell
del kokoro-cli\constraints.txt
cd kokoro-cli
python kokoro-tts.py --michael "Hello world"
```

✅ If successful, you should hear "Hello world" and find a WAV file in `C:\Users\YourName\kokoro-audio\`

### Why These Steps?

- PyPI versions of kokoro don't support Python 3.13 yet
- GitHub source versions have Python 3.13 support
- Constraints prevent spaCy from upgrading to dev versions that fail to build on Windows

---

## Windows (Python 3.12 and below)

Installation is much simpler for Python 3.12 and earlier!

### Prerequisites

- Windows 10 or later
- Python 3.10-3.12

### Installation

```powershell
# Install dependencies
pip install kokoro soundfile sounddevice

# Clone the repository
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli

# Test
python kokoro-tts.py --michael "Hello world"
```

That's it! ✅

---

## macOS

### Prerequisites

- macOS 10.14 or later
- Python 3.7+ (usually pre-installed)

### Installation

#### Simple Installation

```bash
# Install dependencies
pip3 install kokoro soundfile

# Download the script
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py

# Make it executable
chmod +x kokoro-tts.py

# Test
python3 kokoro-tts.py --michael "Hello world"
```

#### Installation with Global Command

```bash
# Install dependencies
pip3 install kokoro soundfile

# Download to home directory
cd ~
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py
chmod +x kokoro-tts.py

# Create global command
mkdir -p ~/bin
cat > ~/bin/kokoro << 'EOF'
#!/bin/bash
exec python3 "$HOME/kokoro-tts.py" "$@"
EOF
chmod +x ~/bin/kokoro

# Add to PATH (for zsh)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Or for bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Test
kokoro --michael "Hello world"
```

---

## Linux

### Prerequisites

- Any modern Linux distribution
- Python 3.7+
- Audio player: `paplay`, `aplay`, `ffplay`, or `mpv`

### Installation

#### Simple Installation

```bash
# Install dependencies
pip3 install kokoro soundfile

# Download the script
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py

# Make it executable
chmod +x kokoro-tts.py

# Test
python3 kokoro-tts.py --michael "Hello world"
```

#### Install Audio Player (if needed)

```bash
# Ubuntu/Debian
sudo apt install pulseaudio-utils

# Fedora/RHEL
sudo dnf install pulseaudio-utils

# Arch Linux
sudo pacman -S pulseaudio
```

#### Installation with Global Command

```bash
# Install dependencies
pip3 install kokoro soundfile

# Download to home directory
cd ~
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py
chmod +x kokoro-tts.py

# Create global command
mkdir -p ~/bin
cat > ~/bin/kokoro << 'EOF'
#!/bin/bash
exec python3 "$HOME/kokoro-tts.py" "$@"
EOF
chmod +x ~/bin/kokoro

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Test
kokoro --michael "Hello world"
```

---

## Troubleshooting

### Python/Installation Issues

#### "python is not recognized" or "pip is not recognized" (Windows)

Python wasn't added to PATH during installation. Solutions:
1. Reinstall Python and check **"Add Python to PATH"**
2. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Add `C:\Users\YourName\AppData\Local\Programs\Python\Python313` to PATH

#### "git is not recognized" (Windows)

Install Git for Windows from [git-scm.com](https://git-scm.com/download/win).

#### Build errors: blis, spaCy, curated-tokenizers (Windows)

This happens when pip tries to build packages from source. Solution:
1. Use the [Python 3.13+ installation steps](#windows-python-313)
2. The constraints file locks spaCy version to prevent dev versions
3. Installing from GitHub sources provides pre-built support

#### "ModuleNotFoundError: No module named 'kokoro'"

Install the dependencies:
```bash
# Python 3.12 and below
pip install kokoro soundfile

# Python 3.13+ (Windows)
# Follow the full installation steps above
```

#### "TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'"

Your misaki version is outdated. Install the latest from GitHub:
```bash
pip install --upgrade git+https://github.com/hexgrad/misaki.git
```

### Audio Issues

#### Audio doesn't play

The audio file is always saved, even if playback fails. Play it manually:

**macOS:**
```bash
afplay ~/kokoro-audio/kokoro_*.wav
```

**Linux:**
```bash
mpv ~/kokoro-audio/kokoro_*.wav
# or
paplay ~/kokoro-audio/kokoro_*.wav
```

**Windows:**
- Double-click the WAV file in File Explorer
- Or: `explorer C:\Users\YourName\kokoro-audio`

**Fix for Windows:**
```powershell
pip install sounddevice
```

#### Audio plays in a new window instead of terminal (Windows)

Install `sounddevice` for seamless terminal playback:
```powershell
pip install sounddevice
```

### Performance Issues

#### First run is very slow / downloads files

This is **normal**! The first run downloads:
- Kokoro TTS model (~327 MB) - one time only
- Voice model files (~523 KB per voice) - cached after first use
- spaCy English model (~12 MB) - one time only

All files are cached locally. Subsequent runs will be much faster (usually < 5 seconds).

#### Generation is slow (Windows)

If you installed CPU-only PyTorch, generation will be slower. For GPU acceleration:
```powershell
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Requires an NVIDIA GPU with CUDA support.

### Permission Issues

#### "Permission denied" (macOS/Linux)

Make sure the script is executable:
```bash
chmod +x kokoro-tts.py
```

#### "Access denied" during installation (Windows)

Run PowerShell as Administrator:
1. Search "PowerShell" in Start Menu
2. Right-click → "Run as Administrator"
3. Run the installation commands

### Command Not Found

#### "kokoro: command not found" (macOS/Linux)

Restart your terminal or reload your shell configuration:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

#### "WARNING: scripts not on PATH" (Windows)

This is just a warning and doesn't affect functionality. You can safely ignore it, or add the Scripts directory to PATH:

```powershell
$ScriptsPath = "$env:APPDATA\Python\Python313\Scripts"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$ScriptsPath", "User")
```

---

## Uninstallation

### Windows

```powershell
# Remove repositories
cd ~
rmdir -Recurse -Force kokoro-cli
rmdir -Recurse -Force kokoro

# Remove audio output folder
rmdir -Recurse -Force $HOME\kokoro-audio

# Uninstall packages
pip uninstall kokoro misaki soundfile torch -y

# Remove cached models (optional, saves ~340 MB)
rmdir -Recurse -Force $HOME\.cache\huggingface
```

### macOS/Linux

```bash
# Remove files
rm ~/kokoro-tts.py
rm ~/bin/kokoro
rm -rf ~/kokoro-audio

# Uninstall packages
pip3 uninstall kokoro soundfile -y

# Remove cached models (optional, saves ~340 MB)
rm -rf ~/.cache/huggingface
```

---

## Additional Information

### Internet Requirements

After initial setup, kokoro works offline except:
- First time using a new voice (downloads ~523 KB per voice)
- Model updates (rare)

### GPU Acceleration (Windows)

If you have an NVIDIA GPU with CUDA support, PyTorch will automatically use it for faster generation. No additional configuration needed.

To verify GPU is being used, you'll notice:
- Faster audio generation (especially for long texts)
- First run shows "CUDA available: True"

### File Locations

**macOS/Linux:**
- Script: `~/kokoro-tts.py`
- Global command: `~/bin/kokoro` (if configured)
- Audio output: `~/kokoro-audio/`
- Model cache: `~/.cache/huggingface/`

**Windows:**
- Script: `C:\Users\YourName\kokoro-cli\kokoro-tts.py`
- Audio output: `C:\Users\YourName\kokoro-audio\`
- Model cache: `C:\Users\YourName\.cache\huggingface\`

---

## Getting Help

- **CLI Issues**: [GitHub Issues](https://github.com/JeromeRGero/kokoro-cli/issues)
- **Model Issues**: [Kokoro GitHub](https://github.com/hexgrad/kokoro)
- **Voice Samples**: [HuggingFace Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)

---

**Back to**: [README.md](README.md)

