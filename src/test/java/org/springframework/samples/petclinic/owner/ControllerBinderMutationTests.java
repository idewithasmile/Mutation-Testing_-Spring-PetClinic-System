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
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.bind.WebDataBinder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

/**
 * Mutation-killing tests for {@code @InitBinder} setup methods and
 * {@link VisitController#minVisitDate()}.
 *
 * <p>
 * Each binder test uses {@code verify(...)} so that {@code VoidMethodCallMutator} applied
 * to {@code setDisallowedFields} is killed; the {@code minVisitDate} test kills the
 * {@code NullReturnValsMutator} on that method.
 */
@ExtendWith(MockitoExtension.class)
@DisabledInNativeImage
class ControllerBinderMutationTests {

	@Test
	void ownerControllerDisallowsIdBinding() {
		OwnerRepository owners = mock(OwnerRepository.class);
		WebDataBinder binder = mock(WebDataBinder.class);

		new OwnerController(owners).setAllowedFields(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	@Test
	void visitControllerDisallowsIdBinding() {
		OwnerRepository owners = mock(OwnerRepository.class);
		WebDataBinder binder = mock(WebDataBinder.class);

		new VisitController(owners).setAllowedFields(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	@Test
	void petControllerOwnerBinderDisallowsIdBinding() {
		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
		WebDataBinder binder = mock(WebDataBinder.class);

		controller.initOwnerBinder(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	@Test
	void petControllerPetBinderDisallowsIdBinding() {
		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
		WebDataBinder binder = mock(WebDataBinder.class);

		controller.initPetBinder(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	@Test
	void minVisitDateIsTomorrow() {
		VisitController controller = new VisitController(mock(OwnerRepository.class));

		assertThat(controller.minVisitDate()).isEqualTo(LocalDate.now().plusDays(1));
	}

}
