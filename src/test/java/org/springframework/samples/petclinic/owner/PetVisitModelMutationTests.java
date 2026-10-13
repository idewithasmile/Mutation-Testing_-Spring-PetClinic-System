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

import java.text.ParseException;
import java.time.LocalDate;
import java.util.List;
import java.util.Locale;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.BDDMockito.given;

/**
 * Mutation-killing tests for the simple model classes {@link Pet}, {@link Visit} and
 * {@link PetTypeFormatter}.
 *
 * <p>
 * Targets {@code EmptyObjectReturnValsMutator} (strict value assertions instead of
 * emptiness checks) and the null-name branch of {@link PetTypeFormatter#print}.
 */
@ExtendWith(MockitoExtension.class)
@DisabledInNativeImage
class PetVisitModelMutationTests {

	@Mock
	private PetTypeRepository types;

	private PetTypeFormatter formatter;

	@BeforeEach
	void setUp() {
		this.formatter = new PetTypeFormatter(types);
	}

	@Test
	void petAddVisitStoresVisit() {
		Pet pet = new Pet();
		Visit visit = new Visit();
		visit.setDescription("Checkup");

		pet.addVisit(visit);

		assertThat(pet.getVisits()).containsExactly(visit);
	}

	@Test
	void petTypeAndBirthDateRoundTrip() {
		Pet pet = new Pet();
		PetType type = new PetType();
		type.setName("cat");
		pet.setType(type);
		pet.setBirthDate(LocalDate.of(2020, 5, 4));

		assertThat(pet.getType()).isSameAs(type);
		assertThat(pet.getBirthDate()).isEqualTo(LocalDate.of(2020, 5, 4));
	}

	@Test
	void visitDefaultsToTomorrow() {
		assertThat(new Visit().getDate()).isEqualTo(LocalDate.now().plusDays(1));
	}

	@Test
	void visitDescriptionRoundTrip() {
		Visit visit = new Visit();
		visit.setDescription("Annual checkup");

		assertThat(visit.getDescription()).isEqualTo("Annual checkup");
	}

	@Test
	void visitDateRoundTrip() {
		Visit visit = new Visit();
		visit.setDate(LocalDate.of(2025, 3, 18));

		assertThat(visit.getDate()).isEqualTo(LocalDate.of(2025, 3, 18));
	}

	@Test
	void formatterPrintsNullNameAsPlaceholder() {
		PetType type = new PetType();

		assertThat(this.formatter.print(type, Locale.ENGLISH)).isEqualTo("<null>");
	}

	@Test
	void formatterPrintsConfiguredName() {
		PetType type = new PetType();
		type.setName("Hamster");

		assertThat(this.formatter.print(type, Locale.ENGLISH)).isEqualTo("Hamster");
	}

	@Test
	void formatterParsesKnownType() throws ParseException {
		PetType dog = new PetType();
		dog.setName("Dog");
		given(this.types.findPetTypes()).willReturn(List.of(dog));

		assertThat(this.formatter.parse("Dog", Locale.ENGLISH)).isSameAs(dog);
	}

	@Test
	void formatterRejectsUnknownType() {
		given(this.types.findPetTypes()).willReturn(List.of());

		assertThatThrownBy(() -> this.formatter.parse("Fish", Locale.ENGLISH)).isInstanceOf(ParseException.class);
	}

}
