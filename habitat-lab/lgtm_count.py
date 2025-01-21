import os
import re
import json
import gzip
import os.path as osp
from datetime import datetime

config_name = {
    '1': "llm_spot_fetch_mobility",
    '2': "zxz_llm_dist_man",
    '3': "zxz_llm_height_man",
    '4': "zxz_llm_height_per",
    '5': "llm_multi_agent_mobility"
}

dataset_path = {
    '1': "mp3d/mobility_episodes_1.json.gz",
    '2': "hssd/0/hssd_dist_man.json.gz",
    '3': "hssd/0/hssd_height_man.json.gz",
    '4': "hssd/0/hssd_height_per.json.gz",
    '5': "mp3d/mp3d_rearrange.json.gz"
}

video_dir = {
    '1': "spot_fetch_mobility",
    '2': "dist_man",
    '3': "height_man",
    '4': "height_per",
    '5': "mp3d_rearrange"
}

ablation_mode = {
    '1': "group_discussion",
    '2': "agent_reflection",
    '3': "robot_resume",
    '4': "numerical",
    '5': "full",
}

class LGTM:
    def __init__(self, args):
        self.args = args
        self.config_name = args.config_name
        self.dataset = args.dataset_dir
        self.video_dir = args.video_dir
        self.ablation_mode = args.ablation_mode

        self._full_episode_ids = []
        self._test_episode_ids = []

    def get_episode_ids(self):
        dataset_path = osp.join("data/datasets", self.dataset)
        while not osp.exists(dataset_path):
            print("==================Dataset Path==================")
            print("Dataset path {} does not exist, please input again".format(dataset_path))
            dataset_path = osp.join("data/datasets", input(""))

        with gzip.open(dataset_path, 'rt', encoding='utf-8') as f:
            data = json.load(f)

        episodes = data['episodes']
        episode_ids = [ep['episode_id'] for ep in episodes] 
        self._full_episode_ids = episode_ids      

    # parse success rate of certain task(from video_dir)
    def parse_success_rate(self):
        total_files, success_files = 0, 0
        video_path = osp.join("video_multi", self.video_dir)
        while not osp.exists(video_path):
            print("==================Video Path==================")
            print("We save videos in video_multi/ as default, but video path {} does not exist, please input again".format(video_path))
            video_path = osp.join("video_multi", input(""))

        success_ids, failed_ids = [], []
        for filename in os.listdir(video_path):
            if filename.endswith(".mp4"):
                total_files += 1
                episode_id = filename.split("episode=")[1].split("_")[0]
                if "pddl_success=1.00" in filename:
                    success_files += 1
                    success_ids.append(episode_id)
                else:
                    failed_ids.append(episode_id)

        if total_files > 0:
            success_ratio = success_files / total_files
        else:
            success_ratio = 0     

        self._test_episode_ids = success_ids + failed_ids
        self.success_rate = success_ratio
        print("==================Success Rate Summary==================")
        print(f"Success Episode Num: {success_files}")
        print(f"Tested Episode Num: {total_files}")
        print(f"Success Rate: {success_ratio:.4f}")         

    # split not test data from video_dir to datasets
    def split_not_test_data(self):
        if not len(self._test_episode_ids) or not len(self._full_episode_ids):
            self.get_episode_ids()
            self.parse_success_rate()
        episode_ids = [str(a) for a in self._full_episode_ids]
        tested_episode_ids = [str(a) for a in self._test_episode_ids]

        if len(tested_episode_ids) > len(episode_ids):
            print("==================Warning==================")
            print("You might forgot to reset your video dir after last run, the success rate will be wrong!")
            return False
        
        elif len(tested_episode_ids) == len(episode_ids):
            print("==================All Tested====================")
            print("All episodes in the dataset have been tested!")
        
        else:
            print("==================Not All Tested==================")
            not_tested_ids = list(set(episode_ids) - set(tested_episode_ids))
            print("Episodes that have not been tested: ", not_tested_ids)
            result = input("Do you want to split these episodes to test again? (y/n)")

            if result == "y":
                with gzip.open(osp.join("data/datasets", self.dataset), 'rt', encoding='utf-8') as f:
                    data = json.load(f)
                
                data['episodes'] = [ep for ep in data['episodes'] if ep['episode_id'] in not_tested_ids]

                print("==================Set New Dataset Name==================")  
                scene_prefix = self.dataset.split("/")[0]
                file_name = self.dataset.split("/")[-1]
                if not osp.exists(osp.join("data/datasets", scene_prefix, 'not_test')):
                    os.makedirs(osp.join("data/datasets", scene_prefix, 'not_test'))

                with gzip.open(osp.join("data/datasets", scene_prefix, 'not_test', file_name), 'wt', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print("==================Done==================")
                print("New dataset has been saved in: ", osp.join("data/datasets", scene_prefix, 'not_test', file_name))
        
        return True

    # parse average step nums of task and subgoal average success rate(from episode log)
    def parse_episode_log(self):
        dataset_name = self.dataset.split("/")[-1].split(".")[0]
        episode_log_path = osp.join("episode_log", dataset_name, self.ablation_mode.upper())
        if not osp.exists(episode_log_path):
            print("==================Warning==================")
            print("No log found in {}!".format(episode_log_path))
            return False
        
        step_path = osp.join(episode_log_path, f"{dataset_name}_steps_log.json")
        if not osp.exists(step_path):
            print("==================Warning==================")
            print("No step log found in {}!".format(step_path))
            return False
        with open(step_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_steps = 0
        count = 0
        for key, value in data.items():
            steps = int(value.split(": ")[1])
            total_steps += steps
            count += 1

        average_steps = total_steps / count
        print("==================Average Steps==================")
        print(f"Average num_steps: {average_steps}")
        self.average_steps = average_steps

        subgoal_path = osp.join(episode_log_path, f"{dataset_name}_subgoals.json")
        if not osp.exists(subgoal_path):
            print("==================Warning==================")
            print("No subgoal log found in {}!".format(subgoal_path))
            return False
        
        with open(subgoal_path, 'r') as file:
            data = json.load(file)

        subgoal_stats = {}
        for episode, subgoals in data.items():
            for subgoal, success in subgoals.items():
                if subgoal not in subgoal_stats:
                    subgoal_stats[subgoal] = {'success': 0, 'total': 0}
                subgoal_stats[subgoal]['success'] += success  
                subgoal_stats[subgoal]['total'] += 1        

        print("==================Subgoal Success Rate==================")
        for subgoal, stats in subgoal_stats.items():
            success_rate = stats['success'] / stats['total']
            print(f"{subgoal} average success rate: {success_rate:.4%}")
        self.subgoal_stats = subgoal_stats
        return True

    # parse average token usage of task(from chat history)
    def parse_average_token_usage(self):
        total_sum = 0
        file_count = 0
        
        parent_folder = "chat_history_output/"
        paths = [p for p in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, p))]
        valid_date_paths = []
        date_paths = []
        for path in paths:
            try:
                date = datetime.strptime(path, '%Y-%m-%d')
                date_paths.append((date, path))
            except ValueError:
                continue
        if not date_paths:
            print("==================Warning==================")
            print("No chat history named as date time found in {}!".format(parent_folder))
            if not paths:
                return False
            latest_path = input("Please input right path in chat_history_output: ")
            valid_date_paths.append(latest_path)
        else:
            print("==================Chat History==================")
            mid_path = input("If you want to checkout all the date history, please type 'n', else type specified date like 2022-01-01:")
            if mid_path == 'n':
                for date_path in date_paths:
                    full_path = osp.join(parent_folder, date_path[1], self.config_name, self.ablation_mode.upper())
                    if osp.exists(full_path):
                        valid_date_paths.append(date_path[1])
            else:
                valid_date_paths.append(mid_path)

        for valid_date_path in valid_date_paths:
            episodes_path = osp.join(parent_folder, valid_date_path, self.config_name, self.ablation_mode.upper())

            if not osp.exists(episodes_path):
                print("==================Warning==================")
                print("No episode log found in {}!".format(episodes_path))
                continue
            
            for root, dirs, files in os.walk(episodes_path):
                for file in files:
                    if file == "token_usage.json":
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total_sum += sum(data.values())
                            file_count += 1
        
        if file_count == 0:
            averate_tokens = 0
        else:
            averate_tokens = total_sum / file_count
        print("==================Average Token Usage==================")
        print(f"Average token usage: {averate_tokens}")
        self.averate_tokens = averate_tokens
        return True

    # print final summary of each task
    def summary(self):
        print("==================Summary==================")
        self.split_not_test_data()
        self.parse_episode_log()
        self.parse_average_token_usage()
        print("=================Summary End===============")


