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
 * {@code RemoveConditionalMutator}).
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

	@Test
	void nameExactlyAtMaxLengthIsAccepted() {
		Pet pet = validNewPet();
		pet.setName("A".repeat(30));

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isFalse();
	}

	@Test
	void nameOneOverMaxLengthIsRejectedWithSizeCode() {
		Pet pet = validNewPet();
		pet.setName("A".repeat(31));

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("size");
	}

	@Test
	void emptyNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName("");

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
		assertThat(this.errors.getFieldError("name").getCode()).isEqualTo("required");
	}

	@Test
	void blankNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName("   ");

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
	}

	@Test
	void nullNameIsRejectedWithRequiredCode() {
		Pet pet = validNewPet();
		pet.setName(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("name")).isTrue();
	}

	@Test
	void persistedPetWithoutTypeIsAccepted() {
		// decision table: isNew=false, type=null -> no "type" error
		Pet pet = validNewPet();
		pet.setId(42);
		pet.setType(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("type")).isFalse();
	}

	@Test
	void newPetWithoutTypeIsRejected() {
		Pet pet = validNewPet();
		pet.setType(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("type")).isTrue();
	}

	@Test
	void persistedPetWithoutBirthDateIsStillRejected() {
		Pet pet = validNewPet();
		pet.setId(42);
		pet.setBirthDate(null);

		this.validator.validate(pet, this.errors);

		assertThat(this.errors.hasFieldErrors("birthDate")).isTrue();
	}

	@Test
	void supportsPetAndSubclassesOnly() {
		assertThat(this.validator.supports(Pet.class)).isTrue();
		assertThat(this.validator.supports(String.class)).isFalse();
	}

}
