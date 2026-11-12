from pathlib import Path
from PIL import Image
p=Path('android/app/build.gradle')
s=p.read_text().replace('versionName "1.0"','versionName "1.0.2"').replace('versionCode 1','versionCode 3')
s=s.replace('    buildTypes {','''    signingConfigs {
        release {
            storeFile file(System.getenv("ANDROID_KEYSTORE_PATH"))
            storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
            keyAlias System.getenv("ANDROID_KEY_ALIAS")
            keyPassword System.getenv("ANDROID_KEY_PASSWORD")
        }
    }
    buildTypes {''').replace('        release {\n            minifyEnabled','        release {\n            signingConfig signingConfigs.release\n            minifyEnabled')
p.write_text(s)
p=Path('android/app/src/main/AndroidManifest.xml');p.write_text(p.read_text().replace('android:allowBackup="true"','android:allowBackup="false" android:usesCleartextTraffic="false"'))
im=Image.open('www/club-icon.png').convert('RGBA');res=Path('android/app/src/main/res')
for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    for name in ['ic_launcher','ic_launcher_round','ic_launcher_foreground']:
        dest=res/('mipmap-'+density)/(name+'.png');dest.parent.mkdir(exist_ok=True);im.resize((size,size),Image.Resampling.LANCZOS).save(dest)
    dest=res/('drawable-'+density);dest.mkdir(exist_ok=True)
    canvas=Image.new('RGBA',(int(size*2.25),int(size*2.25)),(0,0,0,0));logo=im.resize((size,size),Image.Resampling.LANCZOS);canvas.paste(logo,((canvas.width-size)//2,(canvas.height-size)//2),logo);canvas.save(dest/'club_launcher_foreground.png')
for name in ['ic_launcher','ic_launcher_round']:
    (res/'mipmap-anydpi-v26'/(name+'.xml')).write_text('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/club_navy"/><foreground android:drawable="@drawable/club_launcher_foreground"/></adaptive-icon>')
(res/'values/club_colors.xml').write_text('<resources><color name="club_cream">#fff9dc</color><color name="club_navy">#05223f</color></resources>')
p=res/'values/styles.xml';s=p.read_text().replace('@drawable/splash','@drawable/club_launcher_foreground').replace('<item name="windowSplashScreenBackground">@color/colorPrimary</item>','<item name="windowSplashScreenBackground">@color/club_navy</item>').replace('<item name="windowNoTitle">true</item>','<item name="windowNoTitle">true</item><item name="android:windowBackground">@color/club_navy</item>');p.write_text(s)
Path('android/app/src/main/java/live/sahyekfootball/app/MainActivity.java').write_text(Path('native/MainActivity.java').read_text())
Path('android/app/src/main/java/live/sahyekfootball/app/ClubRuntimePlugin.java').write_text(Path('native/ClubRuntimePlugin.java').read_text())
