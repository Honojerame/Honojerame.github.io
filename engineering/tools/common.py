"""Small, dependency-free tool driver. Tool binaries can be overridden in the environment."""
from pathlib import Path
import json, os, shlex, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
RESULTS = ROOT / "results"
BUILD.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

def command(name):
    return shlex.split(os.environ.get(name.upper(), name))

def run(args, **kwargs):
    p = subprocess.run(args, text=True, capture_output=True, **kwargs)
    if p.returncode:
        raise RuntimeError(f"Command failed: {shlex.join(map(str,args))}\n{p.stdout}\n{p.stderr}")
    return p.stdout

def compile_sv(project, top, params=None):
    project = ROOT / "projects" / project
    out = BUILD / (top + "_" + "_".join(f"{k}{v}" for k,v in (params or {}).items()))
    args = command("iverilog") + ["-g2012", "-s", top, "-o", str(out)]
    for k,v in (params or {}).items(): args += [f"-P{top}.{k}={v}"]
    args += [str(f) for f in sorted((project/"rtl").glob("*.sv"))]
    args += [str(project/"tb"/(top+".sv"))]
    run(args)
    return out

def simulate(executable, **args):
    if os.environ.get("WAVES"): args["VCD"]=1
    return run(command("vvp") + [str(executable)] + [f"+{k}={v}" for k,v in args.items()], timeout=90, cwd=BUILD)

def save_result(name, data):
    (RESULTS/(name+".json")).write_text(json.dumps(data, indent=2)+"\n")
    print(f"PASS {name}: {data['tests']} tests")
