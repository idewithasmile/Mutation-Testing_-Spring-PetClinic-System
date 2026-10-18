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
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.CALLS_REAL_METHODS;
import static org.mockito.Mockito.mockStatic;

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

	/**
	 * TV3-M01 - State assertion: the visit collection contains the exact stored visit.
	 */
	@Test
	void petAddVisitStoresVisit() {
		Pet pet = new Pet();
		Visit visit = new Visit();
		visit.setDescription("Checkup");

		pet.addVisit(visit);

		assertThat(pet.getVisits()).containsExactly(visit);
	}

	/**
	 * TV3-M02 - State assertion: type identity and the fixed birth date are preserved.
	 */
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

	/**
	 * TV3-M03 - Date BVA: tomorrow is correct for an ordinary day, year end and the day
	 * before leap day, independently of the system date.
	 */
	@Test
	void visitDefaultsToTomorrow() {
		LocalDate[][] dateCases = { { LocalDate.of(2026, 10, 18), LocalDate.of(2026, 10, 19) },
				{ LocalDate.of(2026, 12, 31), LocalDate.of(2027, 1, 1) },
				{ LocalDate.of(2024, 2, 28), LocalDate.of(2024, 2, 29) } };

		for (LocalDate[] dateCase : dateCases) {
			// Fix only now(); keep real date arithmetic and close the mock per case.
			try (MockedStatic<LocalDate> dates = mockStatic(LocalDate.class, CALLS_REAL_METHODS)) {
				dates.when(LocalDate::now).thenReturn(dateCase[0]);

				assertThat(new Visit().getDate()).as("default visit date after %s", dateCase[0]).isEqualTo(dateCase[1]);
			}
		}
	}

	/**
	 * TV3-M04 - State assertion: the assigned description is returned unchanged.
	 */
	@Test
	void visitDescriptionRoundTrip() {
		Visit visit = new Visit();
		visit.setDescription("Annual checkup");

		assertThat(visit.getDescription()).isEqualTo("Annual checkup");
	}

	/**
	 * TV3-M05 - State assertion: an assigned date replaces the default visit date.
	 */
	@Test
	void visitDateRoundTrip() {
		Visit visit = new Visit();
		visit.setDate(LocalDate.of(2025, 3, 18));

		assertThat(visit.getDate()).isEqualTo(LocalDate.of(2025, 3, 18));
	}

	/**
	 * TV3-M06 - EP, F1: a non-null type with a null name prints the placeholder.
	 */
	@Test
	void formatterPrintsNullNameAsPlaceholder() {
		PetType type = new PetType();

		assertThat(this.formatter.print(type, Locale.ENGLISH)).isEqualTo("<null>");
	}

	/**
	 * TV3-M07 - EP, F2: a configured type name is printed unchanged.
	 */
	@Test
	void formatterPrintsConfiguredName() {
		PetType type = new PetType();
		type.setName("Hamster");

		assertThat(this.formatter.print(type, Locale.ENGLISH)).isEqualTo("Hamster");
	}

	/**
	 * TV3-M08 - EP, F3: a known name resolves to the exact repository object.
	 */
	@Test
	void formatterParsesKnownType() throws ParseException {
		PetType dog = new PetType();
		dog.setName("Dog");
		given(this.types.findPetTypes()).willReturn(List.of(dog));

		assertThat(this.formatter.parse("Dog", Locale.ENGLISH)).isSameAs(dog);
	}

	/**
	 * TV3-M09 - EP, F4: an unknown name produces the expected parse error and offset.
	 */
	@Test
	void formatterRejectsUnknownType() {
		given(this.types.findPetTypes()).willReturn(List.of());

		assertThatThrownBy(() -> this.formatter.parse("Fish", Locale.ENGLISH))
			.isInstanceOfSatisfying(ParseException.class, exception -> {
				assertThat(exception).hasMessage("type not found: Fish");
				assertThat(exception.getErrorOffset()).isZero();
			});
	}

}
