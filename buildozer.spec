[app]
title = Lyra Moon AI
package.name = lyramoonai
package.domain = com.taqi.lyra
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Dependencies required for Android
requirements = python3,kivy,g4f,requests,urllib3,certifi,charset-normalizer,idna,asyncio

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android NDK / SDK configuration
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
