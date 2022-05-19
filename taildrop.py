#!/usr/bin/env python3
"""
Taildrop support for Nautilus.
"""
import json
import subprocess

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

from gi.repository import Nautilus, GObject


class Taildrop:
    """
    Wrappers around taildrop.
    """
    @staticmethod
    def find_hosts():
        """
        Discover the tailscale hosts that are online.
        """
        process = subprocess.run(
            ['tailscale', 'status', '--json'],
            capture_output=True,
            check=False
        )
        status = json.loads(process.stdout)
        items = []
        for _host, data in status['Peer'].items():
            items.append({
                'hostname': data['HostName'],
                'os': data['OS'],
                'online': data['Online']
            })

        return items

    @staticmethod
    def send_file(path, host):
        """
        Invoke the tailscale binary to send a file.
        """
        subprocess.run(
            ['tailscale', 'file', 'cp', path, host + ':'],
            check=False
        )

    @staticmethod
    def get_file(path='.'):
        """
        Invoke the tailscale binary to receive a file.
        """
        subprocess.run(
            ['tailscale', 'file', 'get', path],
            check=False
        )


class TaildropMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    """
    Menu Provider for Taildrop
    """
    def __init__(self):
        pass

    def callback(self, _menu, hostname, files):
        """
        Callback Handler
        """
        for file in files:
            filename = unquote(file.get_uri()[7:])
            print(filename)
            Taildrop.send_file(filename, hostname)

    def get_file_items(self, window, files):
        top_menuitem = Nautilus.MenuItem(
            name='TaildropMenuProvider::Devices',
            label='Taildrop',
            tip='',
            icon=''
        )

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        for idx, details in enumerate(Taildrop.find_hosts()):
            if not details['online']:
                continue

            sub_menuitem = Nautilus.MenuItem(
                name='TaildropMenuProvider::Device%i' % idx,
                label="%s - %s" % (details['hostname'], details['os']),
                tip='',
                icon=''
            )
            sub_menuitem.connect(
                'activate',
                self.callback, details['hostname'], files
            )
            submenu.append_item(sub_menuitem)

        return (top_menuitem,)

    def get_background_items(self, window, file):
        """
        Tbh not quite sure what this one does, but it's a thing.

        And yep, seems this does have to be a repeated copy of the above
        function.
        """
        top_menuitem = Nautilus.MenuItem(
            name='TaildropMenuProvider::BDevices',
            label='Taildrop',
            tip='',
            icon=''
        )

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        for idx, details in enumerate(Taildrop.find_hosts()):
            if not details['online']:
                continue

            sub_menuitem = Nautilus.MenuItem(
                name='TaildropMenuProvider::BDevice%i' % idx,
                label="%s - %s" % (details['hostname'], details['os']),
                tip='',
                icon=''
            )
            sub_menuitem.connect(
                'activate',
                self.callback, details['hostname'], [file]
            )
            submenu.append_item(sub_menuitem)

        return (top_menuitem,)
