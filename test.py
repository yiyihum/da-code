from pathlib import Path
import re

def preprocess_py(py_path: str | Path):
    script_path = Path(__file__).parent / 'script.py'
    with open(script_path, 'r') as f:
        script_content = f.readlines()
    
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.readlines()
    py_content = [line for line in py_content if 'plt.close' not in line and \
                'matplotlib.pyplot.close' not in line]
    py_content = [line for line in py_content if 'plt.show' not in line and \
                'matplotlib.pyplot.show' not in line]
    find_main = None
    for idx, line in enumerate(py_content):
        if 'if __name__ == "__main__"' in line or "if __name__ == '__main__'" in line:
            find_main = idx
            break
    if find_main is not None:
        py_content = py_content[:find_main] + \
            [re.sub(r'^ {4}', '', line) for line in py_content[find_main+1:]]
    
    py_content = py_content + ['\n'] + script_content

    output_path = py_path.parent / 'getdata.py'
    
    with open(output_path, 'w') as f:
        f.writelines(py_content)

if __name__ == "__main__":
    py_path = 'benchmark/_result/opendevin-0615/plot-scatter-004/analysis.py'
    py_path = py_path if isinstance(py_path, Path) else Path(py_path)
    preprocess_py(py_path)
