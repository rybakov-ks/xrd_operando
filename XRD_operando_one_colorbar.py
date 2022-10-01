import matplotlib.pyplot as plt
import numpy as np
import glob
import math
import itertools   
from mpl_toolkits.axes_grid1.inset_locator import inset_axes  
import matplotlib.ticker as ticker 

def slice_list(x, y, z, start, stop):
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
    x_new = np.array([n[start:stop+1] for n in x])
    y_new = np.array([n[start:stop+1] for n in y])
    z_new = np.array([n[start:stop+1] for n in z])
    return start, stop, x_new, y_new, z_new

def get_seconds(time_str):
    #print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def data_import_txt():
    degrees, intensity = [], []
    files = glob.glob(r'[0-9]*.txt')
    files_s=[]
    for file in files:
        files_s.append(int(file.split('.txt')[0]))	
    const = 900
    for filename in sorted(files_s):
        with open(str(filename) + str('.txt'), encoding="UTF-8", errors='ignore') as f:
            data_lines = f.readlines()
            degrees_x = [float(n.split('	')[0]) for n in data_lines[9:3525]]
            intensity_y = [float(n.split('	')[1]) if float(n.split('	')[1]) < const else float(const) for n in data_lines[9:3525] ]
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

#Делаем разметку
fig,(ax1,ax,ax2,ax5,ax6,ax7,ax8,ax4) = plt.subplots(1,8, facecolor='w', figsize=(26, 7), gridspec_kw={'width_ratios':[12,15,15,15,15,15,15,6]})

#Строи график ГЗР
ax1.plot(potential, time, color='black', linewidth=2, zorder=50,
                 linestyle='--')
ax1.set_xlabel('Potential vs. Li$^+$/Li, V', family="Helvetica", fontsize=16)
ax1.set_ylabel('Time, h', family="Helvetica", fontsize=16)

#Настраиваем макисмальное и минимальное значение для цйветовой палитры
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 22, 70)
max_value = z_new.max()
min_value = z_new.min()

#Строим контурные графики для различных диапазонов 2-Theta
const=1
start, stop, x_new, z_new, y_new = slice_list(x, y, z, 30-const, 32+const)
sp1 = ax.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

start, stop, x_new, z_new, y_new = slice_list(x, y, z, 35-const, 37+const)
sp = ax2.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

start, stop, x_new, z_new, y_new = slice_list(x, y, z, 43-const, 45+const)
sp2 = ax5.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

start, stop, x_new, z_new, y_new = slice_list(x, y, z, 54-const, 56+const)
sp3 = ax6.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

start, stop, x_new, z_new, y_new = slice_list(x, y, z, 57-const, 59+const)
sp4 = ax7.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

start, stop, x_new, z_new, y_new = slice_list(x, y, z, 63-const, 65+const)
sp5 = ax8.contourf(x_new, y_new, z_new, 500, origin='image', cmap='PRGn', vmax=max_value, vmin=min_value)

#Строим цветовую палитру и настраиваем её
axins = inset_axes(ax4,
                    width="30%",  
                    height="100%",
                    loc='center left',
                    borderpad = 0
                   )
cbar = fig.colorbar(sp, shrink=0.5, cax=axins, format="%d")
cbar.ax.set_ylabel('Intensity, a.u.', rotation=270, labelpad = 25, fontsize=16)
cbar.ax.tick_params(labelsize=16) 

#Ограничиваем диапазоны данных для контурных графиков
ax1.set_xlim(2.9, 4.65)
ax1.set_ylim(0, math.ceil(max(time)))

ax.set_xlim(30.25, 31.25) 
ax.set_ylim(0, math.ceil(max(time)))
 
ax2.set_xlim(35.5, 36.7)  
ax2.set_ylim(0, math.ceil(max(time)))

ax5.set_ylim(0, math.ceil(max(time)))
ax5.set_xlim(43.5, 44.5)
  
ax6.set_ylim(0, math.ceil(max(time)))
ax6.set_xlim(54, 55.3) 

ax7.set_ylim(0, math.ceil(max(time)))
ax7.set_xlim(57.7, 59)  

ax8.set_ylim(0, math.ceil(max(time)))
ax8.set_xlim(63.4, 64.7)

#Оформляем графики
ax.spines['right'].set_visible(False)
ax.yaxis.tick_left()
ax.tick_params(labelright=False)
ax.tick_params(labelleft=False)

ax2.spines['left'].set_visible(False)
ax2.yaxis.tick_right()
ax2.tick_params(labelright=False)

