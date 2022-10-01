# xrd_operando
A set of scripts for constructing diffractograms taken in the *operando* mode during charge-discharge of the electrode material.\
**XRD_operando_many_colorbar.py** is designed to plot X-ray diffraction versus material charge-discharge degree with separate colorbars for selected 2-Theta angle ranges.\
**XRD_operando_one_colorbar.py** is designed to plot X-ray diffraction versus charge-discharge degree of a material with a common colorbar for selected ranges of 2-Theta angles.
## Usage
Execute the script in the catalog with X-ray diffraction data and with galvanostatic cycling data. You must first specify the registration time for one diffraction pattern in seconds (Example: time_step_xrd=1140). For XRD_operando_one_colorbar.py, you additionally need to specify in the data_import_txt() function the maximum intensity above which values will be ignored (Example: const=900).\
X-ray diffraction data must be passed to the data_import_txt() function, and the results of galvanostatic cycling to the data_import_txt_charge(filename) function:
```python
python XRD_operando_many_colorbar.py
python XRD_operando_one_colorbar.py
```
An example of data to be processed is located in the "Data" directory.
## Example 1 – RD_operando_many_colorbar.py
![Alt-текст](https://github.com/rybakov-ks/xrd_operando/blob/main/Images/XRD5.jpg "XRD")
## Example 2 – XRD_operando_one_colorbar.py
![Alt-текст](https://github.com/rybakov-ks/xrd_operando/blob/main/Images/XRD1.jpg "XRD")
## Contributors
Rybakov Kirill (Saratov State University): rybakov-ks@ya.ru
