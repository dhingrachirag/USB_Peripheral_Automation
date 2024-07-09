# USB_HID_Peripheral_Automation

Download and install libusb-win32-devel-filter

http://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/libusb-win32-devel-filter-1.2.6.0.exe/download

<img width="375" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/e0eec44a-d15e-4e80-a0db-85f7dc8e4540">

<img width="350" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/cf4b6e0c-21a0-459e-87f8-f5054bc6e039">

<img width="350" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/b994fb28-de0c-4ff3-a385-cf753bae4ad8">

Installation Instructions:
Copy the files to your local directory. Eg: Under C:\Peripheral_Automation.
Run the following command from folder where the project is placed and wait for completion. This will install all dependencies needed for the project.

<img width="474" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/2d9b8d8d-6f31-4466-9a75-604c1a266390">

C:\Peripheral_Automation pip install -r peripheral_requirements.txt 

<img width="474" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/e4da34d8-218b-42e9-a4f3-ec38f561bc30">

HID Keycode/INTENT Semi-Automated tests
Pre-Req: These tests are run only on a single device. Make sure it is connected via adb. All tests are to be verified manually.
Open Command prompt as administrator and navigate to the project directory and run the below cmd.
C:/Peripheral_Automation >python DataManager.py

Enter the option of the Device from the Device list.

Below is the screenshot:

 <img width="466" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/930a7db1-481a-470b-a5c9-de6ec5d51ce6">

Select the option and enter the input for testing:
 
<img width="492" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/1a47b665-1fa5-483a-aac7-4b3b0b4f2977">

Once the test case is executed, the report will look like below screenshot:
 
<img width="399" alt="image" src="https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/d9fc08ad-4539-4e85-b1bd-fac9bc2e26ef">


