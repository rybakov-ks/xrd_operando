import matplotlib.pyplot as plt
import numpy as np
import glob
import itertools 
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker 

def slice_list(x, y, z, start, stop, bais):
    for i in x:
        for n in i:
            if math.floor(n) == start:
                start = int(i.index(n))
                break
    for i in x:
        for n in i:
            if math.floor(n) == stop:
                stop = int(i.index(n))
                break
    x_new = np.array([n[start:stop+1+bais] for n in x])
    y_new = np.array([n[start:stop+1+bais] for n in y])
    z_new = np.array([n[start:stop+1+bais] for n in z])
    return start, stop, x_new, y_new, z_new
    
def get_seconds(time_str):
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def data_import_txt():
    degrees, intensity = [], []
    files = glob.glob(r'[0-9]*.txt')
    files_s=[]
    for file in files:
        files_s.append(int(file.split('.txt')[0]))	
    for filename in sorted(files_s):
        with open(str(filename) + str('.txt'), encoding="UTF-8", errors='ignore') as f:
            data_lines = f.readlines()
            degrees_x = [float(n.split('	')[0]) for n in data_lines[9:3525]]
            intensity_y = [float(n.split('	')[1]) for n in data_lines[9:3525]]
        degrees.append(degrees_x)
        intensity.append(intensity_y)
    return degrees, intensity
    
def data_import_txt_charge(filename):
    with open(filename, encoding="Windows-1251", errors='ignore') as f:
        data_lines = f.readlines()
        time = [float(get_seconds(n.split()[0]))/3600 for n in data_lines[0:]]
        potential = [float(n.split()[1]) for n in data_lines[0:]]
        current = [float(n.split()[2]) for n in data_lines[0:]]
    return time, potential, current

#Импортируем дифракционные данные
degrees, intensity = data_import_txt()

#Импортируем данные ГЗР
time, potential, current = data_import_txt_charge('charge.txt')

x = degrees
y = intensity

#Генерируем временную шкалу эксперимента
time_step_xrd = 1140
z = []
for i in range(0, len(x)):
    z_temp = []
    for u in x[i]:
        z_temp.append(i*time_step_xrd/3600)
    z.append(z_temp)

#Делаем разметку для графика
fig = plt.figure(figsize=(30, 9))
grid = GridSpec(2, 7, width_ratios=[12, 15, 15, 15, 15, 15, 15], height_ratios=[3, 15])

#Строи график ГЗР
ax1 = plt.subplot(grid[7])
ax1.plot(potential, time, color='black', linewidth=2, zorder=50,
                 linestyle='--')
ax1.set_xlim(2.9, 4.65)
ax1.set_ylim(0, math.ceil(max(time)))
ax1.spines['top'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2) 
ax1.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = True, left = True, right = True, labelsize = 16, pad =13)
ax1.set_xlabel('Potential vs. Li$^+$/Li, V', family="Helvetica", fontsize=16)
ax1.set_ylabel('Time, h', family="Helvetica", fontsize=16)

colormap = "PRGn"
#Контурный график. Первый интервал
ax2 = plt.subplot(grid[8])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 30, 32, 0)
sp1 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax2.tick_params(labelright=False)
ax2.tick_params(labelleft=False)
ax2.spines['top'].set_linewidth(2)
ax2.spines['bottom'].set_linewidth(2)
ax2.spines['left'].set_linewidth(2)
ax2.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax2.set_xlim(30.25, 31.25)
ax2.set_ylim(0, math.ceil(max(time)))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
d = .015 
kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
ax2.plot((1-d,1+d), (-d,+d), **kwargs)
ax2.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax2.spines['right'].set_visible(False)

