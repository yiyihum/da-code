# import operator
import numpy as np
import re
import os, shutil
import sys
from typing import Type
from pathlib import Path
here = Path(__file__).absolute().parent
sys.path.append(str(here.parent))
from controllers.python import PythonController

# from envs.spider2 import DEFAULT_WORK_DIR    
class PlotPy:
    script_path = str(Path(__file__).absolute().parent / 'scripts/image.py')

    @classmethod
    def preprocess_py(cls, py_path: str):

        with open(cls.script_path, 'r') as f:
            script_content = f.readlines()
        
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
        
        py_content = script_content[:30] + py_content + script_content[32:]

        return py_content

    @staticmethod
    def find_plt_py(mnt_dir: str):
        py_files = [os.path.join(mnt_dir, py_path) for py_path in os.listdir(mnt_dir) \
                if os.path.isfile(os.path.join(mnt_dir, py_path)) and py_path.endswith('.py')]
        assert len(py_files) > 0, f"{mnt_dir} contains no py files"

        '''
        Find the py file used to generate the result image
        '''
        def is_matplotlib(filename: str):
            if os.path.basename(filename) == 'plot.py':
                return True
            with open(filename, 'r') as f:
                file_content = f.readlines()
            plt_find, image_find = False, False
            for line in file_content:
                if 'matplotlib' in line:
                    plt_find = True
                if 'plt.savefig' in line or 'matplotlib.pyplot.savefig' in line:
                    image_find = True
                if plt_find and image_find:
                    return True
            return False

        plt_files = [py_path for py_path in py_files if is_matplotlib(py_path)] 
        
        return plt_files
    

def plot_process(mnt_dir: str,controller: Type[PythonController]):
    '''
    This function is used to process the plot results
    save the plot information to the /mnt_dir/dabench/plot.json
    '''
    mnt_files = os.listdir(mnt_dir)
    png_files = [file for file in mnt_files if file.endswith('.png') or file.endswith('.jpg')]
    assert len(png_files) > 0, 'Agent fails to plot image'

    controller.container.exec_run('basch -c cd /workspace')
    plot_path = os.path.join(mnt_dir, 'dabench')
    os.makedirs(plot_path, exist_ok=True)

    plt_files = PlotPy.find_plt_py(mnt_dir)
    assert len(plt_files) > 0, f"Agent fails to generate code to plot image, please check again."

    plot_find = False
    npy_file, json_file = '', ''
    for py_file in plt_files:
        py_content = PlotPy.preprocess_py(py_file)
        with open(py_file, 'w') as py:
            py.writelines(py_content)
        controller.container.exec_run(f'python {os.path.basename(py_file)}')
        mnt_files = os.listdir(mnt_dir)
        npy_files = [os.path.join(mnt_dir, file) for file in mnt_files if file.endswith('.npy') and '_data_result_' in file]
        json_files = [os.path.join(mnt_dir, file) for file in mnt_files if file.endswith('.json') and '_result_image_parameters_' in file]
        if npy_files and json_files:
            plot_find = True
            npy_file, json_file = npy_files[0], json_files[0]
            break
        else:
            unused_files = npy_files + json_files
            for file in unused_files:
                os.remove(file)

    if plot_find:
        plot_json = os.path.join(plot_path, 'plot.json')
        npy_path = os.path.join(plot_path, 'result.npy')
        shutil.move(json_file, plot_json)
        shutil.move(npy_file, npy_path)
    else:
        plot_json, npy_path = '', ''

    
    assert plot_json or npy_path, f'fails to generate plot json result'

    return [plot_json, npy_path]
