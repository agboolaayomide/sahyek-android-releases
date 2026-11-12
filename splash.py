from pathlib import Path
from PIL import Image
import json
res=Path('android/app/src/main/res')
p=Path('android/app/build.gradle');p.write_text(p.read_text().replace('versionName "1.0.0"','versionName "1.0.1"').replace('versionCode 1','versionCode 2'))
im=Image.open('www/club-icon.png').convert('RGBA')
for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 canvas=Image.new('RGBA',(round(size*2.25),round(size*2.25)),(0,0,0,0));logo=im.copy();logo.thumbnail((size,size));canvas.paste(logo,((canvas.width-logo.width)//2,(canvas.height-logo.height)//2),logo);canvas.save(res/('drawable-'+density)/'club_launcher_foreground.png')
(res/'values/club_colors.xml').write_text('<resources><color name="club_cream">#fff9dc</color><color name="club_navy">#05223f</color></resources>')
p=res/'values/styles.xml';p.write_text(p.read_text().replace('@color/club_cream','@color/club_navy').replace('<item name="windowNoTitle">true</item>','<item name="windowNoTitle">true</item><item name="android:windowBackground">@color/club_navy</item>'))
for name in ['ic_launcher','ic_launcher_round']:
 p=res/'mipmap-anydpi-v26'/(name+'.xml');p.write_text(p.read_text().replace('@color/club_cream','@color/club_navy'))
p=Path('android/app/src/main/java/live/sahyekfootball/app/MainActivity.java');p.write_text(p.read_text().replace('super.onCreate(state);','super.onCreate(state);\n  findViewById(android.R.id.content).setBackgroundColor(getColor(live.sahyekfootball.app.R.color.club_navy));\n  getBridge().getWebView().setBackgroundColor(getColor(live.sahyekfootball.app.R.color.club_navy));'))
