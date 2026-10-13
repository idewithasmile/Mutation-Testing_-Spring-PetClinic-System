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

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * Mutation-killing tests for {@link Owner}.
 *
 * <p>
 * Designed with decision-table coverage over {@code addPet}, both {@code getPet}
 * overloads and {@code addVisit} so that PIT operators {@code RemoveConditionalMutator}
 * (both branches) and {@code VoidMethodCallMutator} (side-effect assertions) are killed.
 */
@DisabledInNativeImage
class OwnerMutationTests {

	private Pet persistedPet(Integer id, String name) {
		Pet pet = new Pet();
		pet.setId(id);
		pet.setName(name);
		return pet;
	}

	private Pet newPet(String name) {
		Pet pet = new Pet();
		pet.setName(name);
		return pet;
	}

	@Test
	void addPetIgnoresNull() {
		Owner owner = new Owner();

		owner.addPet(null);

		assertThat(owner.getPets()).isEmpty();
	}

	@Test
	void addPetAddsNewPet() {
		Owner owner = new Owner();
		Pet pet = newPet("Buddy");

		owner.addPet(pet);

		assertThat(owner.getPets()).containsExactly(pet);
	}

	@Test
	void addPetRejectsSameInstanceTwice() {
		Owner owner = new Owner();
		Pet pet = persistedPet(5, "Buddy");

		owner.addPet(pet);
		owner.addPet(pet);

		assertThat(owner.getPets()).hasSize(1);
	}

	@Test
	void addPetRejectsSameNewInstanceTwice() {
		// a new (transient) pet is caught by the contains() guard while the
		// id-equality loop below cannot fire (both ids are null)
		Owner owner = new Owner();
		Pet pet = newPet("Buddy");

		owner.addPet(pet);
		owner.addPet(pet);

		assertThat(owner.getPets()).hasSize(1);
	}

	@Test
	void addPetRejectsDifferentInstanceWithSameId() {
		Owner owner = new Owner();
		Pet first = persistedPet(5, "Buddy");
		Pet second = persistedPet(5, "Max");

		owner.addPet(first);
		owner.addPet(second);

		assertThat(owner.getPets()).containsExactly(first);
	}

	@Test
	void addPetAllowsDifferentIds() {
		Owner owner = new Owner();

		owner.addPet(persistedPet(5, "Buddy"));
		owner.addPet(persistedPet(6, "Max"));

		assertThat(owner.getPets()).hasSize(2);
	}

	@Test
	void addPetAllowsTwoNewPets() {
		Owner owner = new Owner();

		owner.addPet(newPet("Buddy"));
		owner.addPet(newPet("Max"));

		assertThat(owner.getPets()).hasSize(2);
	}

	@Test
	void addPetAllowsNewPetAlongsidePersistedPet() {
		Owner owner = new Owner();

		owner.addPet(persistedPet(5, "Buddy"));
		owner.addPet(newPet("Max"));

		assertThat(owner.getPets()).hasSize(2);
	}

	@Test
	void addPetAllowsPersistedPetAfterNewPet() {
		Owner owner = new Owner();

		owner.addPet(newPet("Max"));
		owner.addPet(persistedPet(5, "Buddy"));

		assertThat(owner.getPets()).hasSize(2);
	}

	@Test
	void getPetByIdReturnsMatchingPet() {
		Owner owner = new Owner();
		Pet buddy = persistedPet(5, "Buddy");
		owner.addPet(buddy);
		owner.addPet(persistedPet(6, "Max"));

		assertThat(owner.getPet(5)).isSameAs(buddy);
	}

	@Test
	void getPetByIdReturnsNullWhenAbsent() {
		Owner owner = new Owner();
		owner.addPet(persistedPet(5, "Buddy"));

		assertThat(owner.getPet(42)).isNull();
	}

	@Test
	void getPetByIdSkipsNewPets() {
		Owner owner = new Owner();
		owner.addPet(newPet("Buddy"));

		assertThat(owner.getPet(5)).isNull();
	}

	@Test
	void getPetByIdWithNullIdReturnsNull() {
		Owner owner = new Owner();
		owner.addPet(newPet("Buddy"));
		owner.addPet(persistedPet(5, "Max"));

		assertThat(owner.getPet((Integer) null)).isNull();
	}

