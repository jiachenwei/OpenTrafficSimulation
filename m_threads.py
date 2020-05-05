from example import *

mod = sys.argv[1]
path = sys.argv[2]

if mod == '-1':
    std_task(std_hdc_idc_proportions, std_traffic_densities, path)
elif mod == '-21':
    std_task(std_hdc_idc_proportions[:6], std_traffic_densities, path)
elif mod == '-22':
    std_task(std_hdc_idc_proportions[6:], std_traffic_densities, path)
elif mod == '-41':
    std_task(std_hdc_idc_proportions[:6], std_traffic_densities[:6], path)
elif mod == '-42':
    std_task(std_hdc_idc_proportions[:6], std_traffic_densities[6:], path)
elif mod == '-43':
    std_task(std_hdc_idc_proportions[6:], std_traffic_densities[:6], path)
elif mod == '-44':
    std_task(std_hdc_idc_proportions[6:], std_traffic_densities[6:], path)
else:
    print("Fail")
    pass
