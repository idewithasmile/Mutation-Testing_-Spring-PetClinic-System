"""
Script kiểm chứng hình thức tính tương đương (Equivalence Verification) của 3 Equivalent Mutants
1. Owner.java:108 - RemoveConditionalMutator_EQUAL_IF (index 39)
2. Owner.java:108 - RemoveConditionalMutator_EQUAL_IF (index 42)
3. OwnerController.java:167 - VoidMethodCallMutator (index 50)
"""

def objects_equals(a, b):
    return a == b

def original_condition(existing_id, pet_id):
    existing_is_new = (existing_id is None)
    pet_is_new = (pet_id is None)
    return (not existing_is_new) and (not pet_is_new) and objects_equals(existing_id, pet_id)

def mutant1_condition(existing_id, pet_id):
    # Mutator: RemoveConditionalMutator_EQUAL_IF on !existingPet.isNew() -> replaced with true
    existing_is_new = (existing_id is None)
    pet_is_new = (pet_id is None)
    return True and (not pet_is_new) and objects_equals(existing_id, pet_id)

def mutant2_condition(existing_id, pet_id):
    # Mutator: RemoveConditionalMutator_EQUAL_IF on !pet.isNew() -> replaced with true
    existing_is_new = (existing_id is None)
    pet_is_new = (pet_id is None)
    return (not existing_is_new) and True and objects_equals(existing_id, pet_id)

def test_owner_line_108_exhaustive():
    domain_values = [None, 1, 2] # None (new), 1, 2 (persisted IDs)
    total_combinations = 0
    matches_m1 = 0
    matches_m2 = 0

    print("=== KIỂM CHỨNG VÉT CẠN OWNER.JAVA:108 ===")
    print(f"{'existing_id':<12} | {'pet_id':<10} | {'Original':<10} | {'Mutant1':<10} | {'Mutant2':<10} | {'Match?'}")
    print("-" * 65)

    for ex_id in domain_values:
        for p_id in domain_values:
            total_combinations += 1
            c_orig = original_condition(ex_id, p_id)
            c_m1 = mutant1_condition(ex_id, p_id)
            c_m2 = mutant2_condition(ex_id, p_id)

            match1 = (c_orig == c_m1)
            match2 = (c_orig == c_m2)
            if match1:
                matches_m1 += 1
            if match2:
                matches_m2 += 1

            status = "EQUIVALENT" if (match1 and match2) else "DIFFERENT"
            print(f"{str(ex_id):<12} | {str(p_id):<10} | {str(c_orig):<10} | {str(c_m1):<10} | {str(c_m2):<10} | {status}")

    print("-" * 65)
    print(f"Tổng số tổ hợp kiểm thử: {total_combinations}")
    print(f"Số tổ hợp Mutant 1 khớp Original: {matches_m1}/{total_combinations} (100.0%)")
    print(f"Số tổ hợp Mutant 2 khớp Original: {matches_m2}/{total_combinations} (100.0%)")
    assert matches_m1 == total_combinations, "LỖI: Mutant 1 không tương đương!"
    assert matches_m2 == total_combinations, "LỖI: Mutant 2 không tương đương!"
    print("=> KẾT LUẬN: Đột biến index 39 và 42 tại Owner.java:108 là EQUIVALENT 100% trên toàn bộ không gian trạng thái.\n")

def test_owner_controller_line_167_flow():
    print("=== KIỂM CHỨNG LUỒNG ĐIỀU KHIỂN OWNERCONTROLLER.JAVA:167 ===")
    test_cases = [
        {"owner_id_field": 1, "url_id": 1, "has_errors": False, "expect_guard_pass": True},
        {"owner_id_field": 1, "url_id": 2, "has_errors": False, "expect_guard_pass": False},
        {"owner_id_field": 2, "url_id": 1, "has_errors": False, "expect_guard_pass": False},
        {"owner_id_field": None, "url_id": 1, "has_errors": False, "expect_guard_pass": False},
    ]

    for tc in test_cases:
        f_id = tc["owner_id_field"]
        u_id = tc["url_id"]
        guard_mismatch = not objects_equals(f_id, u_id)
        
        if guard_mismatch:
            print(f"Case owner.id={f_id}, url_id={u_id} -> Bị guard chặn (redirect edit), KHÔNG BAO GIỜ chạm dòng 167.")
        else:
            # Chạm dòng 167
            id_before = f_id
            # Lệnh gốc: owner.setId(url_id)
            id_after_orig = u_id
            # Lệnh mutant: không làm gì
            id_after_mutant = id_before

            print(f"Case owner.id={f_id}, url_id={u_id} -> Vượt qua guard, chạm dòng 167:")
            print(f"   Original ID sau dòng 167: {id_after_orig}")
            print(f"   Mutant ID sau dòng 167:   {id_after_mutant}")
            assert id_after_orig == id_after_mutant, "LỖI: Trạng thái ID bị lệch!"
            print(f"   => Trạng thái HOÀN TOÀN ĐỒNG NHẤT ({id_after_orig} == {id_after_mutant}).")

    print("=> KẾT LUẬN: Đột biến xóa setId tại OwnerController.java:167 là EQUIVALENT 100% do guard bất biến.\n")

if __name__ == "__main__":
    test_owner_line_108_exhaustive()
    test_owner_controller_line_167_flow()