#Colorbar для первого интервала
ax3 = plt.subplot(grid[1])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax3)
cax = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min(), z_new.max()-40, 4, endpoint=True)
cbar = plt.colorbar(sp1, cax=cax, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
cbar.ax.tick_params(labelsize=14) 
cbar.ax.tick_params(width=2)
cbar.outline.set_linewidth(2)
cbar.ax.tick_params(axis='y', direction='out', length=6, width=2, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')

#Контурный график. Второй интервал
ax4 = plt.subplot(grid[9])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 35, 37, 0)
sp2 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax4.tick_params(labelright=False)
ax4.tick_params(labelleft=False)
ax4.spines['top'].set_linewidth(2)
ax4.spines['bottom'].set_linewidth(2)
ax4.tick_params(axis = 'both', direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax4.set_xlim(35.5, 36.7)
ax4.set_ylim(0, math.ceil(max(time)))
ax4.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
kwargs.update(transform=ax4.transAxes)  
ax4.plot((-d,+d), (1-d,1+d), **kwargs)
ax4.plot((-d,+d), (-d,+d), **kwargs)
ax4.plot((1-d,1+d), (-d,+d), **kwargs)
ax4.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax4.spines['left'].set_visible(False)
ax4.spines['right'].set_visible(False)

#Colorbar для второго интервала
ax5 = plt.subplot(grid[2])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax5)
cax2 = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min()+40, z_new.max()-40, 4, endpoint=True)
cbar2 = plt.colorbar(sp2, cax=cax2, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
#cbar.ax.set_ylabel('Intensity, a.u.', labelpad = 25, fontsize=16)
#cbar2.set_label('Intensity, a.u.', labelpad = 5, fontsize=16)
cbar2.ax.tick_params(labelsize=14) 
cbar2.ax.tick_params(width=2)
cbar2.outline.set_linewidth(2)
cbar2.ax.tick_params(axis='y', direction='out', length=6, width=4, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax2.xaxis.set_label_position('top')
cax2.xaxis.set_ticks_position('top')

#Контурный график. Третий интервал
ax6 = plt.subplot(grid[10])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 43, 45, -23)
sp3 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax6.tick_params(labelright=False)
ax6.tick_params(labelleft=False)
ax6.spines['top'].set_linewidth(2)
ax6.spines['bottom'].set_linewidth(2)
ax6.tick_params(axis = 'both', direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax6.set_xlim(43.5, 44.5)
ax6.set_ylim(0, math.ceil(max(time)))
ax6.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
kwargs.update(transform=ax6.transAxes)  
ax6.plot((-d,+d), (1-d,1+d), **kwargs)
ax6.plot((-d,+d), (-d,+d), **kwargs)
ax6.plot((1-d,1+d), (-d,+d), **kwargs)
ax6.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax6.spines['left'].set_visible(False)
ax6.spines['right'].set_visible(False)

#Colorbar для третьего интервала
ax7 = plt.subplot(grid[3])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax7)
cax3 = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min()+40, z_new.max()-40, 4, endpoint=True)
cbar3 = plt.colorbar(sp3, cax=cax3, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
#cbar.ax.set_ylabel('Intensity, a.u.', labelpad = 25, fontsize=16)
#cbar2.set_label('Intensity, a.u.', labelpad = 5, fontsize=16)
cbar3.ax.tick_params(labelsize=14) 
cbar3.ax.tick_params(width=2)
cbar3.outline.set_linewidth(2)
cbar3.ax.tick_params(axis='y', direction='out', length=6, width=4, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax3.xaxis.set_label_position('top')
cax3.xaxis.set_ticks_position('top')

#Контурный график. Четвертый интервал
ax8 = plt.subplot(grid[11])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 54, 56, 0)
sp4 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax8.tick_params(labelright=False)
ax8.tick_params(labelleft=False)
ax8.spines['top'].set_linewidth(2)
ax8.spines['bottom'].set_linewidth(2)
ax8.tick_params(axis = 'both', direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax8.set_xlim(54, 55.3) 
ax8.set_ylim(0, math.ceil(max(time)))
ax8.xaxis.set_major_locator(ticker.FixedLocator([54.2, 54.7, 55.2]))
kwargs.update(transform=ax8.transAxes)  
ax8.plot((-d,+d), (1-d,1+d), **kwargs)
ax8.plot((-d,+d), (-d,+d), **kwargs)
ax8.plot((1-d,1+d), (-d,+d), **kwargs)
ax8.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax8.spines['left'].set_visible(False)
ax8.spines['right'].set_visible(False)

#Colorbar для четвертого интервала
ax9 = plt.subplot(grid[4])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax9)
cax4 = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min()+40, z_new.max()-40, 4, endpoint=True)
cbar4 = plt.colorbar(sp4, cax=cax4, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
#cbar.ax.set_ylabel('Intensity, a.u.', labelpad = 25, fontsize=16)
#cbar2.set_label('Intensity, a.u.', labelpad = 5, fontsize=16)
cbar4.ax.tick_params(labelsize=14) 
cbar4.ax.tick_params(width=2)
cbar4.outline.set_linewidth(2)
cbar4.ax.tick_params(axis='y', direction='out', length=6, width=4, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax4.xaxis.set_label_position('top')
cax4.xaxis.set_ticks_position('top')

#Контурный график. Пятый интервал
ax10 = plt.subplot(grid[12])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 57, 59, 0)
sp5 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax10.tick_params(labelright=False)
ax10.tick_params(labelleft=False)
ax10.spines['top'].set_linewidth(2)
ax10.spines['bottom'].set_linewidth(2)
ax10.tick_params(axis = 'both', direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax10.set_xlim(57.7, 59)
ax10.set_ylim(0, math.ceil(max(time)))
ax10.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
kwargs.update(transform=ax10.transAxes)  
ax10.plot((-d,+d), (1-d,1+d), **kwargs)
ax10.plot((-d,+d), (-d,+d), **kwargs)
ax10.plot((1-d,1+d), (-d,+d), **kwargs)
ax10.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax10.spines['left'].set_visible(False)
ax10.spines['right'].set_visible(False)

#Colorbar для пятого интервала
ax11 = plt.subplot(grid[5])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax11)
cax5 = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min()+40, z_new.max()-40, 4, endpoint=True)
cbar5 = plt.colorbar(sp5, cax=cax5, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
#cbar.ax.set_ylabel('Intensity, a.u.', labelpad = 25, fontsize=16)
#cbar2.set_label('Intensity, a.u.', labelpad = 5, fontsize=16)
cbar5.ax.tick_params(labelsize=14) 
cbar5.ax.tick_params(width=2)
cbar5.outline.set_linewidth(2)
cbar5.ax.tick_params(axis='y', direction='out', length=6, width=4, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax5.xaxis.set_label_position('top')
cax5.xaxis.set_ticks_position('top')

#Контурный график. Шестой интервал
ax12 = plt.subplot(grid[13])
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 63, 65, -22)
sp6 = plt.contourf(x_new, y_new, z_new, 500, origin='image', cmap=colormap)
ax12.tick_params(labelright=True)
ax12.tick_params(labelleft=False)
ax12.spines['top'].set_linewidth(2)
ax12.spines['bottom'].set_linewidth(2)
ax12.spines['right'].set_linewidth(2)
ax12.tick_params(axis = 'both', direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = True, labelsize = 16, pad =13)
ax12.set_xlim(63.4, 64.7)
ax12.set_ylim(0, math.ceil(max(time)))
ax12.set_ylabel('Time, h', family="Helvetica", fontsize=16, rotation=270, labelpad=18)
ax12.yaxis.set_label_position("right")
ax12.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
kwargs.update(transform=ax12.transAxes)  
ax10.plot((-d,+d), (1-d,1+d), **kwargs)
ax10.plot((-d,+d), (-d,+d), **kwargs)
ax10.spines['left'].set_visible(False)

#Colorbar для шестого интервала
ax13 = plt.subplot(grid[6])
plt.gca().set_visible(False)
divider = make_axes_locatable(ax13)
cax6 = divider.append_axes("bottom", size="30%", pad=0.3)
ticks = np.linspace(z_new.min()+40, z_new.max(), 4, endpoint=True)
cbar6 = plt.colorbar(sp6, cax=cax6, orientation="horizontal", format="%d", pad = -100, ticks=ticks)
#cbar.ax.set_ylabel('Intensity, a.u.', labelpad = 25, fontsize=16)
#cbar2.set_label('Intensity, a.u.', labelpad = 5, fontsize=16)
cbar6.ax.tick_params(labelsize=14)
cbar6.ax.tick_params(width=2)
cbar6.outline.set_linewidth(2)
cbar6.ax.tick_params(axis='y', direction='out', length=6, width=4, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
cax6.xaxis.set_label_position('top')
cax6.xaxis.set_ticks_position('top')

fig.text(0.56, 0.04, '2-Theta, deg.', ha='center', fontsize=16)
fig.suptitle('Operando XRD LCV', x = 0.5, y = 0.85, fontsize=20)

#Заверщаем построение и сохраняем график
plt.subplots_adjust(wspace=0.04,hspace=0.05)
plt.savefig('XRD5.jpg', dpi = 300)
plt.show()