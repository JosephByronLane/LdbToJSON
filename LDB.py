import os
from subprocess import Popen, PIPE
import json
import ast
import codecs

script_dir = os.path.dirname(os.path.realpath(__file__))
ldbdump_path = os.path.join(script_dir, 'ldbdump')
base = r"C:\Users\JOSE\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\pnfmiddhgnhjjfbdkigpaakldoohheel" #change URL HERE

all_entries = []

for f in os.listdir(base):
    if f.endswith(".ldb"):
        ldb_file_path = os.path.join(base, f)
        process = Popen([ldbdump_path, ldb_file_path], stdout=PIPE, text=True, encoding='utf-8')
        output, err = process.communicate()
        exit_code = process.wait()
        for line in output.split("\n")[1:]:
            if line.strip() == "":
                continue
            parsed = ast.literal_eval("{" + line + "}")
            key = next(iter(parsed.keys()))
            try:
                value = json.loads(parsed[key])
            except json.JSONDecodeError:
                print(f"Error decoding JSON for key: {key}")

                continue
            all_entries.append({"key": codecs.encode(key, 'unicode_escape').decode(), "value": value})

output_file_path = os.path.join(script_dir, 'output.json')
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_entries, json_file, ensure_ascii=False, indent=4)

print(f"Data has been written to {output_file_path}")