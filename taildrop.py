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
        subprocess.Popen(['tailscale', 'file', 'cp', path, host + ':'])

    @staticmethod
    def get_file(path='.'):
        """
        Invoke the tailscale binary to receive a file.
        """
        subprocess.Popen(['tailscale', 'file', 'get', path])


class TaildropMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    """
    Menu Provider for Taildrop
    """
    def __init__(self):
        pass

    @staticmethod
    def callback_recv(_menu, directory):
        """
        Callback handler for receiving files.
        """
        filename = unquote(directory.get_uri()[7:])
        Taildrop.get_file(filename)
        # hack, stolen from:
        # https://github.com/brunonova/nautilus-hide/blob/master/extension/nautilus-hide.py#L124
        subprocess.Popen(['xdotool', 'key', 'F5'])

    @staticmethod
    def callback_send(_menu, hostname, files):
        """
        Callback Handler for sending files to a host.
        """
        for file in files:
            filename = unquote(file.get_uri()[7:])
            Taildrop.send_file(filename, hostname)

    def get_file_items(self, _window, files):
        """
        Right click context menu for a batch of files.
        """
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
                TaildropMenuProvider.callback_send, details['hostname'], files
            )
            submenu.append_item(sub_menuitem)

        return (top_menuitem,)

    def get_background_items(self, window, file):
        """
        Adds the context menu to a folder.
        """
        top_menuitem = Nautilus.MenuItem(
            name='TaildropMenuProvider::BackgroundRecieve',
            label='Taildrop Receive',
            tip='',
            icon=''
        )
        top_menuitem.connect(
            'activate',
            TaildropMenuProvider.callback_recv, file
        )

        return (top_menuitem,)
