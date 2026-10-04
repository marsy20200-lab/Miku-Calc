[app]
title = Micu Calc
package.name = micucalc
package.domain = org.miku
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = *.png,*.jpg,*.jpeg
version = 0.1

# Требования к библиотекам
requirements = python3,kivy==master,pillow

# Настройки Android
orientation = portrait
android.use_androidx = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_apk_rescale = 1

[buildozer]
log_level = 2
warn_on_root = 1
