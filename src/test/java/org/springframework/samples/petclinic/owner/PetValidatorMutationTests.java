/*
 * Copyright 2012-2025 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.springframework.samples.petclinic.owner;

import java.time.LocalDate;
import java.util.HashMap;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.springframework.validation.Errors;
import org.springframework.validation.MapBindingResult;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Mutation-killing tests for {@link PetValidator}.
 *
 * <p>
 * Applies Boundary Value Analysis on {@code MAX_NAME_LENGTH = 30} (targets
 * {@code ConditionalsBoundaryMutator} on {@code name.length() > 30}) and a decision table
 * over {@code pet.isNew() && pet.getType() == null} (targets
 * {@code RemoveConditionalMutator}). Test-case IDs map to
 * {@code docs/tv3/TEST_DESIGN_TV3.md}; decision-table rows are in
 * {@code docs/tv3/DESIGN_TABLES.md}.
 */
@DisabledInNativeImage
class PetValidatorMutationTests {

	private PetValidator validator;

	private Errors errors;

	@BeforeEach
	void setUp() {
		this.validator = new PetValidator();
		this.errors = new MapBindingResult(new HashMap<>(), "pet");
	}

	private Pet validNewPet() {
		PetType type = new PetType();
		type.setName("dog");
		Pet pet = new Pet();
		pet.setName("Buddy");
		pet.setType(type);
		pet.setBirthDate(LocalDate.of(2015, 2, 12));
		return pet;
	}

	/**
	 * TV3-V01 - BVA, V-T2: valid new pets with names of length 29 or 30 have no
	 * validation errors. Length 30 targets a boundary change from > to >=.
	 */
	@Test
	void nameExactlyAtMaxLengthIsAccepted() {
		for (int length : new int[] { 29, 30 }) {
			Pet pet = validNewPet();
			pet.setName("A".repeat(length));
			Errors caseErrors = new MapBindingResult(new HashMap<>(), "pet");

			this.validator.validate(pet, caseErrors);

			assertThat(caseErrors.hasErrors()).as("valid new pet with name length %s", length).isFalse();
		}
	}

	/**
	 * TV3-V02 - BVA: a name of length 31 produces a name error with the size code.
	 */
	@Test
	void nameOneOverMaxLengthIsRejectedWithSizeCode() {
		Pet pet = validNewPet();
		pet.setName("A".repeat(31));

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("size");
	}

	/**
	 * TV3-V03 - EP: an empty name produces a name error with the required code.
	 */
	@Test
	void emptyNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName("");

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("required");
	}

	/**
	 * TV3-V04 - EP: a whitespace-only name produces a name/required error.
	 */
	@Test
	void blankNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName("   ");

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("required");
	}

	/**
	 * TV3-V05 - EP: a null name produces a name/required error without dereferencing the
	 * name.
	 */
	@Test
	void nullNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("required");
	}

	/**
	 * TV3-V06 - Decision Table V-T3: a persisted pet may omit its type.
	 */
	@Test
	void persistedPetWithoutTypeIsAccepted() {
		// decision table: isNew=false, type=null -> no "type" error
		Pet pet = validNewPet();
		pet.setId(42);
		pet.setType(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("type")).isFalse();
	}

	/**
	 * TV3-V07 - Decision Table V-T1: a new pet without a type produces type/required.
	 */
	@Test
	void newPetWithoutTypeIsRejected() {
		Pet pet = validNewPet();
		pet.setType(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("type")).isTrue();
		assertThat(this.errors.getFieldError("type").getCode()).isEqualTo("required");
	}

	/**
	 * TV3-V08 - EP, V-T4: a persisted typed pet still requires a birth date; the
	 * birthDate/required error must not imply a type error.
	 */
	@Test
	void persistedPetWithoutBirthDateIsStillRejected() {
		Pet pet = validNewPet();
		pet.setId(42);
		pet.setBirthDate(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("birthDate")).isTrue();
		assertThat(this.errors.getFieldError("birthDate").getCode()).isEqualTo("required");
		assertThat(this.errors.hasFieldErrors("type")).isFalse();
	}

	/**
	 * TV3-V09 - EP: Pet and its subclasses are supported; unrelated classes are not.
	 */
	@Test
	void supportsPetAndSubclassesOnly() {
		assertThat(this.validator.supports(Pet.class)).isTrue();
		assertThat(this.validator.supports(SpecialPet.class)).isTrue();
		assertThat(this.validator.supports(String.class)).isFalse();
	}

	private static class SpecialPet extends Pet {

	}

}
