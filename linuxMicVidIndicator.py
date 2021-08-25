import gi, os, subprocess, signal, glob, re, threading

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, AppIndicator3, GObject
from gi.repository import Notify as notify

APPINDICATOR_ID = 'linuxMicIndicator'

assetsPath = os.path.dirname(os.path.realpath(__file__)) + "/assets/"

def getIcon(type, status):
    return assetsPath + type + "_" + status + ".png"

def getAnimated(type, frameStart):
    return assetsPath + type + "_" + str(frameStart).zfill(4) + ".png"

def getStatus():
    return re.findall("\[(on|off)\]", str(subprocess.check_output("amixer get Capture", shell=True)))[0]

class Indicator():
    def __init__(self):
        self.type = "mic"
        self.toggleStatus = getStatus()
        self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID + "-" + self.type, getIcon(self.type, self.toggleStatus), AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)

    def animate(self, type, frameStart, frameEnd):
        icon = getAnimated(self.type, frameStart)
        if int(frameStart) < int(frameEnd)+1:
            frameStart = str(int(frameStart)+1)
            self.indicator.set_icon(icon)
            GObject.timeout_add(30, self.animate, type, frameStart, frameEnd)

    def checkStatus(self):
        toggle = subprocess.check_output("amixer get Capture", shell=True)
        toggle = re.findall("\[(on|off)\]", str(toggle))[0]
        if self.toggleStatus != toggle:
            if toggle == "off":
                self.animate(toggle, 0, 8)
            elif toggle == "on":
                self.animate(toggle, 10, 18)
            self.toggleStatus = toggle
        GObject.timeout_add(100, self.checkStatus)

    def build_menu(self):
        menu = Gtk.Menu()
        menu.show_all()
        self.checkStatus()
        return menu

    def quit(self, source):
        Gtk.main_quit()


class Indicator2():
    def __init__(self):
        self.type = "vid"
        self.toggleStatus = getStatus()
        self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID + "-" + self.type, getIcon(self.type, self.toggleStatus), AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)

    def animate(self, type, frameStart, frameEnd):
        icon = getAnimated(self.type, frameStart)
        if int(frameStart) < int(frameEnd)+1:
            frameStart = str(int(frameStart)+1)
            self.indicator.set_icon(icon)
            GObject.timeout_add(30, self.animate, type, frameStart, frameEnd)

    def checkStatus(self):
        check = ""
        try:
            check = str(subprocess.check_output("fuser /dev/video0", shell=True))
        except:
            pass

        print(check)
        if check == "":
            toggle = "off"
        else:
            toggle = "on"

        if self.toggleStatus != toggle:
            if toggle == "off":
                self.animate(toggle, 0, 8)
            elif toggle == "on":
                self.animate(toggle, 10, 18)
            self.toggleStatus = toggle
        GObject.timeout_add(1000, self.checkStatus)

    def build_menu(self):
        menu = Gtk.Menu()
        menu.show_all()
        self.checkStatus()
        return menu

    def quit(self, source):
        Gtk.main_quit()

Indicator()
Indicator2()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gui_thread = threading.Thread(target=Gtk.main)
gui_thread.start()
