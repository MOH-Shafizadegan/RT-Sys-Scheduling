from _func import *

# Files and folders addresses:
root = str(Path(__file__).parent) + "\\"
input_addr = root + 'inputs.txt'
rm_out_addr = root + 'outputs_rm.txt'
dm_out_addr = root + 'outputs_dm.txt'
ed_out_addr = root + 'outputs_ed.txt'
ap_out_addr = root + 'outputs_ap.txt'
imgs_folder_addr = root + 'imgs\\'
Path(imgs_folder_addr).mkdir(parents=True, exist_ok=True)

examples = file_reader(input_addr)

rm_results = rm_scheduler(examples,40)
dm_results = dm_scheduler(examples)
ed_results = ed_scheduler(examples)
interupt_time, interupt_job = 3, 8
ap_results = ap_rm_scheduler(examples, interupt_time, interupt_job)
save_figs(examples, rm_results, "RM", imgs_folder_addr)
save_figs(examples, dm_results, "DM", imgs_folder_addr)
save_figs(examples, ed_results, "ED", imgs_folder_addr)
save_figs(examples, ap_results, "AP", imgs_folder_addr)