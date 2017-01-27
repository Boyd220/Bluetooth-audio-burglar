#!/usr/bin/python

from gi.repository import GObject

import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import optparse

justScan = False
justAudio = False

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

bus = None
device_obj = None
path = None

def set_trusted(path):
    props = dbus.Interface(bus.get_object("org.bluez", path),
            "org.freedesktop.DBus.Properties")
    props.Set("org.bluez.Device1", "Trusted", True)
    print("settings trusted")

def dev_connect(path):
    dev = dbus.Interface(bus.get_object("org.bluez", path),
            "org.bluez.Device1")
    dev.Connect()
def interfaces_added(path, interfaces):
    if "org.bluez.MediaControl1" in interfaces or "org.bluez.MediaTransport1" in interfaces:
        print("Detected MediaControl1")
    else:
        #print(interfaces)
        searchManager = dbus.Interface(bus.get_object("org.bluez", "/"),
                                                    "org.freedesktop.DBus.ObjectManager")
        objects = searchManager.GetManagedObjects()
        dev = objects[path]
        properties = dev["org.bluez.Device1"]

        if justAudio == True:
            for key in properties.keys():
                print("looping: " + key)
                value = properties[key]
                if key == "Icon":
                    print(value)
                    if value == "audio-card":
                        print("Found Audio device")
                        if justScan == False:
                            print("connecting to: " + path)
                            dev_connect(path)
        else:
            if justScan == False:
                print("connecting to: " + path)
                dev_connect(path)
                dev_connect(path)


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"

class Agent(dbus.service.Object):
    @dbus.service.method(AGENT_INTERFACE,
            in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print("RequestPinCode (%s)" % (device))
        return "0000"

    @dbus.service.method(AGENT_INTERFACE,
            in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print("RequestPasskey (%s)" % (device))
        set_trusted(device)
        return 0000

    @dbus.service.method(AGENT_INTERFACE,
            in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        print("DisplayPasskey (%s, %06u entered %u)" %
                (device, passkey, entered))

        @dbus.service.method(AGENT_INTERFACE,
                in_signature="os", out_signature="")
        def DisplayPinCode(self, device, pincode):
            print("DisplayPinCode (%s, %s)" % (device, pincode))

    @dbus.service.method(AGENT_INTERFACE,
            in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print("RequestConfirmation (%s, %06d)" % (device, passkey))
        return

    @dbus.service.method(AGENT_INTERFACE,
            in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print("RequestAuthorization (%s)" % (device))
        return

    @dbus.service.method(AGENT_INTERFACE,
            in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")
        dev_connect(path)


def pair_reply():
    print("Device paired")


def pair_error(error):
    err_name = error.get_dbus_name()
    if err_name == "org.freedesktop.DBus.Error.NoReply" and device_obj:
        print("Timed out. Cancelling pairing")
        device_obj.CancelPairing()
    else:
        print("Creating device failed: %s" % (error))


    mainloop.quit()

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    capability = "KeyboardDisplay"


    parser = optparse.OptionParser()
    parser.add_option('-s', action='store_true', default=False, dest='justScan', help="Scan devices")
    parser.add_option('-a', action='store_true', default=False, dest='justAudio', help="Only audio devices")

    options, args = parser.parse_args()

    justScan = options.justScan
    justAudio = options.justAudio


    path = "/test/agent"
    agent = Agent(bus, path)

    mainloop = GObject.MainLoop()

    obj = bus.get_object(BUS_NAME, "/org/bluez");
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(path, capability)

    print("Agent registered")

    bus.add_signal_receiver(interfaces_added,
            dbus_interface = "org.freedesktop.DBus.ObjectManager",
            signal_name = "InterfacesAdded")


    manager.RequestDefaultAgent(path)

    mainloop.run()
