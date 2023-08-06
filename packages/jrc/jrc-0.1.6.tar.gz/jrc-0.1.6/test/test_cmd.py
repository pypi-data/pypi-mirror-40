from jrc import main
import os

current_file_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_command():
    json_path = os.path.join(current_file_dir_path, "..", "demo", "json")
    zion_path = os.path.join(current_file_dir_path, "..", "demo", "zion")
    pipeline_path = os.path.join(current_file_dir_path, "..", "demo", "pipeline")
    # 进入到相应目录执行编译命令
    for path in [json_path, zion_path, pipeline_path]:

        os.chdir(path)
        try:
            main(("compile",))
        except SystemExit as e:
            assert e.code == 0
