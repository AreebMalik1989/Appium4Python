# appium_pyton_android
Inherit and encapsulate appium, Android mobile terminal automated testing framework.
Support multiple devices to run testcase concurrently, direct error log and screenshot function, HTML output test report, etc.

## Brief introduction of usage:
* Please add test package and device information to config.yaml before running
    * NiceAPK: /Users/xxxxx/xxx.apk # Path of the test package
    * Devices:
        * deviceid: 5HUC9S6599999999 # device recognizes the value of adb devices
        * devicename: OPPO_R9M # The name of the device, used to distinguish
        * serverport: 4723 # -p Appium's main port, cannot be repeated between devices
        * bootstrapport: 4823 # -bp Appium bootstrap port, cannot be repeated between devices
        * platformname: Android    # desired_caps
        * platformversion: 5.1    # desired_caps
        * server: 127.0.0.1 # address
* Test cases, two reference use cases are kept under the testcase directory, one of which is the real use case test com.nice.main  
* After connecting all devices, run run_server_appium to start the appium server
* After the appium server is started, run run_server_http
* Select the type to be run: automated test or monkey test
* If you have any suggestions, please email areeb.malik1989@gmail.com

### Credits
* [h080294/appium_python_android](https://github.com/h080294/appium_python_android)

### Todo
* Translate or remove testresult dir
* generate_html_test_result method implementation of TheTestResult.py
* Translate prepro dir
