from tkinter import font
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

tasks = ["Task 1", "Task 2", "Task 3", "Task 4"]
ablations = ["EMOS", "w/o. Numerical", "w/o. Robot Resume",  "w/o. Discussion"]

data = pd.read_csv("ablation.csv", header=None)
data.columns = ["Ablation", "Task", "SuccessRate", "TokenUsage", "Steps"]
data = data.fillna(0)
tasks = data['Task'].unique()
ablations = data['Ablation'].unique()
success_rate = np.zeros((len(ablations), len(tasks)))
token_usage = np.zeros((len(ablations), len(tasks)))
steps = np.zeros((len(ablations), len(tasks)))

# Set data from xlsx
for i, ablation in enumerate(ablations):
    for j, task in enumerate(tasks):
        row = data[(data['Ablation'] == ablation) & (data['Task'] == task)]
        if not row.empty:
            success_rate[i, j] = row['SuccessRate'].values[0]
            token_usage[i, j] = row['TokenUsage'].values[0]
            steps[i, j] = row['Steps'].values[0]       

token_max = token_usage.max()
steps_max = steps.max()

# 计算每个任务成功率的平均值
success_rate_mean = success_rate.mean(axis=1)
width = 0.3
fig, ax1 = plt.subplots(figsize=(15, 5))  # Increase figure size for better spacing

# Flatten x-axis positions for ablations within each task with increased spacing
x_spacing = 1.5  # Increase the spacing between tasks
x = np.arange(len(tasks) * len(ablations)) * x_spacing
task_positions = np.array([np.arange(len(ablations)) + i*len(ablations)*x_spacing for i in range(len(tasks))]).flatten()

# Success rate scaling factors for better visibility
success_rate_scaling_factor = 600000
mean_success_rate_scaling_factor = 700000

# Plot Token Usage bars
token_bar = ax1.bar(task_positions - width/2, token_usage.flatten(), width, color="#F0988C", alpha=1.0)

# Plot Steps bars on the secondary y-axis
ax2 = ax1.twinx()
steps_bar = ax2.bar(task_positions + width/2, steps.flatten(), width, color="#B883D4", alpha=1.0)

# Plot Success Rate lines for each task
# Plot Success Rate lines for each task
for i in range(len(tasks)):
    success_line, = ax1.plot(task_positions[i*len(ablations):(i+1)*len(ablations)], 
                             success_rate[:, i] * success_rate_scaling_factor + 210000,  # 修改这里
                             color="#A1A9D0", marker="o", linewidth=2)
    # Add text for success rate at each point
    for j in range(len(ablations)):
        ax1.text(task_positions[i*len(ablations) + j], success_rate[j][i] * success_rate_scaling_factor + 220000,  # 修改这里
                 f'{success_rate[j][i]:.2f}', ha='center', va='bottom', color='#A1A9D0', fontsize=13)

# Plot the mean success rate as a red dashed line
mean_success_rate = success_rate.mean(axis=0)  # 修改这里
mean_success_line, = ax1.plot(np.arange(0, len(tasks) * len(ablations) * x_spacing, len(ablations) * x_spacing) + len(ablations) / 2, 
                              mean_success_rate * mean_success_rate_scaling_factor + 320000, 
                              color="#F0988C", linestyle="--", marker="D", linewidth=2, label="Mean Success Rate")


for i in range(len(tasks)):
    ax1.text(task_positions[i*len(tasks)] + len(ablations) / 2, mean_success_rate[i] * mean_success_rate_scaling_factor + 330000, 
             f'{mean_success_rate[i]:.2f}', ha='center', va='bottom', color='#F0988C', fontsize=13)

# Set custom x-ticks: for each ablation and task
ablation_labels = np.tile(ablations, len(tasks))
task_labels = np.repeat(tasks, len(ablations))

ax1.tick_params(axis='y', labelsize=12)
ax2.tick_params(axis='y', labelsize=12)

# Set x-tick positions and labels
ax1.set_xticks(task_positions)
ax1.set_xticklabels(ablation_labels, rotation=45, ha="right", fontsize=12, verticalalignment='top')

# Add task names at the bottom
for i, task in enumerate(tasks):
    ax1.text(np.mean(task_positions[i*len(ablations):(i+1)*len(ablations)]), token_max * 3.1, task, 
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Set y-axis labels
ax1.set_ylabel("Token Usage", fontsize=14, fontweight='bold', color="black")
ax1.set_ylim(0, token_max * 3.0)
ax2.set_ylabel("Steps", fontsize=14, fontweight='bold', color="black")
ax2.set_ylim(0, steps_max * 3.0)

# Add a global legend for all the plot elements
fig.legend([token_bar, steps_bar, success_line, mean_success_line], 
           ["Token Usage ↓", "Steps ↓", "Success Rate ↑", "Task Average Success Rate ↑"], 
           loc="upper center", bbox_to_anchor=(0.5, 1.015), ncol=4, fontsize=14)

# Adjust the layout for better spacing and visibility
plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()
