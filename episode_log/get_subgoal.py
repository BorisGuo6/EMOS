import json
import argparse
import os.path as osp

parser = argparse.ArgumentParser()
# necessary arguments
parser.add_argument(
    "--dir",
    type=str,
    default='',
    help="Relative path to video path.",
)
args, _ = parser.parse_known_args()

# 加载json数据
with open(args.dir, 'r') as file:
    data = json.load(file)

# 创建一个字典来存储每种subgoal的成功次数和总次数
subgoal_stats = {}

# 遍历每个episode
for episode, subgoals in data.items():
    for subgoal, success in subgoals.items():
        if subgoal not in subgoal_stats:
            subgoal_stats[subgoal] = {'success': 0, 'total': 0}
        subgoal_stats[subgoal]['success'] += success  # 累加成功次数
        subgoal_stats[subgoal]['total'] += 1          # 累加总次数

# 计算成功率并输出
for subgoal, stats in subgoal_stats.items():
    success_rate = stats['success'] / stats['total']
    print(f"{subgoal}: 成功率为 {success_rate:.2%}")