	@Test
	void getPetByNameIsCaseInsensitive() {
		Owner owner = new Owner();
		Pet buddy = persistedPet(5, "Buddy");
		owner.addPet(buddy);

		assertThat(owner.getPet("buddy")).isSameAs(buddy);
		assertThat(owner.getPet("BUDDY")).isSameAs(buddy);
	}

	@Test
	void getPetByNameReturnsNullWhenAbsent() {
		Owner owner = new Owner();
		owner.addPet(persistedPet(5, "Buddy"));

		assertThat(owner.getPet("Max")).isNull();
	}

	@Test
	void getPetByNameSkipsPetsWithNullName() {
		Owner owner = new Owner();
		Pet nameless = new Pet();
		nameless.setId(7);
		owner.addPet(nameless);
		Pet buddy = persistedPet(5, "Buddy");
		owner.addPet(buddy);

		assertThat(owner.getPet("Buddy")).isSameAs(buddy);
		assertThat(owner.getPet("anything")).isNull();
	}

	@Test
	void getPetByNameWithIgnoreNewSkipsNewPet() {
		Owner owner = new Owner();
		owner.addPet(newPet("Rex"));

		assertThat(owner.getPet("Rex", true)).isNull();
	}

	@Test
	void getPetByNameWithIgnoreNewReturnsPersistedPet() {
		Owner owner = new Owner();
		Pet rex = persistedPet(8, "Rex");
		owner.addPet(rex);

		assertThat(owner.getPet("Rex", true)).isSameAs(rex);
	}

	@Test
	void getPetByNameWithoutIgnoreNewReturnsNewPet() {
		Owner owner = new Owner();
		Pet rex = newPet("Rex");
		owner.addPet(rex);

		assertThat(owner.getPet("Rex", false)).isSameAs(rex);
		assertThat(owner.getPet("Rex")).isSameAs(rex);
	}

	@Test
	void addVisitDelegatesToPet() {
		Owner owner = new Owner();
		Pet pet = persistedPet(7, "Buddy");
		owner.addPet(pet);
		Visit visit = new Visit();
		visit.setDescription("Annual checkup");

		owner.addVisit(7, visit);

		assertThat(pet.getVisits()).containsExactly(visit);
	}

	@Test
	void addVisitRejectsNullPetId() {
		Owner owner = new Owner();

		assertThatThrownBy(() -> owner.addVisit(null, new Visit())).isInstanceOf(IllegalArgumentException.class)
			.hasMessage("Pet identifier must not be null!");
	}

	@Test
	void addVisitRejectsNullVisit() {
		Owner owner = new Owner();
		owner.addPet(persistedPet(7, "Buddy"));

		assertThatThrownBy(() -> owner.addVisit(7, null)).isInstanceOf(IllegalArgumentException.class)
			.hasMessage("Visit must not be null!");
	}

	@Test
	void addVisitRejectsUnknownPetId() {
		Owner owner = new Owner();
		owner.addPet(persistedPet(7, "Buddy"));

		assertThatThrownBy(() -> owner.addVisit(404, new Visit())).isInstanceOf(IllegalArgumentException.class)
			.hasMessage("Invalid Pet identifier!");
	}

	@Test
	void toStringContainsKeyFields() {
		Owner owner = new Owner();
		owner.setId(1);
		owner.setFirstName("George");
		owner.setLastName("Franklin");
		owner.setAddress("110 W. Liberty St.");
		owner.setCity("Madison");
		owner.setTelephone("6085551023");

		assertThat(owner.toString()).contains("Franklin").contains("Madison").contains("6085551023");
	}

	@Test
	void getPetsStartsEmpty() {
		assertThat(new Owner().getPets()).isEmpty();
	}

	@Test
	void getAddressCityTelephoneRoundTrip() {
		Owner owner = new Owner();
		owner.setAddress("123 Caramel Street");
		owner.setCity("London");
		owner.setTelephone("1316761638");

		assertThat(owner.getAddress()).isEqualTo("123 Caramel Street");
		assertThat(owner.getCity()).isEqualTo("London");
		assertThat(owner.getTelephone()).isEqualTo("1316761638");
	}

	@Test
	void birthDateHelperAcceptsLocalDate() {
		// guards Pet birth-date accessors used by validator/controller flows
		Pet pet = newPet("Buddy");
		pet.setBirthDate(LocalDate.of(2015, 2, 12));

		assertThat(pet.getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12));
	}

}
