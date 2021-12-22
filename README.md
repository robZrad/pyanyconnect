# pyAnyconnect

Simple application allowing to use Cisco AnyConnect using password stored in MacOS keychain.

![](images/showcase.gif)

1. Click Connect
2. Approve connection in MFA app on your phone and... voilà - you are connected!

## Prerequisites
1. Cisco Anyconnect installed. Path to the command is configurable via [.pyanyconnect file](./.pyanyconnect)
2. Password stored in keychain under "pyAnyconnect Password" name (it is hardcoded in app) using following command:
```
security add-generic-password -s "pyAnyconnect Password" -a $(whoami) -w
```
If you want to update your password record, you have to first remove the old one:
```
security delete-generic-password -s "pyAnyconnect Password" -a $(whoami)
security add-generic-password -s "pyAnyconnect Password" -a $(whoami) -w
```
3. pyanyconnect assumes existence of multiple hosts returned by vpn command. It filters the list using preferred_host value taken from [.pyanyconnect file](./.pyanyconnect)
4. [.pyanyconnect file](./.pyanyconnect) needs to be copied to the user `$HOME` folder and adapted to your needs

### Building from sources
1. Install python3
2. Install rumps and py2app: e.g.
```
pip3 install rumps py2app --user`
```
3. Build the app with:
```
python3 setup.py py2app
```
1. After successfull build binary will be placed in the [dist folder](./dist)

### Running
#### Script from console
1. You can try it by just running `./pyanyconnect.py` directly. You may examine console output for any issues.
#### Binary on login
1. Build binary, and copy `./dist/pyanyconnect.app` to the `/Applications` folder
2. Add it MacOS login items via: System Preferences -> Users & Groups -> Login items