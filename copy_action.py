import json
import os
import re
import sys
from datetime import date
from os.path import expanduser

from richxerox import copy

config_path = os.getenv('ACCEL_SHOOTER_CONFIG_FILE')
with open(config_path) as f:
    config = json.load(f)
day = sys.argv[1] if len(sys.argv) >= 2 else date.today().strftime('%Y/%m/%d')
with open(expanduser(config['DailyProgressFile'])) as f:
    content = f.readlines()

match_result = re.search(rf'(### {day}.*?)\n###', ''.join(content), re.DOTALL)
record = match_result.group(1)
if re.search(r'2\. Today\n3\.', record):
    print('Today content is empty.')
    sys.exit()
item_regex = r'\* (\([A-Za-z ]+\)) \[(.*?)\]\((https:\/\/app.clickup.com\/t\/\w+)\).*'
result_record = record
for item in re.finditer(item_regex, record):
    full = item.group(0)
    status = item.group(1)
    title = item.group(2)
    clickUpUrl = item.group(3)
    result_record = result_record.replace(full, f'* {status} <a href="{clickUpUrl}">{title}</a>')
result_record = result_record.replace('  -', '&nbsp;&nbsp;-')
result_record = result_record.replace('    *', '&nbsp;&nbsp;&nbsp;&nbsp;*')
result_record = result_record.replace('\n', '<br/>')
copy(
    text=record,
    html=result_record
)
