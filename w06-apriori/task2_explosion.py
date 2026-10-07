#!/usr/bin/env python3
"""Week 6 · Task 2 — Lower the threshold until your machine says no.

Textbook §6.1, §6.2.

Support is a knob, and turning it down is how you find the interesting rules.
It is also how you run out of memory, and where that happens is a fact about
your laptop rather than about the algorithm.

    python3 task2_explosion.py --supports 400,200,100,50,25
    python3 task2_explosion.py --supports 12,6            # careful

Lower the threshold until something gives. Write down where and what.
"""
import argparse, json, os, platform, time, tracemalloc
import ctypes
if os.name == "nt":
    import winreg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def machine():
    details = {"platform": platform.platform(),
               "processor": platform.processor() or platform.machine(),
               "python": platform.python_version(),
               "background": "Codex desktop session; full host process inventory unavailable in sandbox"}
    if os.name == "nt":
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                details["processor"] = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except OSError as error:
            details["cpu_note"] = str(error)
        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
                (name, ctypes.c_ulonglong) for name in
                ("total_physical", "available_physical", "total_page", "available_page",
                 "total_virtual", "available_virtual", "extended_virtual")]
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            details["ram_bytes"] = status.total_physical
            details["available_ram_bytes_at_start"] = status.available_physical
    return details


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--supports", default="400,200,100,50,25")
    a = p.parse_args()
    os.makedirs(OUT, exist_ok=True)

    import bench
    from task3_pcy import PlainApriori
    baskets = bench.build()

    metadata = machine()
    rows = []
    for support in [int(x) for x in a.supports.split(",")]:
        algo = PlainApriori(support)
        tracemalloc.start()
        t0 = time.perf_counter()
        pairs = algo.run(baskets)
        elapsed = time.perf_counter() - t0
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        row = {"support": support, "frequent_pairs": len(pairs),
               "peak_counters": algo.peak_counters, "seconds": elapsed,
               "peak_bytes": peak_bytes}
        rows.append(row)
        print(f"  support {support:>5}   pairs {len(pairs):>7,}   "
              f"counters {algo.peak_counters:>10,}   "
              f"{elapsed:>7.2f}s   {peak_bytes / 1e6:>8.1f} MB")

    path = os.path.join(OUT, "explosion.json")
    prior = json.load(open(path)) if os.path.exists(path) else {"runs": []}
    prior["machine"] = metadata
    prior["runs"].extend(rows)
    json.dump(prior, open(path, "w"), indent=2)
    print(f"\n  -> out/explosion.json  ({len(prior['runs'])} run(s))")
    print("  Keep halving the support until it is unbearable. Record where.")


if __name__ == "__main__":
    main()
