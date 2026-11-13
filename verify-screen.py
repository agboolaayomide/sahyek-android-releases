"""Verify actual rendered emulator evidence, not incomplete WebView accessibility nodes."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

root = Path('release')
nodes = list(ET.parse(root / 'emulator-window.xml').getroot().iter('node'))
assert any(n.get('class') == 'android.webkit.WebView' and n.get('package') == 'live.sahyekfootball.app' for n in nodes), 'Native WebView missing'
assert not any(n.get('resource-id', '').startswith(('com.android.chrome:id/', 'com.chrome.beta:id/')) for n in nodes), 'External browser UI detected'

def rendered_text(name):
    result = subprocess.run(['tesseract', str(root / name), 'stdout'], capture_output=True, text=True, check=True)
    return result.stdout.lower()

launch = rendered_text('emulator-launch.png')
assert 'welcome' in launch and 'email' in launch, 'Live account screen not rendered'
scrolled = rendered_text('emulator-scrolled.png')
assert 'password' in scrolled and 'email' in scrolled, 'Sign-in controls not reachable'
print('Rendered hosted account and reachable sign-in controls verified inside native WebView; no browser toolbar')
