# USB_HID_Automation

Download and install libusb-win32-devel-filter

http://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/libusb-win32-devel-filter-1.2.6.0.exe/download


 

 



 


 


3) Installation Instructions:
Copy the files to your local directory. Eg: Under C:\Peripheral_Automation.
Run the following command from folder where the project is placed and wait for completion. This will install all dependencies needed for the project.
C:\Peripheral_Automation pip install -r peripheral_requirements.txt 
 
HID Keycode/INTENT Semi-Automated tests
Pre-Req: These tests are run only on a single device. Make sure it is connected via adb. All tests are to be verified manually.
Open Command prompt as administrator and navigate to the project directory and run the below cmd.
C:/Peripheral_Automation >python DataManager.py
Enter the option of the Device from the Device list.
Below is the screenshot:
 
Select the option and enter the input for testing:
 






Once the test case is executed, the report will look like below screenshot:
 





![image](https://github.com/dhingrachirag/USB_HIDS_Automation/assets/46193115/2f353930-edc9-48e5-830b-138993823bc3)
