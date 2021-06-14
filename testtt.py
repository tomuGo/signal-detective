import json
import filter_json
import numpy as np
# s = "{'notch':{'filter_frequency':2}}"
# text = []
# text.append(s)
ss = "[{\"bandpass\":{\"filter_min_frequency\":11,\"filter_max_frequency\":30}},{\"notch\":{\"filter_frequency\":2}}]"
#text.append(ss)
qq = [0]*1250
filter = filter_json.FilterJson(qq,ss,250)
filter.run()
aa = np.zeros(1250*1250)
aa = aa.reshape(1250,1250)
print(aa.value())

