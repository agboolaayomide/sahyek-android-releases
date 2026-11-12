from pathlib import Path
import runpy
runpy.run_path('prepare-base.py')
res=Path('android/app/src/main/res')
p=res/'values/styles.xml'
p.write_text(p.read_text().replace('<item name="android:forceDarkAllowed">false</item>',''))
v29=res/'values-v29'
v29.mkdir(exist_ok=True)
(v29/'styles.xml').write_text('<resources><style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar"><item name="windowActionBar">false</item><item name="windowNoTitle">true</item><item name="android:windowBackground">@color/club_navy</item><item name="android:forceDarkAllowed">false</item></style></resources>')
