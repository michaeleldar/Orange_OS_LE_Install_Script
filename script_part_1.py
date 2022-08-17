"""\nThis program is an installer for Orange OS LE, you can find more information in the README\n    Copyright (C) 2022 Michael Halpin\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <https://www.gnu.org/licenses/>.\n'"""
_C='/sys/firmware/efi'
_B='{'
_A='}'
import sys,os
print('Welcome to the Orange OS LE 1.0.0-alpha install script.')
print('We will ask you a few questions to make sure you get a great configuration.')
hard_drive=input('Please input your disk drive file, like /dev/sda: ')
host_name=input('Please enter the name you want to give your computer (a.k.a your hostname): ')
keyboard_layout=input('Now enter your keyboard layout, like uk or us: ')
language=input('Now please enter your locale language. This should be something like "en_US": ')
time_zone=input('Now we need your timezone, this is usually in the format of <Continent>/<City>, e.g Europe/Paris: ')
location=input("Finally, we need to know what country you live in. If you don't want to anser this, enter worldwide.").capitalize()
with open('user_configuration.json','w')as user_config:user_config.write(f'''{_B}
"audio": "pipewire",
"bootloader": "grub-install",
"filesystem": "ext4",
"config_version": "2.5.0",
"debug": false,
"harddrives": [
    "{hard_drive}"
],
"kernels": [
    "linux"
],
"swap": true,
"keyboard-language": "{keyboard_layout}",
"mirror-region": "{location}",
"hostname": "{host_name}",
"keyboard-layout": "{keyboard_layout}",
"mount_point": null, 
"nic": {_B}
    "dhcp": true,
    "dns": null,
    "gateway": null,
    "iface": null,
    "ip": null,
    "type": "iso"
{_A},
"ntp": true,

"plugin": null,
"profile": {_B}
    "path": "/usr/lib/python3.10/site-packages/archinstall/profiles/minimal.py"
{_A},
"script": "guided",
"silent": false,
"sys-language": "{language}",
"sys-encoding": "utf-8",
"timezone": "{time_zone}",
"version": "2.5.0"
{_A}''')
print('Okay, now we are going to setup users for you.')
user_creds=open('user_credentials.json','w')
user_creds.write('{\n    "!users": [')
users_no=int(input('First, how many users do you want the system to hold: '))
for x in range(0,users_no):
	user_creds.write('{\n');username=input(f"Ok what the you want the username of user {x+1} to be: ");password=input(f"Now, what password do you want to give {username}: ");superuser=input(f"Lastly do you want {username} to be a superuser? Leave blank if you don't: ");user_creds.write(f'"!password": "{password}",\n')
	if superuser:user_creds.write('"sudo": true,\n')
	else:user_creds.write('"sudo": false,\n')
	user_creds.write(f'"username": "{username}"\n');user_creds.write(_A)
	if x==users_no-1:user_creds.write('\n')
	else:user_creds.write(',\n')
user_creds.write(']\n}')
user_creds.close()
print("Now we will setup the disks for you. Unfourtuanatley, we can't offer to let you")
print('do the disk partioning, but we might offer this in future.')
input("This will delete all data on the disk you have chosen,\nso if you don't want this, press Ctrl/Command C. Otherwise press enter. ")
user_disks=open('user_disk_layout.json','w')
user_disks.write(f'''{_B}
    "{hard_drive}": {_B}
        "partitions": [
            {_B}
                "boot": true,
                "encrypted": false,
                "filesystem": {_B}
                    "format": "fat32"
                {_A},
                "mountpoint": "/boot",
                "size": "{"203MiB"if not os.path.exists(_C)else"512MiB"}",
                "start": "{"3MiB"if not os.path.exists(_C)else"1MiB"}",
                "type": "primary",
                "wipe": true
            {_A},
            {_B}
                "encrypted": false,
                "filesystem": {_B}
                    "format": "ext4",
                    "mount_options": []
                {_A},
                "mountpoint": "/",
                "size": "100%",
                "start": "{"206MiB"if not os.path.exists(_C)else"513MiB"}",
                "type": "primary",
                "wipe": true
            {_A}
        ],
        "wipe": true
    {_A}
{_A}''')
user_disks.close()
os.system('sudo archinstall --config ./user_configuration.json --creds ./user_credentials.json --disk_layouts ./user_disk_layout.json')