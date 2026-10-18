# Đặc tả và ánh xạ 45 test TV3

Quy ước: tiền điều kiện chung là object mới và fixture hợp lệ nếu không ghi khác.
Expected là hành vi source tại snapshot `589a505`; trạng thái `GAP` nói rõ
assertion chưa có, không phải kết quả PASS. Chi tiết kỹ thuật EP/BVA/Decision
Table nằm trong [DESIGN_TABLES.md](DESIGN_TABLES.md).

## OwnerMutationTests — TV3-O01…O27

| ID | Chức năng / kỹ thuật | Tiền điều kiện và input | Expected | Java method / rủi ro |
|---|---|---|---|---|
| O01 | addPet, DT A1 | Owner rỗng; `null` | pets rỗng | `addPetIgnoresNull`; bỏ guard null |
| O02 | addPet, DT A2 | Owner rỗng; pet mới Buddy | chứa đúng Buddy | `addPetAddsNewPet`; không thêm pet |
| O03 | addPet, DT A3 | cùng persisted pet id=5 thêm hai lần | size 1 | `addPetRejectsSameInstanceTwice`; contains/duplicate |
| O04 | addPet, DT A4 | cùng transient instance thêm hai lần | size 1 | `addPetRejectsSameNewInstanceTwice`; guard contains |
| O05 | addPet, DT A5 | hai instance persisted id=5 | giữ instance đầu | `addPetRejectsDifferentInstanceWithSameId`; ID duplicate |
| O06 | addPet, DT A6 | pets id=5 và id=6 | size 2 | `addPetAllowsDifferentIds`; so ID sai |
| O07 | addPet, DT A7 | hai transient instance khác nhau | size 2 | `addPetAllowsTwoNewPets`; coi null IDs là duplicate |
| O08 | addPet, DT A8 | persisted rồi transient | size 2 | `addPetAllowsNewPetAlongsidePersistedPet`; nhánh isNew |
| O09 | addPet, DT A9 | transient rồi persisted | size 2 | `addPetAllowsPersistedPetAfterNewPet`; nhánh isNew |
| O10 | getPet(id), EP | id=5 và id=6; tìm 5 | đúng instance id=5 | `getPetByIdReturnsMatchingPet`; lookup sai |
| O11 | getPet(id), EP | chỉ id=5; tìm 42 | `null` | `getPetByIdReturnsNullWhenAbsent`; fallback sai |
| O12 | getPet(id), state | chỉ pet mới; tìm 5 | `null` | `getPetByIdSkipsNewPets`; không bỏ new |
| O13 | getPet(id), null | new và id=5; tìm `(Integer)null` | `null` | `getPetByIdWithNullIdReturnsNull`; equals/null |
| O14 | getPet(name), EP | Buddy persisted; `buddy`, `BUDDY` | đúng Buddy | `getPetByNameIsCaseInsensitive`; case sensitivity |
| O15 | getPet(name), EP | Buddy; tìm Max | `null` | `getPetByNameReturnsNullWhenAbsent`; fallback |
| O16 | getPet(name), null field | pet name null rồi Buddy | bỏ null name, trả Buddy/null | `getPetByNameSkipsPetsWithNullName`; null dereference |
| O17 | getPet(name,bool), DT N3 | Rex mới; `ignoreNew=true` | `null` | `getPetByNameWithIgnoreNewSkipsNewPet`; ignoreNew |
| O18 | getPet(name,bool), DT N4 | Rex persisted; `ignoreNew=true` | đúng Rex | `getPetByNameWithIgnoreNewReturnsPersistedPet`; lọc sai |
| O19 | overload name, DT N5 | Rex mới; `false` và overload | đúng Rex | `getPetByNameWithoutIgnoreNewReturnsNewPet`; default sai |
| O20 | addVisit, DT AV4 | pet id=7; Visit Annual checkup | visits chứa đúng Visit | `addVisitDelegatesToPet`; side effect mất |
| O21 | addVisit, EP null | petId null; Visit khác null | IAE, `Pet identifier must not be null!` | `addVisitRejectsNullPetId`; guard/message |
| O22 | addVisit, EP null | pet id=7; visit null | IAE, `Visit must not be null!` | `addVisitRejectsNullVisit`; guard/message |
| O23 | addVisit, EP unknown | chỉ id=7; gọi 404 | IAE, `Invalid Pet identifier!` | `addVisitRejectsUnknownPetId`; lookup guard |
| O24 | toString, output | đủ field Owner | chứa Franklin, Madison, telephone | `toStringContainsKeyFields`; GAP id/new/firstName/address |
| O25 | getPets, initial state | Owner mới | collection rỗng | `getPetsStartsEmpty`; init collection |
| O26 | accessors, state | set address/city/telephone | ba getter đúng giá trị | `getAddressCityTelephoneRoundTrip`; field wiring |
| O27 | Pet accessor, state | set birthDate 2015-02-12 | đúng ngày | `birthDateHelperAcceptsLocalDate`; getter/setter |

