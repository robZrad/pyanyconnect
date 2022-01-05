#!/usr/bin/env python3

import rumps
import subprocess
import getpass
import configparser
import os

host = ''

config = configparser.RawConfigParser()
config.read(os.path.expanduser('~') + '/.pyanyconnect')

def update_host():
    global host
    preferred_host = config['defaults']['preferred_host']
    print(f'Preferred host: {preferred_host}')
    hosts_command = [config['defaults']['vpn_command_path'], 'hosts']
    output = subprocess.run(hosts_command, shell=False, capture_output=True, check=True, text=True).stdout
    filtered = list(filter(lambda x: preferred_host in x, output.splitlines()))[0]
    index = filtered.index(">") + 2
    host = filtered[index:]
    print(f'Host set to {host}')

def update_state(app,vpn_button):
    update_host()
    state_command = [config['defaults']['vpn_command_path'], 'state']
    output = subprocess.run(state_command, shell=False, text=True, capture_output=True, check=True)
    if output.returncode == 0:
        if 'state: Connected' in output.stdout:
            print('Checking state... connected')
            app.title = "VPN: Connected"
            vpn_button.title = "Disconnect"
            vpn_button.set_callback(disconnect)
        elif 'state: Disconnected' in output.stdout:
            print('Checking state... disconnected')
            app.title = "VPN: Disconnected"
            vpn_button.title = "Connect"
            vpn_button.set_callback(connect)
        elif 'state: Reconnecting' in output.stdout:
            print('Checking state... reconnecting')
            app.title = "VPN: Reconnecting"
            vpn_button.title = "Connect"
            vpn_button.set_callback(connect)
        else:
            rumps.alert(f'Unexpected output:\n {output.stdout}')
    else:
        rumps.alert(f'Unexpected output:\n {output.stdout}')


@rumps.timer(10)
def periodic_check(sender):
    global vpn_button
    update_state(app, vpn_button)

def connect(sender):
    global app
    global host
    vpn_command = [config['defaults']['vpn_command_path'], 'connect', host, '-s']
    username=getpass.getuser()
    get_pass_command = ['security', 'find-generic-password', '-w', '-s','pyAnyconnect Password', '-a', username]
    password = subprocess.run(get_pass_command, text=True, capture_output=True).stdout.strip()
    input=f'''{username}
{password}
y'''
    # rumps.alert("Connecting, remember to confirm connection attempt in MFA app on your phone")
    sp = subprocess.run(vpn_command, text=True, input=input, capture_output=True)

    if sp.returncode != 0 or 'error' in sp.stdout:
        rumps.alert(f'Could not connect. Check logs for details.')
        print(sp.stdout)
    elif 'Login failed.' in sp.stdout:
        rumps.alert(f'Login failed, incorrect password? Check logs for details.')
        print(sp.stdout)
    update_state(app, sender)


def disconnect(sender):
    global app
    print("Disconnecting...")
    sp = subprocess.run([config['defaults']['vpn_command_path'],'disconnect'], shell=False, capture_output=False, check=True)
    update_state(app, sender)


callback = None

app = rumps.App('pyAnyconnect', quit_button=rumps.MenuItem('Quit pyAnyconnect', key='q'))
vpn_button = rumps.MenuItem('')

update_state(app, vpn_button)
app.menu.add(vpn_button)
app.run()
