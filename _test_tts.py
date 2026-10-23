import edge_tts, asyncio, subprocess, sys, os
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FF = str(Path('.venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'))

# Test ffmpeg version
r = subprocess.run([FF, '-version'], capture_output=True, text=True, timeout=10)
print('ffmpeg rc:', r.returncode)
print('ffmpeg out:', (r.stdout or '')[:200])

# Generate test audio
async def speak():
    c = edge_tts.Communicate('Hello world test narration', 'en-US-GuyNeural')
    await c.save('_test_tts.mp3')
asyncio.run(speak())

# Check audio file
p = Path('_test_tts.mp3')
print(f'audio file exists: {p.exists()}, size: {p.stat().st_size if p.exists() else 0}')

# Get duration with ffmpeg
r2 = subprocess.run([FF, '-i', '_test_tts.mp3'], capture_output=True, text=True, timeout=10)
dur_line = [l for l in (r2.stderr or '').splitlines() if 'Duration' in l]
print('duration line:', dur_line[0] if dur_line else 'not found')

# Re-encode
r3 = subprocess.run([FF, '-y', '-i', '_test_tts.mp3', '-ar', '44100', '-ac', '2', '-b:a', '128k', '_test_re.mp3'], capture_output=True, text=True, timeout=10)
print(f're-encode rc: {r3.returncode}')
if r3.returncode != 0:
    print(f're-encode stderr: {(r3.stderr or "")[-400:]}')

# Cleanup
for f in ['_test_tts.mp3', '_test_re.mp3']:
    try: Path(f).unlink()
    except: pass
