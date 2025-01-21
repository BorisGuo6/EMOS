import os
import json

from sympy import root

def calculate(root_path):
    total_sum = 0
    folder_num = 0

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            token_path = os.path.join(folder_path, "token_usage.json")
            if os.path.exists(token_path):
                try:
                    with open(token_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            folder_sum = sum(data.values())
                            total_sum += folder_sum      
                            folder_num += 1               
                except json.JSONDecodeError:
                    pass
                
    if folder_num > 0:
        average = total_sum / folder_num
        print(f"Average token usage of {root_folder}: {average}")
        return average
    else:
        return 0                                                                                                                    

root_folder =  "/home/lgtm/habitat-lab/chat_history_output/scalability_chat_new/robot_10"
calculate(root_folder)