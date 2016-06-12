import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys

BAR_WIDTH = 0.5

if len(sys.argv) == 1:
    print "Need to add a file name"
    sys.exit()


with open(sys.argv[1]) as open_file:
    f = csv.reader(open_file)
    tmp_list = []

    for row in f:
        tmp_list.append(row)

    labels = tmp_list[0]
    avg = map(float, tmp_list[1])

    if len(tmp_list) == 3:
        std = map(float, tmp_list[2])

fig = plt.figure()
ax = fig.add_subplot(111)

#if sys.argv[1][:2] == "Tx":
print len(labels)
print len(avg)

x_values = [i for i in range(len(labels))]
labels.insert(0, 'bump')

ax.set_title(r"Success Rate, 1 Pilot", fontsize=20)
ax.set_xlabel('Setup', fontsize=20)
ax.set_ylabel(r'Success Rate', fontsize=20)

ax.set_xlim(0, len(labels) - 1)
ax.set_ylim(-0.1, 105)

majorLocator = MultipleLocator(1)
majorFormatter = FormatStrFormatter('%d')
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_major_formatter(majorFormatter)

ax.set_xticklabels(labels, fontsize=16, rotation=15)
ax.tick_params(axis='y', labelsize=20)

for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_horizontalalignment('left')

if len(tmp_list) == 2:
    ax.bar(x_values, avg, BAR_WIDTH, color='r', alpha=0.6)

elif len(tmp_list) == 3:
    ax.bar(x_values, avg, BAR_WIDTH, yerr=std, color='r', alpha=0.6)

plt.grid(True)
plt.show()
