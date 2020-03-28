from datetime import date
from settings import  *

def write_log(errors, new_refs, start, end):
    errors = "\n".join(errors)
    date_str = date.today().strftime("%d%m%Y")
    outfile = date_str + '.txt'
    outpath = os.path.join(log_dir, outfile)
    with open(outpath, 'w+') as filehandle:
        filehandle.writelines(f"errors:{errors}")
        filehandle.writelines('\n---------------------\n')
        filehandle.writelines(f"time elapsed in seconds: {end - start}")
        filehandle.writelines('\n---------------------\n')

    # Update refs files
    outpath = r'resources\refs.txt'
    new_refs = "\n".join(new_refs)
    with open(outpath, 'a') as filehandle:
        filehandle.write(new_refs)
