

# mp3d
#python habitat-baselines/habitat_baselines/run.py --config-name=social_rearrange/llm_spot_fetch_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat.dataset.should_group_discussion=False habitat_baselines.video_dir="video_multi/wo_group_discussion/spot_fetch_mobility" habitat.dataset.should_terminate_on_wait=False

#python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/llm_multi_agent_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat.dataset.should_group_discussion=False habitat_baselines.video_dir="video_multi/wo_group_discussion/multi_agent_mobility" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=social_rearrange/llm_spot_fetch_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/spot_fetch_mobility" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/llm_multi_agent_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/mp3d_rearrange" habitat.dataset.should_terminate_on_wait=False

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/llm_multi_agent_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/mp3d_rearrange" habitat.dataset.should_terminate_on_wait=False habitat.dataset.data_path=data/datasets/mp3d/not_test/mp3d_rearrange_1.json.gz

python habitat-baselines/habitat_baselines/run.py --config-name=multi_rearrange/llm_multi_agent_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1 habitat_baselines.video_dir="video_multi/wo_full/mp3d_rearrange" habitat.dataset.should_terminate_on_wait=False habitat.dataset.data_path=data/datasets/mp3d/not_test/mp3d_rearrange_2.json.gz

python -u -m habitat_baselines.run --config-name=social_rearrange/llm_spot_fetch_mobility.yaml habitat_baselines.evaluate=True habitat_baselines.num_environments=1