from example import *

mod = sys.argv[1]
path = sys.argv[2]

if mod == '-0':
    std_task(std_hdc_idc_proportions, std_traffic_densities, path)
elif mod == '-1':
    std_task(std_hdc_idc_proportions[:5], std_traffic_densities[:5], path)
elif mod == '-2':
    std_task(std_hdc_idc_proportions[:5], std_traffic_densities[5:], path)
elif mod == '-3':
    std_task(std_hdc_idc_proportions[5:], std_traffic_densities[:5], path)
elif mod == '-4':
    std_task(std_hdc_idc_proportions[5:], std_traffic_densities[5:], path)
else:
    print("Fail")
    pass
