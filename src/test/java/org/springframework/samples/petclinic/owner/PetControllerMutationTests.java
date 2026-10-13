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
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.FilterType;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.test.context.aot.DisabledInAotMode;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.web.servlet.mvc.support.RedirectAttributesModelMap;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.hamcrest.Matchers.hasProperty;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

/**
 * Mutation-killing tests for {@link PetController}.
 *
 * <p>
 * Targets: side-effect assertions on {@code owner.addPet} and the field copies in
 * {@code updatePetDetails} ({@code VoidMethodCallMutator}), the null-birth-date guard,
 * the duplicate-name decision table ({@code RemoveConditionalMutator}), rethrow of
 * unexpected {@link DataIntegrityViolationException}s, the
 * {@code Assert.state(id != null)} guard and the {@code orElseThrow} lambdas.
 */
@WebMvcTest(value = PetController.class,
		includeFilters = @ComponentScan.Filter(value = PetTypeFormatter.class, type = FilterType.ASSIGNABLE_TYPE))
@DisabledInNativeImage
@DisabledInAotMode
class PetControllerMutationTests {

	private static final int TEST_OWNER_ID = 1;

	private static final int TEST_PET_ID = 1;

	@Autowired
	private MockMvc mockMvc;

	@MockitoBean
	private OwnerRepository owners;

	@MockitoBean
	private PetTypeRepository types;

	private PetType hamster;

