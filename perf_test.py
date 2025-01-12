#!/usr/bin/env python3
"Launch a program with multiple thread counts and plot scalability curves."

example="""Example:
    perf_test.py --timer_location=-1,4 --best_of=5  --  ./intersection --max_tbb {t} --nb_plane 1000
    Note the use of:
    - '=' in =-1,4 otherwise -1 is parsed as an (unsupported) option.
    - '--' to separate the program's arguments from perf_test's arguments.
    - '--best_of' to smooth out the influence of other running processes.
"""

# Ideas:
#  --nox : to disable graph
#  --check-as-fast-as <REF> : should be within 10% of a reference run
#  --nb_threads=start:stop:step,extra1,extra2
#  handle mpirun and hybrid


import argparse
import os
import os.path as osp
from socket import gethostname
import subprocess
import time

import numpy as np
import matplotlib.pyplot as plt


# cpu_count = os.cpu_count()
# cpu_count = psutil.cpu_count(logical=True|False)
cpu_count = len(os.sched_getaffinity(0))  # best: it takes slurm's or taskset's limit into account
host = gethostname()
git = "tbd"

def cgroup_cpu_limit():
    """Query a potential CPU limit from cgroup."""
    # mem quota:
    # cat /sys/fs/cgroup/memory/user.slice/user-$(id -u).slice/memory.limit_in_bytes
    # CPU quota:
    # divide by 100000, since the value is 100% of 100ms / CPU:
    # cat /sys/fs/cgroup/cpu/user.slice/user-$(id -u).slice/cpu.cfs_quota_us
    try:
        userid=os.getuid()
        f = open("/sys/fs/cgroup/cpu/user.slice/user-%d.slice/cpu.cfs_quota_us"%userid)
        quota = int(f.read())
        return quota // 100000
    except Exception:
        # there is probably no cgroup on this machine, return the base value:
        return cpu_count

cpu_limit = cgroup_cpu_limit()

def run1(nb_threads, timer_location, program, extra_args):
    "Run program, return its timer."
    expanded_args = [ a.format(t=nb_threads) for a in extra_args]
    #print (expanded_args)
    start_time = time.time()
    #print('running', [program] + expanded_args)
    out = subprocess.run([program] + expanded_args, stdout=subprocess.PIPE)
    output = out.stdout.decode('utf-8').strip()  # strip blank lines, the use wouldn't see them
    #print(output)
    if timer_location:
        x,y = map(int, timer_location.split(','))
#        print("x,y=", x,y)
        lines = output.split('\n')
#        print(lines)
        line = lines[x]
#        print(line)
        dt = float(line.split()[y])
        return dt
    else:
        return time.time() - start_time


def campaign(min_threads, max_threads, timer_location, best_of, program, extra_args):
    "Run program with various numbers of threads, return the timers."
    results = []
    print("# Performance for git:%s on %s"%(git, host))
    print("# ", program, *extra_args)
    print("# nb_threads  dt(best of %d)"%best_of)
    for nb_threads in range(min_threads, 1+max_threads):
        dts = []
        for _ in range(best_of):
             dt = run1(nb_threads, timer_location, program, extra_args)
             dts.append(dt)
        mindt = min(dts)
        results.append((nb_threads, mindt))
        print(nb_threads, mindt)

    threads, dtimes = np.array(results).T
    #    print(threads, dtimes)
    return threads, dtimes


def graph(threads, dtimes, ref):
    """Draw results"""

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, sharex=True,
                                        figsize=(12, 6))
    ax0.set_title("timers")
    ax0.plot(threads, dtimes, '-o')

    th0 = threads[0]
    dt0 = dtimes[0]
    if (th0 != min(threads)): raise ValueError("threads should be sorted here")

    speedup = (dt0*th0)/dtimes

    ax1.set_title("speedup")
    ax1.plot(threads, speedup, '-o')

    eff = speedup / threads *100
    ax2.set_title("efficiency (%)")
    ax2.plot(threads, eff, '-o')

    if ref:
        # code is copy-pasted, could be factorized?
        threads, dtimes = np.loadtxt(ref).T
        ax0.plot(threads, dtimes, ":.")
        speedup = (dtimes[0]*threads[0])/dtimes
        ax1.plot(threads, speedup, ":.")
        eff = speedup / threads *100
        ax2.plot(threads, eff, ':.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--min_threads",
                        default=1, type=int,
                        help="Lower bound for nb_threads (default 1)")  # 1 thread is added to run if efficiency or speedup are plotted

    parser.add_argument("--max_threads",
                        default=cpu_limit, type=int,
                        help="Upper bound for nb_threads (default %(default)s)")

    parser.add_argument("--timer_location", help="Position of the timer in stdout, as (x,y) coordinates. Use e.g. --timer_location=-1,4 to get the fifth value on the last line (default is None, meaning the whole program is timed)")
    # timer_regexp? ou timer_filter?

    # parser.add_argument("--curves", help="which curves to draw"
    #                     )

    parser.add_argument("--ref", help="Data file of reference timers (default=./<program>.perf)")

    parser.add_argument("--best_of", type=int, default=3, help="Run BEST_OF times, keeping only the best timer (default=%(default)s, probably enough in most cases).")

    parser.add_argument("program", help="The program to run")
    parser.add_argument("extra_args", nargs='*', default=["--nb_threads={t}"], help="Pass these arguments to program. {t} is substituted by nb_threads (default: %(default)s)")

    args = parser.parse_args()
    # print(args)

    threads, dtimes = campaign(args.min_threads, args.max_threads, args.timer_location, args.best_of, args.program, args.extra_args)

    if args.ref is None:
        if osp.exists(args.program + osp.extsep + "perf"):
            args.ref = args.program + osp.extsep + "perf"

    graph(threads, dtimes, args.ref)

    plt.show()
