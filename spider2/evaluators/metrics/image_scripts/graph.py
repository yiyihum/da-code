import matplotlib.pyplot as plt
import pickle, sys, argparse, yaml, os
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PathCollection


def parse_args(args):
    parser = argparse.ArgumentParser(description='Process integers.')
    parser.add_argument('-y', '--yaml', type=str, default='', help='File to store image yaml information') 
    return parser.parse_args()

def compare_numpy(hyp_np: np.ndarray, ref_np: np.ndarray, hyp_order: list, ref_order: list , tol=1e-5):
    if hyp_np.shape != ref_np.shape:
        return [], []
    if len(hyp_order) and len(ref_order):
        if np.allclose(hyp_np[list(hyp_order)], ref_np[list(ref_order)], atol=tol):
            return list(hyp_order), list(ref_order)
        else:
            return [], []
    hyp_order = np.argsort(hyp_np)
    sorted_hyp = hyp_np[hyp_order]
    ref_order = np.argsort(ref_np)
    sorted_ref = ref_np[ref_order]
    if np.allclose(sorted_hyp, sorted_ref, atol=1e-5):
        return list(hyp_order), list(ref_order)
    return [], []

parse = parse_args(sys.argv[1:])
yaml_path = parse.yaml
assert os.path.exists(yaml_path), f"{yaml_path} does not exist"
with open(yaml_path, 'r') as file:
    data = yaml.safe_load(file)
gt_npy = data.pop('gt_npy', '')
gt_colors = data.pop('colors', [])
gt_title = data.pop('title', '')
gt_fig = data.pop('figsize', {})
gt_order = data.pop('order', False)
gt_graph = data.pop('graph')
gt_xlabel = data.pop('xlabel', "")
gt_ylabel = data.pop('ylabel', "")
gt_xticks = data.pop('xticks', [])
gt_yticks = data.pop('yticks', [])
gt_label = data.pop('label', [])

width = gt_fig.get("width", None)
height = gt_fig.get("height", None)
gt_fig = (width, height)

ax, fig = plt.gca(), plt.gcf()
assert os.path.exists(gt_npy), f'{gt_npy} does not exist'
gt = np.load(gt_npy)
gt = gt.reshape(1,-1) if gt.ndim == 1 else gt

results = []
colors = []
if gt_graph == 'bar':
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            results.append(patch.get_height())
            colors.append(patch.get_facecolor())
        else:
            with open(r'./evaluation_results.pkl', 'wb') as f:
                pickle.dump(False, f)
                sys.exit()
    columns = gt.shape[1]
    results = [np.array(results[i:i+columns]) if i+columns <= len(results) else np.array(results[i:]) \
            for i in range(0, len(results),columns)]
    colors = list(set(colors))
elif gt_graph  == 'line':
    lines = ax.get_lines()
    if len(lines) == 0:
        with open('./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
    for line in lines:
        results.append(line.get_ydata())
        colors.append(line.get_color())
elif gt_graph  == 'pie':
    for patch in ax.patches:
        if isinstance(patch, Wedge):
            results.append(abs(patch.theta2 - patch.theta1) / 360)
            colors.append(patch.get_facecolor())
        else:
            with open(r'./evaluation_results.pkl', 'wb') as f:
                pickle.dump(False, f)
                sys.exit()
    gt = np.apply_along_axis(lambda x: x / np.sum(x), axis=1, arr=gt)
elif gt_graph == 'scatter':
    scatters = [child for child in ax.get_children() if isinstance(child, PathCollection)]
    if scatters:
        for scatter in scatters:
            results.append(scatter.get_offsets())
            colors.append(scatter.get_facecolor())
    else:
        with open(r'./evaluation_results.pkl', 'wb') as f:
                pickle.dump(False, f)
                sys.exit()
        
if gt_colors:
    colors = [mcolors.to_hex(rgb_tuple) for rgb_tuple in colors]
    if not colors == gt_colors:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_fig:
    figsize = fig.get_size_inches()
    if not gt_fig == figsize:
        with open(r'./evaluation_results.pkl', 'wb') as f:
                pickle.dump(False, f)
                sys.exit()
if gt_title:
    title = ax.get_title()
    if not gt_title == title:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_label:
    labels = [text.get_text() for text in ax.get_legend().get_texts()]
    if not gt_label == labels:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_xlabel:
    x_label = ax.get_xlabel()
    if not gt_xlabel == x_label:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_ylabel:
    y_label = ax.get_ylabel()
    if not gt_ylabel == y_label:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_xticks:
    xtick_labels = ax.get_xticklabels()
    xtick_texts = [label.get_text() for label in xtick_labels]
    if not gt_xticks == xtick_texts:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()
if gt_yticks:
    ytick_labels = ax.get_yticklabels()
    ytick_texts = [label.get_text() for label in ytick_labels]
    if not gt_yticks == ytick_texts:
        with open(r'./evaluation_results.pkl', 'wb') as f:
            pickle.dump(False, f)
            sys.exit()


output = []
hyp_order, ref_order = [], []

if not gt_order:
    for idx, result in enumerate(results):
        find = False
        result = np.array(result) if isinstance(result, list) else result
        for row in range(gt.shape[0]):
            gold = gt[row]
            hyp_temp_order, ref_temp_order = compare_numpy(hyp_np=result, ref_np=gold, hyp_order=hyp_order, ref_order=ref_order)
            if len(hyp_temp_order) and len(ref_temp_order) and idx == 0:
                hyp_order, ref_order = hyp_temp_order, ref_temp_order
                find = True
                break
            elif len(hyp_temp_order) and len(ref_temp_order):
                find = True
                break
        if not len(hyp_order) and not len(ref_order) and idx != 0:
            find = False
        output.append(find)
else:
    for idx, result in enumerate(results):
        find = False
        result = np.array(result) if isinstance(result, list) else result
        gold = gt[idx]
        if np.allclose(result, gold, atol=1e-5):
            find = True
        output.append(find)

comparison = True if all(output) else False
with open('./evaluation_results.pkl', 'wb') as f:
    pickle.dump(comparison, f)

