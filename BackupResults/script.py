"""
main.py

Copyright 2020 LEAP Australia Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author:
    Khesh Selvaganapathi
    Nish Joseph

Discription:
    ACT backup ANSYS Mechanical results with options to append timestamps
    design point number and copy of input file.
"""

import os
import shutil
import datetime
import wbjn


extensions = ['rst', 'rth', 'rmg']


def copy_rst(result, stepinfo, collector):
    file_name = result.Properties['filename'].Value
    use_timestamp = True if result.Properties['timestamp'].Value == 'Yes' else False
    use_dp = True if result.Properties['designpoint'].Value == 'Yes' else False
    backup_input = True if result.Properties['input'].Value == 'Yes' else False
    directory = result.Properties['directory'].Value

    for ext in extensions:
        rst_file = os.path.join(result.Analysis.WorkingDir, 'file.' + ext)
        if not os.path.exists(rst_file):
            continue

        if use_dp:
            dp_num = wbjn.ExecuteCommand(
                ExtAPI, 'returnValue(Parameters.GetCurrentDesignPoint().Name)')
            file_name = 'dp{0}_{1}'.format(dp_num, file_name)

        if use_timestamp:
            current_time = datetime.datetime.now()
            string_time = current_time.strftime('%d-%m-%y_%H-%M-%S')
            file_name = '{0}_{1}'.format(string_time, file_name)

        trg_file = os.path.join(directory,  file_name + '.' + ext)
        shutil.copy(rst_file, trg_file)

        if backup_input:
            input_file = os.path.join(result.Analysis.WorkingDir, 'ds.dat')
            trg_file = os.path.join(directory,  file_name + '.'+ ext + '.dat')
            shutil.copy(input_file, trg_file)

    for nodeid in collector.Ids:
        collector.SetValues(nodeid, (0.0,))
        break
