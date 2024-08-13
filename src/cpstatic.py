import os
import shutil

def cp_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for fn in os.listdir(src):
        f_p = os.path.join(src, fn)
        d_p = os.path.join(dst, fn)

        print(f"=> From {f_p} -> To {d_p}")

        if os.path.isfile(f_p):
            shutil.copy(f_p, d_p)
        else:
            cp_dir(f_p, d_p)
