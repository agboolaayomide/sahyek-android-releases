import json,pathlib
config=json.loads(pathlib.Path('android/app/google-services.json').read_text())
assert config['project_info']['project_id']=='football-f4a74', 'Android Firebase project differs from connected server sender'
assert any(c['client_info']['android_client_info']['package_name']=='live.sahyekfootball.app' for c in config['client']), 'Firebase Android registration must match release package'
print('Android Firebase project/package match verified')
