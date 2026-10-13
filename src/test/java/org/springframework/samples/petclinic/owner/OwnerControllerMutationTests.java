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

import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.test.context.aot.DisabledInAotMode;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.web.servlet.mvc.support.RedirectAttributesModelMap;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

/**
 * Mutation-killing tests for {@link OwnerController}.
 *
 * <p>
 * Targets: {@code MathMutator} on the zero-based page index, the
 * {@code lastName.isEmpty()} branch of the out-of-bounds redirect, the
 * {@code orElseThrow} lambdas (unknown owner) and the id-mismatch {@code rejectValue}
 * call.
 */
@WebMvcTest(OwnerController.class)
@DisabledInNativeImage
@DisabledInAotMode
class OwnerControllerMutationTests {

	private static final int TEST_OWNER_ID = 1;

	@Autowired
	private MockMvc mockMvc;

	@MockitoBean
	private OwnerRepository owners;

	private Owner george() {
		Owner george = new Owner();
		george.setId(TEST_OWNER_ID);
		george.setFirstName("George");
		george.setLastName("Franklin");
		george.setAddress("110 W. Liberty St.");
		george.setCity("Madison");
		george.setTelephone("6085551023");
		return george;
	}

	@BeforeEach
	void setup() {
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(george()));
		given(this.owners.findByLastNameStartingWith(eq("Franklin"), any(Pageable.class)))
			.willReturn(new PageImpl<>(List.of(george())));
	}

	@Test
	void processFindFormRequestsZeroBasedPageIndex() throws Exception {
		Page<Owner> page = new PageImpl<>(List.of(george()), PageRequest.of(1, 5), 12);
		given(this.owners.findByLastNameStartingWith(eq(""), any(Pageable.class))).willReturn(page);

		this.mockMvc.perform(get("/owners").param("page", "2"))
			.andExpect(status().isOk())
			.andExpect(view().name("owners/ownersList"));

		ArgumentCaptor<Pageable> captor = ArgumentCaptor.forClass(Pageable.class);
		verify(this.owners).findByLastNameStartingWith(eq(""), captor.capture());
		assertThat(captor.getValue().getPageNumber()).isEqualTo(1);
		assertThat(captor.getValue().getPageSize()).isEqualTo(5);
	}

	@Test
	void outOfBoundsPageWithEmptyLastNameOmitsLastNameParam() throws Exception {
		given(this.owners.findByLastNameStartingWith(eq(""), any(Pageable.class)))
			.willReturn(new PageImpl<>(List.of()));

		this.mockMvc.perform(get("/owners").param("page", "99"))
			.andExpect(status().is3xxRedirection())
			.andExpect(redirectedUrl("/owners?page=1"));
	}

	@Test
	void editFormWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}/edit", 999)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	@Test
	void showOwnerWithUnknownIdThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}", 999)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	@Test
	void showOwnerFailingOnSecondLookupThrowsIllegalArgument() {
		// the @ModelAttribute findOwner succeeds on the first repository call
		// while showOwner itself fails on the second one, covering its
		// orElseThrow lambda
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(george()), Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}", TEST_OWNER_ID)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: " + TEST_OWNER_ID);
	}

	@Test
	void processUpdateOwnerFormMismatchRecordsIdFieldError() {
		OwnerRepository repository = mock(OwnerRepository.class);
		OwnerController controller = new OwnerController(repository);
		Owner owner = george();
		owner.setId(2);
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(owner, "owner");
		RedirectAttributesModelMap redirectAttributes = new RedirectAttributesModelMap();

		String view = controller.processUpdateOwnerForm(owner, result, 1, redirectAttributes);

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}/edit");
		assertThat(result.hasFieldErrors("id")).isTrue();
		assertThat(result.getFieldError("id")).isNotNull();
		assertThat(result.getFieldError("id").getCode()).isEqualTo("mismatch");
		verify(repository, never()).save(any(Owner.class));
	}

}
