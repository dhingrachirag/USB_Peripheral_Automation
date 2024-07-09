#Author : Chirag Dhingra
#Email-id : dhingrachirag@hotmail.com
#Time: 14:48:00
from msvcrt import kbhit
from time import sleep
from pywinusb import hid
import sys
from contextlib import contextmanager


@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout

class DataManager:
    def __init__(self):
        self.vid = []
        self.pid = []
        self.not_useful_tests = []
        self.Initiate()


    def Initiate(self):
            print "#################"
            print('USB HID VALIDATOR')
            print "#################"
            print "\n"
            all_hids = hid.find_all_hid_devices()
            if all_hids:
                while True:
                    print("Choose a device to monitor operations:\n")
                    print("0 => Exit")
                    for index, device in enumerate(all_hids):
                        device_name = unicode("{0.vendor_name} {0.product_name}" \
                                              "(vID=0x{1:04x}, pID=0x{2:04x})" \
                                              "".format(device, device.vendor_id, device.product_id))
                        x = unicode("0x{1:04x}"
                                    "".format(device, device.vendor_id))
                        self.vid.append(int(x,16))
                        y = unicode("0x{1:04x}"
                                    "".format(device, device.product_id))
                        self.pid.append(int(y,16))
                        print("{0} => {1}".format(index + 1, device_name))
                    print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                          "[press enter after number]:" % len(all_hids))
                    index_option = raw_input()
                    print "##################################################"
                    print('CHOOSE THE OPERATION YOU WANT TO TEST')
                    print "##################################################"
                    print "\n"
                    if index_option.isdigit() and int(index_option) <= len(all_hids):
                        #
                        break;
                int_option = int(index_option)
                if int_option:
                    device = all_hids[int_option - 1]
                    try:
                        print "1 To Check whether device is ASP(Accessory Signailing Protocol) supported or not\n2 To get all HID information of the device\n3 To test mute functionality of device\n4 To test hook switch functionality of device\n5 To test Flash usage functionality of device\n6 To test Speed Dial usage functionality of device\n7 To test offhook/onhook functionality from TEAMS to Device\n8 To test Voice Mail usage functionality of device\n9 To test volume increment from device to Teams client\n10 To test volume decrement from device to Teams Client\n (Press x if not applicable)"
                        while True:
                            input = self.read_and_validate_integer_input(0, 9)
                            if input == 'x':
                                self.not_useful_tests.append(0)
                            else:
                                if input == 1:
                                    verify = self.device_test(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 2:
                                    verify = self.hid_report(self.vid[int_option - 1], self.pid[int_option - 1])
                                    print('Your Hid information of the device stored in ASP.txt.Please see the file for detailed HID information!')
                                    print("Please proceed with the following operations...")

                                if input == 3:
                                    verify = self.test_mute_usage(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 4:
                                    verify = self.test_telephony_hook(self.vid[int_option - 1],self.pid[int_option - 1])

                                if input == 5:
                                    verify = self.test_flash_usage(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 6:
                                    verify = self.test_speed_dial_usage(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 7:
                                    verify = self.test_busy_usage(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 8:
                                    verify = self.test_voice_mail_usage(self.vid[int_option - 1],self.pid[int_option - 1])

                                if input == 9:
                                    verify = self.test_vol_incre_hook(self.vid[int_option - 1], self.pid[int_option - 1])

                                if input == 10:
                                    verify = self.test_vol_decre_hook(self.vid[int_option - 1], self.pid[int_option - 1])
                                    return verify
                    except KeyboardInterrupt as e:
                        print "Exception caught : " + str(e)
                        return None
            else:
                print("There's not any non system HID class device available")


    def read_and_validate_integer_input(self,start_range, end_range):
        while True :
            try :
                input = raw_input('Enter your input: Range['+str(start_range) +"-"+str(end_range) +"] :")
                selected = int(input)
                if (selected >= start_range and selected <= end_range):
                    return selected
            except Exception as e :
                print "Exception caught : " + str(e)
                return None

    def hid_report(self,vendor,product):
        with open('ASP.txt', "w") as f:
            with stdout_redirected(f):
                dev = hid.core.show_hids(target_vid=vendor, target_pid=product)
                print dev

    def device_test(self,vendor,product):
        with open('output3.txt', "w") as f:
            with stdout_redirected(f):
                dev = hid.core.show_hids(target_vid=vendor, target_pid=product)
                print dev
        with open("output3.txt", 'r') as myfile:
            for l in myfile.readlines():
                if "report_id: 154" in l:
                    print "###########################################"
                    print("This device is ASP supported")
                    print "###########################################"
                    print("Please proceed with the following operations...")
                    break
                elif "done!" in l:
                    pass
                    print "##################################################"
                    print("This device is not ASP supported")
                    print "##################################################"
                    print("Please proceed with the following operations...")
        open('output3.txt', 'w').close()

    def test_telephony_hook(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_hook = hid.get_full_usage_id(0xb, 0x20)

            def hook_pressed(new_value, event_type):
                event_type = event_type  # avoid pylint warnings
                if new_value:
                    print("On Hook!")
                else:
                    print("Off Hook!")

            for device in all_devices:
                try:
                    device.open()

                    # browse input reports
                    all_input_reports = device.find_input_reports()

                    for input_report in all_input_reports:
                        if usage_telephony_hook in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Hook switch functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press the hook switch to test or exit" \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_hook,
                                                     hook_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                # just keep the device opened to receive events
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")

    def test_mute_usage(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_mute = hid.get_full_usage_id(0xb, 0x2f)

            def mute_pressed(new_value, event_type):
                event_type = event_type
                if new_value:
                    print("Muted!")
                else:
                    print("Unmuted!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()
                    for input_report in all_input_reports:
                        if usage_telephony_mute in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Mute functionality!"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press Mute key to test or exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_mute,
                                                     mute_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")


    def test_busy_usage(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_busy = hid.get_full_usage_id(0xb, 0x97)

            def tone_pressed(new_value, event_type):
                event_type = event_type
                if new_value:
                    print("Call Accepted!")
                else:
                    print("Call Ended!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()
                    for input_report in all_input_reports:
                        if usage_telephony_busy in input_report:
                            print "\nEnd the call, if user is already is in call. Receive incoming call from Peripheral Device !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press Accept button from Teams or exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_busy,
                                                     tone_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")


    def test_flash_usage(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_flash = hid.get_full_usage_id(0xb, 0x21)
            def flash_pressed(new_value, event_type):
                event_type = event_type
                if new_value:
                    print("FLash Appeared!")
                else:
                    print("Flash Disappeared!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()
                    for input_report in all_input_reports:
                        if usage_telephony_flash in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Flash usage functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press any key to exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_flash,
                                                     flash_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")



    def test_speed_dial_usage(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_speed_dial = hid.get_full_usage_id(0xb, 0x50)
            def speed_dial_pressed(new_value, event_type):
                event_type = event_type
                if new_value:
                    print("FLash Appeared!")
                else:
                    print("Flash Disappeared!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()
                    for input_report in all_input_reports:
                        if usage_telephony_speed_dial in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Speed Dial functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press any key to exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_speed_dial,
                                                     speed_dial_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")

    def test_voice_mail_usage(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("\nNo HID class devices attached.")
        else:
            usage_telephony_voice_mail = hid.get_full_usage_id(0xc, 0xe2)
            def voice_mail_pressed(new_value, event_type):
                event_type = event_type
                if new_value:
                    print("FLash Appeared!")
                else:
                    print("Flash Disappeared!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()
                    for input_report in all_input_reports:
                        if usage_telephony_voice_mail in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Voice Mail functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press any key to exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_telephony_voice_mail,
                                                     voice_mail_pressed, hid.HID_EVT_CHANGED)  # level usage

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")

    def test_vol_decre_hook(self,vendor,product):
        input_interrupt_transfers = False
        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("No HID class devices attached.")
        else:
            # search for our target usage (the vol_decrement button)
            # target pageId, usageId
            usage_volume_decrement = hid.get_full_usage_id(0xc, 0xea)

            def button_pressed(new_value, event_type):
                "simple usage control handler"
                event_type = event_type
                if new_value:
                    print("Searching for our target usage, Pressed button.")
                    print("Button found: Volume Decremented!")

            for device in all_devices:
                try:
                    device.open()

                    all_input_reports = device.find_input_reports()

                    for input_report in all_input_reports:
                        if usage_volume_decrement in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Volume Increment functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press any key to exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_volume_decrement,
                                                     button_pressed, hid.HID_EVT_CHANGED)

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Raising and error: Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")

    def test_vol_incre_hook(self,vendor,product):
        input_interrupt_transfers = False

        all_devices = hid.HidDeviceFilter(vendor_id=vendor).get_devices()

        if not all_devices:
            print("No HID class devices attached.")
        else:
            # search for our target usage (the vol_increment button)
            # target pageId, usageId
            usage_volume_increment = hid.get_full_usage_id(0xc, 0xe9)

            def button_pressed(new_value, event_type):
                "simple usage control handler"
                event_type = event_type
                if new_value:
                    print("")
                    print("Searching for our target usage. Pressed button.")
                    print("Button found: Volume Incremented!")

            for device in all_devices:
                try:
                    device.open()
                    all_input_reports = device.find_input_reports()

                    for input_report in all_input_reports:
                        if usage_volume_increment in input_report:
                            print "\nPlease check whether the user is already in call or not, if not please establish the call before testing Volume Decrement functionality !"
                            print("\nMonitoring {0.vendor_name} {0.product_name} " \
                                  "device.\n".format(device))
                            print("Press any key to exit monitoring " \
                                  "(or remove HID device)...")

                            device.add_event_handler(usage_volume_increment,
                                                     button_pressed, hid.HID_EVT_CHANGED)

                            if input_interrupt_transfers:
                                input_report.get()

                            while not kbhit() and device.is_plugged():
                                sleep(0.5)
                            return
                finally:
                    device.close()
            print("Sorry, no one of the attached HID class devices " \
                  "provide any Telephony Hook button")

def main():
    DataManager()

if __name__ == '__main__':
    main()