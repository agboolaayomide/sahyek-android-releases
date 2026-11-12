import xml.etree.ElementTree as E
from pathlib import Path
nodes=list(E.parse('release/emulator-window.xml').getroot().iter('node'))
assert any(n.get('class')=='android.webkit.WebView' and n.get('package')=='live.sahyekfootball.app' for n in nodes), 'Not running in the native Capacitor WebView'
assert not any(n.get('resource-id') in ['com.android.chrome:id/url_bar','com.android.chrome:id/toolbar','com.chrome.beta:id/url_bar'] for n in nodes), 'Browser toolbar detected'
assert any('Sign in' in (n.get('text','')+n.get('content-desc','')) for n in nodes), 'Hosted sign-in screen did not finish loading'
print('Native WebView, no Chrome address bar, live sign-in screen verified')
