Note: Appium Server needs to be started separately, which is convenient for distributed deployment.
Start method: run run_server.py

Solve the problem of installing various APKs every time,

File: /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/lib/driver.js, comment out the following lines of code
await this.adb.uninstallApk (this.opts.appPackage);
await helpers.installApkRemotely (this.adb, this.opts);
await helpers.resetApp (this.adb, this.opts.app, this.opts.appPackage, this.opts.fastReset);
await this.checkPackagePresent ();

File: /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/build/lib/driver.js Comment the following lines of code
return _regeneratorRuntime.awrap (_androidHelpers2 ['default']. resetApp (this.adb, this.opts.app, this.opts.appPackage, this.opts.fastReset));
return _regeneratorRuntime.awrap (this.adb.uninstallApk (this.opts.appPackage));
return _regeneratorRuntime.awrap (_androidHelpers2 ['default']. installApkRemotely (this.adb, this.opts));
return _regeneratorRuntime.awrap (this.checkPackagePresent ());

File: /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/lib/android-helpers.js Comment the following lines of code
await adb.install (unicodeIMEPath, false);
await helpers.pushSettingsApp (adb);
await helpers.pushUnlock (adb);

The file /usr/local/lib/node_modules/appium/node_modules/appium-android-driver/build/lib/android-helpers.js replace the following lines of code
return _regeneratorRuntime.awrap (helpers.initUnicodeKeyboard (adb)) replaced with return context $ 1 $ 0.abrupt ('return', defaultIME);
return _regeneratorRuntime.awrap (helpers.pushSettingsApp (adb)); Replace with return context $ 1 $ 0.abrupt ('return', defaultIME);
return _regeneratorRuntime.awrap (helpers.pushUnlock (adb)); Replace with return context $ 1 $ 0.abrupt ('return', defaultIME);
