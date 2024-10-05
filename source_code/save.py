import os
import io
import sys

def save_output(m=None):
    cur_dir = os.path.dirname(__file__)
    path_to_output_folder = os.path.join(cur_dir, '..', 'outputs')
    
    original_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    m.display()
    
    sys.stdout = original_stdout
    output = captured_output.getvalue()
    # with open('output.txt', 'w') as f:
    #     f.write(output)
    
    max_file_size = 100 * 1000 * 1000 #100 MB Beschränkung auf GitHub: 100 * 1024 * 1024
    
    def write_output_to_files(output, base_filename, max_file_size):
        file_index = 1
        bytes_written = 0
        buffer = []
        for line in output.splitlines(keepends=True):
            buffer.append(line)
            bytes_written += len(line.encode('utf-8'))
            if bytes_written >= max_file_size:
                file_name = '{}_{}.txt'.format(base_filename, file_index)
                file_path = os.path.join(path_to_output_folder, file_name)
                with open(file_path, 'w') as f:
                    f.writelines(buffer)
                buffer = []
                bytes_written = 0
                file_index += 1
        if buffer:
            file_name = '{}_{}.txt'.format(base_filename, file_index)
            file_path = os.path.join(path_to_output_folder, file_name)
            with open(file_path, 'w') as f:
                f.writelines(buffer)
    
    write_output_to_files(output, 'output', max_file_size)
    