import subprocess,xml.etree.ElementTree as E
from pathlib import Path
root=Path('release')
nodes=list(E.parse(root/'emulator-window.xml').getroot().iter('node'))
assert any(n.get('class')=='android.webkit.WebView' and n.get('package')=='live.sahyekfootball.app' for n in nodes), 'Native WebView missing'
assert not any(n.get('resource-id','').startswith(('com.android.chrome:id/','com.chrome.beta:id/')) for n in nodes), 'External browser UI detected'
text=subprocess.run(['tesseract',str(root/'emulator-launch.png'),'stdout'],capture_output=True,text=True,check=True).stdout.lower()
assert all(x in text for x in ['welcome','email','google']), 'Live account screen not rendered'
text=subprocess.run(['tesseract',str(root/'emulator-scrolled.png'),'stdout'],capture_output=True,text=True,check=True).stdout.lower()
assert 'sign in' in text and 'password' in text, 'Sign-in controls not reachable'
print('Rendered hosted account and sign-in controls verified inside native WebView; no browser toolbar')
