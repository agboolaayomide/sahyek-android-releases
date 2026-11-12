import datetime,hashlib,json,os,pathlib,re,subprocess,zipfile
apk=pathlib.Path(os.environ['APK_PATH']);tools=pathlib.Path(os.environ['ANDROID_HOME'])/'build-tools/36.0.0'
with zipfile.ZipFile(apk) as z:
 assert {'AndroidManifest.xml','classes.dex','resources.arsc'}.issubset(z.namelist())
 assert z.testzip() is None
 assert any(n.startswith('res/') and n.endswith('.png') for n in z.namelist()), 'Native imagery missing from APK'
sig=subprocess.check_output([str(tools/'apksigner'),'verify','--verbose','--print-certs',str(apk)],text=True)
cert=re.search(r'Signer #1 certificate SHA-256 digest: ([a-fA-F0-9]{64})',sig)
assert cert and cert.group(1).lower()==os.environ['ANDROID_SIGNING_CERT_SHA256'].lower()
b=subprocess.check_output([str(tools/'aapt'),'dump','badging',str(apk)],text=True)
resources=subprocess.check_output([str(tools/'aapt'),'dump','resources',str(apk)],text=True)
assert 'club_launcher_foreground' in resources and 'club_navy' in resources, 'Native splash resources missing from compiled resource table'
p=re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'",b)
m=re.search(r"sdkVersion:'(\d+)'",b)
assert p and m and p.group(1)=='live.sahyekfootball.app' and p.group(2)=='3' and p.group(3)=='1.0.2' and m.group(1)=='24'
assert "application-label:'SAHYEK F.C.'" in b
meta=dict(packageId=p.group(1),version=p.group(3),versionCode=3,minSdk=24,sizeBytes=apk.stat().st_size,releasedAt=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),sha256=hashlib.sha256(apk.read_bytes()).hexdigest(),certificateSha256=cert.group(1).lower(),fileName=apk.name,signatureVerified=True)
(apk.parent/'android-release.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))