d = .015 
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((1-d,1+d), (-d,+d), **kwargs)
ax.plot((1-d,1+d),(1-d,1+d), **kwargs)

kwargs.update(transform=ax2.transAxes)  
ax2.plot((-d,+d), (1-d,1+d), **kwargs)
ax2.plot((-d,+d), (-d,+d), **kwargs)
ax2.plot((1-d,1+d), (-d,+d), **kwargs)
ax2.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_visible(False)

kwargs.update(transform=ax5.transAxes)  
ax5.plot((-d,+d), (1-d,1+d), **kwargs)
ax5.plot((-d,+d), (-d,+d), **kwargs)
ax5.plot((1-d,1+d), (-d,+d), **kwargs)
ax5.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax5.tick_params(labelleft=False)
ax5.spines['left'].set_visible(False)
ax5.spines['right'].set_visible(False)

kwargs.update(transform=ax6.transAxes)  
ax6.plot((-d,+d), (1-d,1+d), **kwargs)
ax6.plot((-d,+d), (-d,+d), **kwargs)
ax6.plot((1-d,1+d), (-d,+d), **kwargs)
ax6.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax6.tick_params(labelleft=False)
ax6.spines['left'].set_visible(False)
ax6.spines['right'].set_visible(False)

kwargs.update(transform=ax7.transAxes)  
ax7.plot((-d,+d), (1-d,1+d), **kwargs)
ax7.plot((-d,+d), (-d,+d), **kwargs)
ax7.plot((1-d,1+d), (-d,+d), **kwargs)
ax7.plot((1-d,1+d),(1-d,1+d), **kwargs)
ax7.tick_params(labelleft=False)
ax7.spines['left'].set_visible(False)
ax7.spines['right'].set_visible(False)

kwargs.update(transform=ax8.transAxes)  
ax8.plot((-d,+d), (1-d,1+d), **kwargs)
ax8.plot((-d,+d), (-d,+d), **kwargs)
ax8.spines['left'].set_visible(False)
ax8.tick_params(labelleft=False)

ax.spines['top'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

ax1.spines['top'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2)

ax2.spines['top'].set_linewidth(2)
ax2.spines['bottom'].set_linewidth(2)
ax2.spines['right'].set_linewidth(2)
ax2.spines['left'].set_linewidth(2)

ax4.spines['top'].set_linewidth(False)
ax4.spines['bottom'].set_linewidth(False)
ax4.spines['right'].set_linewidth(False)
ax4.spines['left'].set_linewidth(False)

ax4.axes.xaxis.set_visible(False)
ax4.axes.yaxis.set_visible(False)

ax5.spines['top'].set_linewidth(2)
ax5.spines['bottom'].set_linewidth(2)
ax5.spines['right'].set_linewidth(2)
ax5.spines['left'].set_linewidth(2)

ax6.spines['top'].set_linewidth(2)
ax6.spines['bottom'].set_linewidth(2)
ax6.spines['right'].set_linewidth(2)
ax6.spines['left'].set_linewidth(2)

ax7.spines['top'].set_linewidth(2)
ax7.spines['bottom'].set_linewidth(2)
ax7.spines['right'].set_linewidth(2)
ax7.spines['left'].set_linewidth(2)

ax8.spines['top'].set_linewidth(2)
ax8.spines['bottom'].set_linewidth(2)
ax8.spines['right'].set_linewidth(2)
ax8.spines['left'].set_linewidth(2)

cbar.outline.set_linewidth(2)

cbar.ax.tick_params(axis='y', direction='out', length=6, width=2, grid_alpha=0.3, bottom = False, top = False, left = False, right = True, labelsize = 16, pad =13)
ax2.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax1.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = True, left = True, right = True, labelsize = 16, pad =13)
ax.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax5.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax6.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax7.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)
ax8.tick_params(direction='in', length=6, width=2, grid_alpha=0.3, bottom = True, top = False, left = False, right = False, labelsize = 16, pad =13)

ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax5.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
ax7.xaxis.set_major_locator(ticker.MultipleLocator(0.4))
ax6.xaxis.set_major_locator(ticker.FixedLocator([54.2, 54.7, 55.2]))

fig.suptitle('Operando XRD LCV', x = 0.5, y = 0.94, fontsize=20)
fig.text(0.57, 0.02, '2-Theta, deg.', ha='center', fontsize=16)

#Заверщаем построение и сохраняем график
plt.subplots_adjust(wspace=0.04,hspace=0.2)
plt.savefig('XRD1.jpg', dpi = 300)
plt.show()