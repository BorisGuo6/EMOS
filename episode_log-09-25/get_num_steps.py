import argparse
import os.path as osp
import json

parser = argparse.ArgumentParser()
# necessary arguments
parser.add_argument(
    "--dir",
    type=str,
    default='',
    help="Relative path to video path.",
)
args, _ = parser.parse_known_args()


with open(args.dir, encoding='utf-8') as f:
    data = json.load(f)
    
# 解析并计算平均 num_steps
total_steps = 0
count = 0

for key, value in data.items():
    # 提取 num_steps 的值
    steps = int(value.split(": ")[1])
    total_steps += steps
    count += 1

# 计算平均值
average_steps = total_steps / count

# 输出平均 num_steps
print(f"Average num_steps: {average_steps}")