if __name__ == "__main__":
    class Args:
        """
        class for argument input
        """
        config_name: str = "llm_spot_fetch_mobility"
        video_dir: str = "spot_fetch_mobility"
        dataset_dir: str = "mp3d/mobility_episodes_1.json.gz"
        ablation_mode: str = "group_discussion"
    
    new_args = Args()

    print("==================Task Summary==================")
    print("Bravo! You have finished one ablation experiment.")

    # default mode
    new_args.default = False
    print("==================Default Mode==================")
    default_mode = input("In default mode you only need to choose the number of config and ablation. Do you want to use default mode? (y/n): ")

    print("==================Config Name==================")
    print("The default config name are:")
    for key, value in config_name.items():
        print(f"{key}: {value}")
    config_choice = input("You can choose the index of them, or type 'n' if you want to input your own: ")
    if config_choice in config_name:
        new_args.config_name = config_name[config_choice]
        print(f"Your config name is {new_args.config_name}")
    else:
        print("Please input your task config name like llm_spot_fetch_mobility OR zxz_llm_dist_man: ")
        new_args.config_name = input("")

    print("==================Ablation Mode==================")
    print("The default ablation mode are:")
    for key, value in ablation_mode.items():
        print(f"{key}: {value}")
    ablation_choice = input("Please choose the index of them, or type 'n' if you want to input your own: ")

    if ablation_choice in ablation_mode:
        new_args.ablation_mode = ablation_mode[ablation_choice]
        print(f"Your ablation mode is {new_args.ablation_mode}")
    else:
        print("Please input your Ablation mode like group_discussion OR agent_reflection: ")
        new_args.ablation_mode = input("")

    set_default = False
    if default_mode == 'y':
        set_default = True
        if config_choice in dataset_path:
            new_args.dataset_dir = dataset_path[config_choice]
        else:
            print("==================Warning==================")
            print("No DEFAULT dataset path found in dataset!")
            set_default = False
        video_path = f"wo_{new_args.ablation_mode}/{video_dir[config_choice]}"
        if osp.exists(osp.join('video_multi', video_path)):
            new_args.video_dir =  video_path
        else:
            print("==================Warning==================")
            print("No DEFAULT video path found in video_multi!")
            set_default = False
        
    if not set_default:
        new_choice = True
        print("==================Dataset Path==================")
        if config_choice in dataset_path:
            print(f"Default dataset path according to your config is {dataset_path[config_choice]}")
            dataset_choice = input("Do you want to use it? (y/n): ")
            if dataset_choice == 'y':
                new_args.dataset_dir = dataset_path[config_choice]
                new_choice = False
        if new_choice:
            print("The default dataset path are:")
            for key, value in dataset_path.items():
                print(f"{key}: {value}")
            data_choice = input("You can choose the index of them, or type 'n' if you want to input your own: ")
            if data_choice in dataset_path:
                new_args.config_name = dataset_path[data_choice]
            else:
                print("Please input your Dataset relative path like mp3d/mobility_episodes_1.json.gz OR hssd/dist_man.json.gz: ")
                new_args.dataset_dir = input("")

        print("==================Video Path==================")
        new_choice = True
        if config_choice in video_dir:
            video_path = f"wo_{new_args.ablation_mode}/{video_dir[config_choice]}"
            video_choice = input(f"The default video path according to your config and video_dir are {video_path}, do you want to use it? (y/n): ")
            if video_choice == 'y':
                new_args.video_dir = video_path
                new_choice = False
        if new_choice:
            print("Please input your Video relative path like spot_fetch_mobility OR dist_man, we set the video_dir as video_multi as default: ")
            new_args.video_dir = input("")

    print("===================Thank You=====================")

    lgtm = LGTM(new_args)
    lgtm.summary()
