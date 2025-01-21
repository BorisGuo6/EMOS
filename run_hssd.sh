

# hssd
#python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_dist_man.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat.dataset.should_group_discussion=False habitat_baselines.video_dir="video_multi/wo_group_discussion/dist_man" habitat.dataset.should_terminate_on_wait=False

#python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_height_man.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat.dataset.should_group_discussion=False habitat_baselines.video_dir="video_multi/wo_group_discussion/height_man" habitat.dataset.should_terminate_on_wait=False

#python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_height_per.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat.dataset.should_group_discussion=False habitat_baselines.video_dir="video_multi/wo_group_discussion/height_per" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_dist_man.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/dist_man" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_height_man.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/height_man" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/zxz_llm_height_per.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/height_per" habitat.dataset.should_terminate_on_wait=False
