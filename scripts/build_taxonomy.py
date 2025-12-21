#!/usr/bin/env python3
import yaml, json, os, glob

ROOT = os.path.dirname(os.path.dirname(__file__))
POL_DIR = os.path.join(ROOT, '_policies')
REG = os.path.join(ROOT, 'data', 'registry.yaml')
OUT = os.path.join(ROOT, 'src', 'data')

def load_registry():
    with open(REG,'r',encoding='utf-8') as f:
        return yaml.safe_load(f)

def build_index(registry):
    index = {'sectors':{}, 'impacts':{}}
    policies = registry.get('policies',{})
    for pid,meta in policies.items():
        for s in meta.get('sectors',[]):
            index['sectors'].setdefault(s,[]).append(pid)
        for imp in meta.get('impacts',[]):
            index['impacts'].setdefault(imp,[]).append(pid)
    return index

def save(index):
    os.makedirs(OUT, exist_ok=True)
    p=os.path.join(OUT,'taxonomy_index.json')
    with open(p,'w',encoding='utf-8') as f:
        json.dump(index,f,indent=2)
    print('Wrote',p)

def main():
    registry=load_registry()
    index=build_index(registry)
    save(index)

if __name__=='__main__':
    main()
