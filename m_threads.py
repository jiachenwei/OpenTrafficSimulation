from task import *

mod = sys.argv[1]
path = sys.argv[2]

proportions = std_hdc_idc_cacc_proportions
traffic_densities = std_traffic_densities

if mod == '-1':
    std_task(proportions, traffic_densities, path)
elif mod == '-21':
    std_task(proportions[:6], traffic_densities, path)
elif mod == '-22':
    std_task(proportions[6:], traffic_densities, path)
elif mod == '-41':
    std_task(proportions[:6], traffic_densities[:6], path)
elif mod == '-42':
    std_task(proportions[:6], traffic_densities[6:], path)
elif mod == '-43':
    std_task(proportions[6:], traffic_densities[:6], path)
elif mod == '-44':
    std_task(proportions[6:], traffic_densities[6:], path)
else:
    print("Fail")
    pass
