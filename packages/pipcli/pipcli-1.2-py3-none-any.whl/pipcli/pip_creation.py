from .utils import *
import tempfile
import os
import shutil

PIP_TEMPLATE_GIT_URL = 'https://github.com/SquarePants1991/pip_template.git'
PIP_TEMPLATE_CACHE_REL_PATH = 'pip_template'
PIP_SCRIPT_TEMPLATE_REL_PATH = 'cli_template'

logger = create_logger()

def clear_pip_template():
    pip_template_cache_path = os.path.join(tempfile.gettempdir(), PIP_TEMPLATE_CACHE_REL_PATH)
    if os.path.exists(pip_template_cache_path):
        run_command('rm -rf {0}'.format(pip_template_cache_path))

def create_pip(pip_name, work_dir):
    clear_pip_template()
    pip_template_cache_path = os.path.join(tempfile.gettempdir(), PIP_TEMPLATE_CACHE_REL_PATH) 
    if not os.path.exists(pip_template_cache_path):
        logger.info('克隆项目模版：{0}'.format(pip_template_cache_path))
        run_command('git clone --depth=1 {0} {1}'.format(PIP_TEMPLATE_GIT_URL, pip_template_cache_path))
    else:
        logger.info('项目模版已存在')
    return process_script_template(pip_template_cache_path, pip_name, work_dir)


def process_script_template(pip_template_cache_path, pip_name, work_dir):
    script_template_path = os.path.join(pip_template_cache_path, PIP_SCRIPT_TEMPLATE_REL_PATH)
    if not os.path.exists(script_template_path):
        logger.error('脚本模版不存在于：{0}'.format(script_template_path))
        return False
    script_template_copy_target_path = os.path.join(work_dir, pip_name)
    logger.info('拷贝脚本项目模版')
    run_command('cp -r {0} {1}'.format(script_template_path, script_template_copy_target_path))

    keywords_map = { '__pip_name__': pip_name }
    logger.info('处理模版文件（目录）')
    replace_pip_template_keywords(script_template_copy_target_path, keywords_map)
    logger.info('处理完毕')


def replace_pip_template_keywords(root_dir, keywords_map):
    for file in os.listdir(root_dir):
        current_full_path = os.path.join(root_dir, file)
        logger.info(current_full_path + ' 完成！')
        for key in keywords_map:
            file = file.replace(key, keywords_map[key])
        new_full_path = os.path.join(root_dir, file)
        os.rename(current_full_path, new_full_path)
        if os.path.isfile(new_full_path):
            all_content = ''
            with open(new_full_path, 'r') as file_handler:
                all_content = file_handler.read()
                for key in keywords_map:
                    all_content = all_content.replace(key, keywords_map[key])
            with open(new_full_path, 'w+') as file_handler:
                file_handler.write(all_content)
        else:
            replace_pip_template_keywords(new_full_path, keywords_map)