"""
Phân tích 64 mutants sống sót ở Baseline và đối chiếu với Final Mutation report
Để tìm ra:
- Mutator, Class, Method, Line, Description, Index
- Trạng thái Baseline (SURVIVED / NO_COVERAGE)
- Trạng thái Final (KILLED / SURVIVED)
- Killing Test trong Final (nếu có)
- Nhóm nguyên nhân gốc rễ (Root Cause Group)
"""
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict

def main():
    # 1. Đọc baseline_mutations.xml
    btree = ET.parse('reports/data/baseline_mutations.xml')
    b_muts = []
    for m in btree.getroot().findall('mutation'):
        st = m.get('status')
        b_muts.append({
            'status': st,
            'class': m.findtext('mutatedClass', ''),
            'method': m.findtext('mutatedMethod', ''),
            'line': m.findtext('lineNumber', ''),
            'mutator': m.findtext('mutator', '').split('.')[-1],
            'description': m.findtext('description', ''),
            'index': m.findtext('index', '')
        })

    # Lọc 64 non-killed ở baseline
    b_survs = [m for m in b_muts if m['status'] in ('SURVIVED', 'NO_COVERAGE')]
    print(f"Tổng baseline non-killed: {len(b_survs)}")

    # 2. Đọc final_mutations.xml
    ftree = ET.parse('reports/data/final_mutations.xml')
    f_muts = {}
    for m in ftree.getroot().findall('mutation'):
        key = (
            m.findtext('mutatedClass', ''),
            m.findtext('mutatedMethod', ''),
            m.findtext('lineNumber', ''),
            m.findtext('mutator', '').split('.')[-1],
            m.findtext('index', '')
        )
        f_muts[key] = {
            'status': m.get('status'),
            'killingTest': m.findtext('killingTest', ''),
            'description': m.findtext('description', '')
        }

    # 3. Ghép nối
    combined = []
    for b in b_survs:
        key = (b['class'], b['method'], b['line'], b['mutator'], b['index'])
        if key in f_muts:
            f = f_muts[key]
            combined.append({
                'class': b['class'],
                'simple_class': b['class'].split('.')[-1],
                'method': b['method'],
                'line': int(b['line']),
                'mutator': b['mutator'],
                'index': b['index'],
                'desc': b['description'],
                'b_status': b['status'],
                'f_status': f['status'],
                'killing_test': f['killingTest']
            })
        else:
            print(f"KHÔNG TÌM THẤY KEY: {key}")

    print(f"Tổng combined: {len(combined)}")

    # Sắp xếp theo class, line, mutator, index
    combined.sort(key=lambda x: (x['simple_class'], x['line'], x['mutator'], x['index']))

    # In ra danh sách chi tiết
    print("\n--- DANH SÁCH 64 SURVIVORS VÀ KILLING TEST ---")
    for i, c in enumerate(combined, 1):
        kt_simple = c['killing_test'].split('/')[-1] if c['killing_test'] else "NONE (Equivalent)"
        print(f"{i:2d} | {c['simple_class']:<16} | L{c['line']:<3} | {c['method']:<28} | {c['mutator']:<34} | {c['b_status']:<11} | {kt_simple}")

    # 4. Phân nhóm RCA
    print("\n--- PHÂN TÍCH NHÓM RCA ---")
    g_no_cov = []
    g_aliasing = []
    g_void = []
    g_return = []
    g_bva = []
    g_decision = []

    for c in combined:
        cls = c['simple_class']
        line = c['line']
        mut = c['mutator']
        b_st = c['b_status']
        
        # Nhóm NO_COVERAGE
        if b_st == 'NO_COVERAGE':
            g_no_cov.append(c)
        # Nhóm MockMvc Aliasing & Redundant Assignment
        elif (cls == 'PetController' and line in (190, 192, 193, 194) and mut in ('VoidMethodCallMutator', 'RemoveConditionalMutator_EQUAL_ELSE')) or (cls == 'OwnerController' and line == 167):
            g_aliasing.append(c)
        # Nhóm Deep state / Return values
        elif mut == 'EmptyObjectReturnValsMutator':
            g_return.append(c)
        # Nhóm VoidMethodCallMutator
        elif mut == 'VoidMethodCallMutator':
            g_void.append(c)
        # Nhóm BVA & Math
        elif (cls == 'PetValidator' and line == 46) or (cls == 'OwnerController' and line == 144) or (cls == 'OwnerController' and line == 110) or (cls == 'VisitController' and line == 85) or (cls == 'PetTypeFormatter' and line == 48) or (cls == 'PetController' and line == 188 and mut == 'RemoveConditionalMutator_EQUAL_IF'):
            g_bva.append(c)
        else:
            g_decision.append(c)

    print(f"Group 1 (MockMvc Aliasing / Redundant): {len(g_aliasing)}")
    print(f"Group 2 (Void Method Calls / Side-effects): {len(g_void)}")
    print(f"Group 3 (BVA / Arithmetic Logic): {len(g_bva)}")
    print(f"Group 4 (Deep State / Return Values): {len(g_return)}")
    print(f"Group 5 (No Coverage / Unreached Branches): {len(g_no_cov)}")
    print(f"Group 6 (Decision Table / Complex Conditions): {len(g_decision)}")
    total_g = len(g_aliasing) + len(g_void) + len(g_bva) + len(g_return) + len(g_no_cov) + len(g_decision)
    print(f"TỔNG CỘNG: {total_g} / 64")

    print("\n--- CHI TIẾT GROUP 6 (DECISION TABLE) ---")
    for c in g_decision:
        print(f"  {c['simple_class']}:{c['line']} | {c['method']} | {c['mutator']} | {c['desc']}")

if __name__ == '__main__':
    main()
