# TV3 handoff — Domain/Validator black-box tests

## Snapshot and scope

Handoff prepared in S07 on 19/10/2026 for branch `TranMinhTai/Session5`,
HEAD `589a5057a75f37d476bc95268b0e04f1e0ff62c1`. TV3 scope is limited to:

- `OwnerMutationTests`, `PetValidatorMutationTests`, and
  `PetVisitModelMutationTests`;
- test design and TV3-only documentation under `docs/tv3/`;
- environment/onboarding guidance and evidence interpretation.

TV3 did not change production code, `pom.xml`, CI, controller tests owned by
TV4, common report E.2, database configuration, or `target/` artifacts.

## Actual repository state

| Item | State |
|---|---|
| Three assigned test files | present, 27 + 9 + 9 = 45 methods |
| E.1 design and method mapping | present in `DESIGN_TABLES.md` and `TEST_DESIGN_TV3.md` |
| Windows onboarding / Part C draft | present in `ONBOARDING_WINDOWS.md` and `REPORT_C_TV3_DRAFT.md` |
| S03 commit `80d23de` | not an ancestor of current HEAD |
| S04 commit `41c65b0` | not an ancestor of current HEAD |
| Assigned branch `test/domain-validator-mutation` | absent locally and on `origin`; not created or checked out |

The code snapshot therefore lacks the planned S03/S04 refinements: a dedicated
29-character validation assertion, all required-code/type assertions, a Pet
subclass assertion, and deterministic default-date cases across year/leap-year
boundaries. They are recorded as GAPs, not represented as completed code.

## S06 validation evidence — executed, not historical

Executed on 19/10/2026, UTC+07, with Temurin 21.0.12.1, Maven Wrapper 3.9.16,
Spring Boot 4.1.0, Java target 17, PIT 1.30.0. Source reports are overwritten
build artifacts and must not be staged.

| Command | Time | Exit | Result | Evidence |
|---|---|---:|---|---|
| `mvnw.cmd test -Dtest=OwnerMutationTests,PetValidatorMutationTests,PetVisitModelMutationTests` | 04:20:41–04:20:55 | 0 | 45 run, 45 pass, 0 F/E/S | `target/surefire-reports/TEST-*.xml` |
| `mvnw.cmd test -Dtest=org.springframework.samples.petclinic.owner.**` | 04:20:57–04:21:20 | 0 | 130 run, 130 pass, 0 F/E/S | `target/surefire-reports/TEST-*.xml` |
| `mvnw.cmd test -Dtest=!*IntegrationTests -DfailIfNoTests=false` | 04:21:22–04:21:53 | 0 | 153 run, 153 pass, 0 F/E/S | `target/surefire-reports/TEST-*.xml` |
| `mvnw.cmd test-compile org.pitest:pitest-maven:mutationCoverage -Djacoco.skip=true` | 04:21:59–04:23:42 | 0 | 195 generated; 192 killed; 3 survived; 0 no coverage | `target/pit-reports/mutations.xml`, `target/pit-reports/index.html` |

PIT reports line coverage 250/250 (100%) and mutation 192/195 (98%), satisfying
POM gates of mutation >=88% and line >=95%. `27 tests examined` is a PIT metric,
not the 45-test TV3 suite or 130-test owner suite. The filtered 153-test command
excludes every class ending in `IntegrationTests`, including two classes that do
not require Docker; it is not an all-tests claim.

The three survivors remain `Owner.java:108` twice (indexes 39, 42) and
`OwnerController.java:167` (index 50). Their equivalent-mutant explanation from
handover is only a source-semantics hypothesis; the reported score remains 98%.

## Documentation reconciliation

| Document | Reconciled status |
|---|---|
| `REPORT_C_TV3_DRAFT.md` | S05 observations remain historical-to-S05; S06 values above are actual rerun evidence |
| `ONBOARDING_WINDOWS.md` | command instructions remain valid; it must not claim a clean-machine or HTTP demo was performed |
| `DESIGN_TABLES.md` | source-based EP/BVA/Decision Table, including 29/30/31 and explicit GAPs |
| `TEST_DESIGN_TV3.md` | 45 IDs map one-to-one to current Java methods and expected behavior |

## Ownership, blockers, and coordination

| Owner | Required follow-up | Status |
|---|---|---|
| TV3 / integrator | choose and integrate S03/S04 changes, then rerun S06 | waiting; no automatic branch switch/merge performed |
| TV1 | provide/confirm integration branch and resolve any future POM/CI failure | no current POM/CI blocker |
| TV2 | coordinate any live HTTP port 8090 demonstration | not run or claimed by TV3 |
| TV4 | own controller-specific test changes | no controller defect assigned from S06 |

## Review questions for the defence

1. Why is 30 accepted and 31 rejected? The predicate is `length() > 30`; 30
   distinguishes it from a `>= 30` boundary mutation, while 29 validates the
   lower adjacent valid partition.
2. Why can a persisted pet omit type? Type validation is exactly
   `pet.isNew() && pet.getType() == null`; birth date remains independently
   required.
3. Why is O04 separate from duplicate persisted-ID testing? Two transient pets
   share null IDs but are allowed when distinct; only the same instance is
   rejected by `contains`.
4. What makes M01/M02/M08 deep assertions? They verify collection content,
   identity, and exact field values rather than merely non-null results.

## Git plan — user action required

Do not stage `target/`, `REPORT_R01_K03.md`, `pom.xml`, or TV4/TV1 files. After
reviewing the intended diff, use the following commands only if the files and
their content are approved:

```powershell
git status --short
git diff --check
git add -- src/test/java/org/springframework/samples/petclinic/owner/OwnerMutationTests.java
git add -- src/test/java/org/springframework/samples/petclinic/owner/PetValidatorMutationTests.java
git add -- src/test/java/org/springframework/samples/petclinic/owner/PetVisitModelMutationTests.java
git add -- docs/tv3/ONBOARDING_WINDOWS.md docs/tv3/REPORT_C_TV3_DRAFT.md docs/tv3/DESIGN_TABLES.md docs/tv3/TEST_DESIGN_TV3.md docs/tv3/TV3_HANDOFF.md
git diff --cached --check
git diff --cached --name-only
```

No `git add`, commit, push, PR, branch creation, checkout, merge, or GitHub
Actions claim was performed in S07.

## Suggested message to the team lead

> TV3 handoff is ready for review on snapshot `589a505`: 45 TV3 tests pass,
> owner package 130/130, filtered suite 153/153, PIT 192/195 (98%) and line
> coverage 250/250. E.1 design/mapping and onboarding evidence are in
> `docs/tv3/`. Please confirm the integration branch for S03/S04 refinements;
> those commits are not ancestors of the current branch. No commit, PR, HTTP
> demo, or CI result is being claimed.
