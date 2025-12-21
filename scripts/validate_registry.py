#!/usr/bin/env python3
import yaml, os

ROOT = os.path.dirname(os.path.dirname(__file__))
REG = os.path.join(ROOT, 'data', 'registry.yaml')

def main():
    with open(REG,'r',encoding='utf-8') as f:
        reg=yaml.safe_load(f)
    defs=reg.get('taxonomy_definitions',{})
    valid_sectors={s['id'] for s in defs.get('sectors',[])}
    valid_impacts={s['id'] for s in defs.get('impacts',[])}
    errors=[]
    for pid,meta in reg.get('policies',{}).items():
        for s in meta.get('sectors',[]):
            if s not in valid_sectors:
                errors.append(f"Policy {pid} references unknown sector '{s}'")
        for imp in meta.get('impacts',[]):
            if imp not in valid_impacts:
                errors.append(f"Policy {pid} references unknown impact '{imp}'")
    if errors:
        print('Validation errors:')
        for e in errors:
            print('- ',e)
        raise SystemExit(2)
    print('Registry validation passed')

if __name__=='__main__':
    main()
