from collections import defaultdict
from income_processing import County
import pdb

county_dict = defaultdict(list)
counties = []
with open('allagi.csv') as fp:
    line = fp.readline()
    fields = line.split(',')
    state_idx = fields.index('STATE')
    county_idx = fields.index('COUNTYNAME')
    income_range_idx = fields.index('agi_stub')
    total_idx = fields.index('N1')
    joint_idx = fields.index('MARS2')
    head_idx = fields.index('MARS4')

    income_ranges = [1, 10, 25, 50, 75, 100, 200, 500]
    last_key = None
    for line in fp.readlines():
        fields = line.split(',')
        state = fields[state_idx]
        county = fields[county_idx]
        key = state + ':' + county
        income_level = fields[income_range_idx]
        joint = int(float(fields[joint_idx]))
        head = int(float(fields[head_idx]))
        total = int(float(fields[total_idx]))

        last_key = last_key or key  # initialize first time around

        if key != last_key:
            # this is a new county
            # create the county object
            obj = County(last_key, county_dict[last_key])
            if obj:
                counties.append(obj)
            last_key = key

        county_dict[key].append(head + joint)

print('Found {} counties'.format(len(counties)))

for v in counties[:5]:
    print(v)