## PetValidatorMutationTests — TV3-V01…V09

Fixture hợp lệ: pet mới, name Buddy, type dog, birthDate 2015-02-12.

| ID | Chức năng / kỹ thuật | Input | Expected | Java method / rủi ro |
|---|---|---|---|---|
| V01 | name BVA | `A × 30` | không lỗi `name` | `nameExactlyAtMaxLengthIsAccepted`; `>30` thành `>=30`; GAP 29 và toàn errors |
| V02 | name BVA | `A × 31` | `name/size` | `nameOneOverMaxLengthIsRejectedWithSizeCode`; bỏ size |
| V03 | name EP | `""` | `name/required` | `emptyNameIsRejectedWithRequiredCode`; required code |
| V04 | name EP | `"   "` | `name/required` | `blankNameIsRejectedWithRequiredCode`; GAP chưa assert code |
| V05 | name EP | `null` | `name/required` | `nullNameIsRejectedWithRequiredCode`; GAP chưa assert code/null path |
| V06 | type Decision V-T3 | id=42, type null | không lỗi type | `persistedPetWithoutTypeIsAccepted`; isNew condition |
| V07 | type Decision V-T1 | id null, type null | `type/required` | `newPetWithoutTypeIsRejected`; GAP chưa assert code |
| V08 | birthDate / type | id=42, birthDate null | `birthDate/required`, không type error | `persistedPetWithoutBirthDateIsStillRejected`; GAP code/type assertion |
| V09 | supports EP | `Pet.class`, `String.class` | true, false | `supportsPetAndSubclassesOnly`; GAP subclass Pet |

`isNew && type == null` chỉ báo lỗi type khi cả hai đúng. `birthDate` được kiểm
tra độc lập với isNew. Không có luật source cấm ngày tương lai.

## PetVisitModelMutationTests — TV3-M01…M09

| ID | Chức năng / kỹ thuật | Input | Expected | Java method / rủi ro |
|---|---|---|---|---|
| M01 | Pet.addVisit, deep state | Visit Checkup | collection chứa đúng instance | `petAddVisitStoresVisit`; empty return/add mất |
| M02 | Pet fields, deep state | type cat, date 2020-05-04 | cùng type, đúng date | `petTypeAndBirthDateRoundTrip`; field wiring |
| M03 | Visit constructor / BVA ngày | `new Visit()` | hôm nay + 1 | `visitDefaultsToTomorrow`; GAP clock/năm mới/năm nhuận |
| M04 | Visit field | Annual checkup | đúng description | `visitDescriptionRoundTrip`; getter/setter |
| M05 | Visit field | 2025-03-18 | đúng date | `visitDateRoundTrip`; setter mất |
| M06 | Formatter.print EP | PetType name null | `<null>` | `formatterPrintsNullNameAsPlaceholder`; null-name branch |
| M07 | Formatter.print EP | PetType name Hamster | `Hamster` | `formatterPrintsConfiguredName`; placeholder sai |
| M08 | Formatter.parse EP | repository chứa Dog; parse Dog | cùng instance Dog | `formatterParsesKnownType`; comparison/return |
| M09 | Formatter.parse EP | repository rỗng; parse Fish | `ParseException` | `formatterRejectsUnknownType`; GAP message/offset/non-empty miss |

## Traceability summary

| File | IDs | Methods hiện có | Runtime S06 |
|---|---|---:|---|
| `OwnerMutationTests.java` | O01–O27 | 27 | 27 pass |
| `PetValidatorMutationTests.java` | V01–V09 | 9 | 9 pass |
| `PetVisitModelMutationTests.java` | M01–M09 | 9 | 9 pass |
| Tổng | 45 IDs | 45 | 45 pass |

Không dùng số 45 để suy ra coverage/PIT. S06 thực tế đạt 192/195 mutants và
250/250 line coverage; report PIT và giới hạn snapshot được ghi trong
[TV3_HANDOFF.md](TV3_HANDOFF.md).