	@BeforeEach
	void setup() {
		this.hamster = new PetType();
		this.hamster.setId(3);
		this.hamster.setName("hamster");
		given(this.types.findPetTypes()).willReturn(List.of(this.hamster));

		Owner owner = new Owner();
		Pet petty = new Pet();
		Pet doggy = new Pet();
		owner.addPet(petty);
		owner.addPet(doggy);
		petty.setId(TEST_PET_ID);
		doggy.setId(TEST_PET_ID + 1);
		petty.setName("petty");
		doggy.setName("doggy");
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(owner));
	}

	@Test
	void initCreationFormAddsPetToOwnerModel() throws Exception {
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(new Owner()));

		this.mockMvc.perform(get("/owners/{ownerId}/pets/new", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("owner", hasProperty("pets", hasSize(1))));
	}

	@Test
	void initCreationFormExposesConfiguredPetTypes() throws Exception {
		this.mockMvc.perform(get("/owners/{ownerId}/pets/new", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("types", is(List.of(this.hamster))));
	}

	@Test
	void creationWithNullBirthDateShowsRequiredError() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty").param("type", "hamster"))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasFieldErrors("pet", "birthDate"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "birthDate", "required"))
			.andExpect(view().name("pets/createOrUpdatePetForm"));
	}

	@Test
	void creationRethrowsUnexpectedIntegrityViolation() {
		given(this.owners.saveAndFlush(any(Owner.class)))
			.willThrow(new DataIntegrityViolationException("FK constraint fails on owners"));

		assertThatThrownBy(
				() -> this.mockMvc.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty")
					.param("type", "hamster")
					.param("birthDate", "2015-02-12")))
			.hasRootCauseInstanceOf(DataIntegrityViolationException.class);
	}

	@Test
	void creationRethrowsViolationWithNullMessage() {
		given(this.owners.saveAndFlush(any(Owner.class))).willThrow(new DataIntegrityViolationException((String) null));

		assertThatThrownBy(
				() -> this.mockMvc.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty")
					.param("type", "hamster")
					.param("birthDate", "2015-02-12")))
			.hasRootCauseInstanceOf(DataIntegrityViolationException.class);
	}

	@Test
	void creationPersistsNewPetThroughOwner() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty")
				.param("type", "hamster")
				.param("birthDate", "2015-02-12"))
			.andExpect(status().is3xxRedirection());

		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(this.owners).saveAndFlush(captor.capture());
		assertThat(captor.getValue().getPet("Betty")).isNotNull();
	}

	@Test
	void updateWithFutureBirthDateIsRejected() throws Exception {
		String future = LocalDate.now().plusMonths(1).toString();

		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/edit", TEST_OWNER_ID, TEST_PET_ID).param("name", "Betty")
				.param("type", "hamster")
				.param("birthDate", future))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasFieldErrors("pet", "birthDate"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "birthDate", "typeMismatch.birthDate"))
			.andExpect(view().name("pets/createOrUpdatePetForm"));
	}

	@Test
	void updateRethrowsUnexpectedIntegrityViolation() {
		given(this.owners.saveAndFlush(any(Owner.class)))
			.willThrow(new DataIntegrityViolationException("FK constraint fails on owners"));

		assertThatThrownBy(() -> this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/edit", TEST_OWNER_ID, TEST_PET_ID).param("name", "Betty")
				.param("type", "hamster")
				.param("birthDate", "2015-02-12")))
			.hasRootCauseInstanceOf(DataIntegrityViolationException.class);
	}

	@Test
	void updateCopiesEditedFieldsOntoExistingPet() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/edit", TEST_OWNER_ID, TEST_PET_ID).param("name", "Betty")
				.param("type", "hamster")
				.param("birthDate", "2015-02-12"))
			.andExpect(status().is3xxRedirection());

		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(this.owners).saveAndFlush(captor.capture());
		Pet updated = captor.getValue().getPet(TEST_PET_ID);
		assertThat(updated).isNotNull();
		assertThat(updated.getName()).isEqualTo("Betty");
		assertThat(updated.getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12));
		assertThat(updated.getType()).isNotNull();
		assertThat(updated.getType().getName()).isEqualTo("hamster");
	}

	@Test
	void creationDuplicateCheckRespectsIsNew() {
		OwnerRepository repository = mock(OwnerRepository.class);
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet existing = new Pet();
		existing.setId(1);
		existing.setName("petty");
		owner.addPet(existing);
		// detached (already persisted, id != null) pet reusing the same name
		Pet detached = new Pet();
		detached.setId(2);
		detached.setName("petty");
		detached.setType(this.hamster);
		detached.setBirthDate(LocalDate.of(2015, 2, 12));
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(detached, "pet");

		String view = controller.processCreationForm(owner, detached, result, new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		assertThat(result.hasFieldErrors("name")).isFalse();
	}

	@Test
	void creationDuplicateCheckRequiresReadableName() {
		OwnerRepository repository = mock(OwnerRepository.class);
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet blankNamed = new Pet();
		blankNamed.setId(3);
		blankNamed.setName(" ");
		owner.addPet(blankNamed);
		Pet candidate = new Pet();
		candidate.setName(" ");
		candidate.setType(this.hamster);
		candidate.setBirthDate(LocalDate.of(2015, 2, 12));
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(candidate, "pet");

		String view = controller.processCreationForm(owner, candidate, result, new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		assertThat(result.hasFieldErrors("name")).isFalse();
	}

	@Test
	void updateFallsBackToAddForUnknownPetId() {
		OwnerRepository repository = mock(OwnerRepository.class);
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet existing = new Pet();
		existing.setId(1);
		existing.setName("petty");
		owner.addPet(existing);
		Pet detached = new Pet();
		detached.setId(99);
		detached.setName("Newbie");
		detached.setType(this.hamster);
		detached.setBirthDate(LocalDate.of(2015, 2, 12));
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(detached, "pet");

		String view = controller.processUpdateForm(owner, detached, result, new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(repository).saveAndFlush(captor.capture());
		assertThat(captor.getValue().getPet(99)).isNotNull();
	}

	@Test
	void updateCopiesFieldsOntoManagedPet() {
		OwnerRepository repository = mock(OwnerRepository.class);
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet managed = new Pet();
		managed.setId(1);
		managed.setName("petty");
		managed.setBirthDate(LocalDate.of(2010, 1, 1));
		owner.addPet(managed);
		// detached form-backing object: a different instance carrying the same id
		Pet detached = new Pet();
		detached.setId(1);
		detached.setName("Betty");
		detached.setType(this.hamster);
		detached.setBirthDate(LocalDate.of(2015, 2, 12));
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(detached, "pet");

		String view = controller.processUpdateForm(owner, detached, result, new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		assertThat(result.hasErrors()).isFalse();
		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(repository).saveAndFlush(captor.capture());
		Pet updated = captor.getValue().getPet(1);
		assertThat(updated).isNotNull();
		assertThat(updated.getName()).isEqualTo("Betty");
		assertThat(updated.getBirthDate()).isEqualTo(LocalDate.of(2015, 2, 12));
		assertThat(updated.getType()).isNotNull();
		assertThat(updated.getType().getName()).isEqualTo("hamster");
	}

	@Test
	void updateWithBlankNameSkipsDuplicateCheck() {
		OwnerRepository repository = mock(OwnerRepository.class);
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet edited = new Pet();
		edited.setId(1);
		edited.setName("petty");
		owner.addPet(edited);
		Pet blankNamed = new Pet();
		blankNamed.setId(3);
		blankNamed.setName(" ");
		owner.addPet(blankNamed);
		Pet detached = new Pet();
		detached.setId(1);
		detached.setName(" ");
		detached.setType(this.hamster);
		detached.setBirthDate(LocalDate.of(2015, 2, 12));
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(detached, "pet");

		String view = controller.processUpdateForm(owner, detached, result, new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		assertThat(result.hasFieldErrors("name")).isFalse();
	}

	@Test
	void updateWithNullPetIdFailsFast() {
		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
		Owner owner = new Owner();
		Pet detached = new Pet();
		detached.setName("Betty");
		detached.setType(this.hamster);
		detached.setBirthDate(LocalDate.of(2015, 2, 12));

		assertThatThrownBy(() -> controller.processUpdateForm(owner, detached,
				new BeanPropertyBindingResult(detached, "pet"), new RedirectAttributesModelMap()))
			.isInstanceOf(IllegalStateException.class)
			.hasMessageContaining("'pet.getId()' must not be null");
	}

	@Test
	void creationWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/new", 999)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	@Test
	void editWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/edit", 999, TEST_PET_ID)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	@Test
	void editFormOwnerVanishingOnSecondLookupThrowsIllegalArgument() {
		// findOwner (@ModelAttribute) succeeds on the first repository call while
		// findPet fails on the second one, covering the orElseThrow lambda
		Owner owner = new Owner();
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(owner), Optional.empty());

		assertThatThrownBy(
				() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/edit", TEST_OWNER_ID, TEST_PET_ID)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: " + TEST_OWNER_ID);
	}

	@Test
	void findPetWithUnknownOwnerThrowsIllegalArgument() {
		// direct invocation: deterministic execution of the orElseThrow lambda
		// in findPet regardless of @ModelAttribute ordering
		OwnerRepository repository = mock(OwnerRepository.class);
		given(repository.findById(999)).willReturn(Optional.empty());
		PetController controller = new PetController(repository, mock(PetTypeRepository.class));

		assertThatThrownBy(() -> controller.findPet(999, TEST_PET_ID)).isInstanceOf(IllegalArgumentException.class)
			.hasMessageContaining("Owner not found with id: 999");
	}

}
