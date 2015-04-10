import re
import json

import requests
import websocket
from anybar import AnyBar


class ButtonIndicator(object):
    """Class to watch Reddit's /r/thebutton and update AnyBar."""

    headers = {'user-agent': 'Button_Visualizer_app/0.1.0'}

    BUTTON_COLORS = {
        52: 'purple',
        42: 'blue',
        32: 'green',
        22: 'yellow',
        12: 'orange',
        0: 'red'
    }

    def __init__(self, anybar_port=None):
        """Create ButtonInidicator

        Args:
        -----
        anybar_port : Optional port to use for AnyBar
        """
        if anybar_port:
            self.anybar = AnyBar(anybar_port)
        else:
            self.anybar = AnyBar()
        self.entered = False

    def __enter__(self):
        """Create context manager that allows safe polling."""
        socket_url = self.get_websocket_url()
        self.ws = self.connect_to_socket(socket_url)
        self.entered = True
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def run(self):
        """Poll webserver and update anybar."""
        if not self.entered:
            with self as s:
                s.run()

        for time in self.read_socket_data():
            self.set_anybutton_color(time)

    def cleanup(self):
        """Close port and reset AnyBar to default (white)."""
        self.entered = False
        if hasattr(self, 'ws'):
            self.ws.close()
            del self.ws
            print "Socket closed"

        self.anybar.change('white')

    @classmethod
    def get_websocket_url(cls):
        """Scan reddit page for websocket url."""
        url = "http://www.reddit.com/r/thebutton"
        r = requests.get(url, headers=cls.headers)

        if r.ok:
            pattern = r'"(wss://wss.redditmedia.com/thebutton\?h=[^"]*)'
            found = re.search(pattern, r.content)
            if found:
                return found.group(1)
        return None

    def connect_to_socket(self, socket_url):
        """Create client connection to websocket."""
        ws = websocket.create_connection(socket_url)
        print "Successfully connected to socket: {}".format(socket_url)
        return ws

    def read_socket_data(self):
        """Iterator to read data from websocket."""
        if not hasattr(self, 'ws'):
            raise Exception("Websocket not created.")
        try:
            while True:
                result = json.loads(self.ws.recv())
                yield result['payload']['seconds_left']
        except:
            return

    def set_anybutton_color(self, time):
        """Update AnyButton with current colour or exclamation on error."""
        color_index = max([k for k in self.BUTTON_COLORS if time >= k] or 0)
        color = self.BUTTON_COLORS.get(color_index, "exclamation")
        self.anybar.change(color)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="/r/TheButton notifier")
    parser.add_argument('port',
                        type=int,
                        nargs='?',
                        help='Anybutton port to use')

    args = parser.parse_args()

    ButtonIndicator(args.port).run()
