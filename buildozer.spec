[app]
title = Micu Calc
package.name = micucalc
package.domain = org.miku
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = *.png,*.jpg,*.jpeg
version = 0.1

# (list) Application requirements
requirements = python3,kivy==master,pillow

# (str) Supported orientations
orientation = portrait

# (bool) Use AndroidX
android.use_androidx = 1

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk tools
android.skip_apk_rescale = 1

[buildozer]
log_level = 2
warn_on_root = 1
