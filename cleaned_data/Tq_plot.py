import matplotlib.pyplot as plt
import csv

x_range = [i for i in range(12)]

with open("Tq_timings.csv") as q_csv:
    q = csv.reader(q_csv)
    tmp_list = []
    for row in q:
        tmp_list.append(row)

    q_avg = map(float, tmp_list[0])
    q_std = map(float, tmp_list[1])

fig = plt.figure()
ax = fig.add_subplot(111)

width = 0.3

q_bars = ax.bar(x_range, q_avg, width, color='r', alpha=0.5,  yerr=q_std)

ax.set_xlabel('Pilot-Unit Setup', fontsize=20)
ax.set_xlim(-0.5, 12)
ax.set_xticks([x_range[i] + width for i in range(len(x_range))])
xTickNames = ax.set_xticklabels(["P1 U1", "P1 U2", "P1 U4", "P1 U8", "P1 U16", "P1 U32", \
                                  "P1 U64", "P1 U128", "P1 U256", "P1 U512", "P1 U1024",  \
                                  "P1 U2048"])
plt.setp(xTickNames, rotation = 25, fontsize=20)

ax.tick_params(axis='both', labelsize=20)
ax.set_ylabel('Time (s)', fontsize=20)
ax.set_ylim(0, 400)


ax.set_title("Average Queue Times", fontsize=20)

plt.show()
