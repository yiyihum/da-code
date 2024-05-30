# import operator
import numpy as np
import re
from typing import List
from PIL import Image
import os, uuid, pickle
from dataclasses import dataclass
import sys
from pathlib import Path
here = Path(__file__).absolute().parent.parent
sys.path.append(str(here.parent))
from controllers.python import PythonController
# from envs.spider2 import DEFAULT_WORK_DIR

DEFAULT_WORK_DIR = '/workspace'
def preprocess_py(py_path: str):
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.readlines()
    py_content = [line for line in py_content if 'plt.close()' not in line and \
                  'matplotlib.pyplot.close()' not in line]
    py_content = [line for line in py_content if 'plt.show()' not in line and \
                  'matplotlib.pyplot.show()' not in line]
    find_main = None
    for idx, line in enumerate(py_content):
        if 'if __name__ == "__main__"' in line or "if __name__ == '__main__'" in line:
            find_main = idx
            break
    if find_main is not None:
        py_content = py_content[:find_main] + \
            [re.sub(r'^ {4}', '', line) for line in py_content[find_main+1:]]
    return py_content

    
@dataclass
class ImageTest:
    dir: str = str(Path(__file__).absolute().parent / "image_scripts")
    container_name : str= "spider2"

    @staticmethod
    def find_plt_py(mnt_dir: str, result: str):
        image_name = os.path.basename(result)
        py_files = [os.path.join(mnt_dir, py_path) for py_path in os.listdir(mnt_dir) \
                if os.path.isfile(os.path.join(mnt_dir, py_path)) and py_path.endswith('.py')]
        
        assert len(py_files) > 0, f"{mnt_dir} contains no py files"

        '''
        Find the py file used to generate the result image
        '''
        def is_matplotlib(filename: str, imagename: str):
            with open(filename, 'r') as f:
                file_content = f.readlines()
            plt_find, image_find = False, False
            for line in file_content:
                if 'matplotlib' in line:
                    plt_find = True
                if imagename in line and ('plt.savefig' in line or 'matplotlib.pyplot.savefig' in line):
                    image_find = True
                if plt_find and image_find:
                    return True
            return False
        
        plt_files = [py_path for py_path in py_files if is_matplotlib(py_path, image_name)] 

        return plt_files
    
    @classmethod
    def evaluate_graph(cls, py_content: List[str], gt: str, mnt_dir: str, controller: PythonController):
        graph_file = os.path.join(cls.dir, f'graph.py')
        assert os.path.exists(graph_file), f'{graph_file} does not exist'
        with open(graph_file, 'r') as f:
            graph_content = f.readlines()

        # add ground truth to the code
        gt = os.path.abspath(gt).replace(os.path.abspath(mnt_dir), DEFAULT_WORK_DIR) \
            if not gt.startswith(DEFAULT_WORK_DIR)\
            else gt
        
        graph_import, graph_code = graph_content[0:6], graph_content[6:]
        test_code = graph_import + py_content + graph_code
        test_path = os.path.join(mnt_dir, str(uuid.uuid4())[:4] + '_eval.py')
        with open(test_path, 'w') as f:
            f.writelines(test_code)
        controller.container.exec_run(cmd=f'bash -c "python {os.path.basename(test_path)} -y {gt}"', workdir=DEFAULT_WORK_DIR)
        output_path = os.path.join(mnt_dir, 'evaluation_results.pkl')
        assert os.path.exists(output_path), f'{output_path} does not exist'
        with open(output_path, 'rb') as file:
            loaded = pickle.load(file)
    
        return loaded
    

def compare_image(result: str, expected: List[str], **options):
    """ 
    @args:
        result(str): the pred image file
        expect(str|List[str]): the gold image file or image files, maybe multiple potential answers, not there are two answers
        option(dict): the configuration dictionary
    """
    if isinstance(expected, List):
        mnt_dir = options.pop('mnt_dir')
        controller = options.pop('controller')
    else:
        raise TypeError('expected must be List, which contains of image and npy files')
    if not isinstance(result, str):
        raise TypeError('result must be str')
    
    result_img = np.array(Image.open(result))
    expected_yaml = [gt for gt in expected if gt.endswith('.yaml')]
    assert len(expected_yaml) == 1, "expect a yaml file containing ground truth of figure in graph"
    expected_imgs = [np.array(Image.open(gt)) for gt in expected if gt not in expected_yaml]
    
    # Image Testing
    for gt in expected_imgs:
        sample_image_stat = (
            result_img.shape == gt.shape
            and np.allclose(result, gt)
        )
        if sample_image_stat:
            return 1.0
    
    # Code Testing
    assert os.path.exists(mnt_dir), 'Please provide correct mount directory'
    
    plt_files = ImageTest.find_plt_py(mnt_dir=mnt_dir, result=result)
    assert len(plt_files) > 0, 'Expect files that uses matplotlib to generates code'

    
    for py_file in plt_files:
        py_lines = preprocess_py(py_path=py_file)
        result = ImageTest.evaluate_graph(py_content=py_lines, gt=expected_yaml[0], \
                    mnt_dir=mnt_dir, controller=controller)
        if result:
            return 1.0
    return 0.0
