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

	/**
	 * Kỹ thuật: Error Guessing / Mockito Verify Đường đi/Nhánh: BP-OC-01 (Dòng 60–62
	 * trong OwnerController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 61 (xóa
	 * dataBinder.setDisallowedFields) Ý đồ: Dùng verify(binder) để đảm bảo lời gọi cấm
	 * bind "id" và "*.id" được thực thi, ngăn chặn lỗ hổng Mass Assignment và diệt
	 * VoidMethodCallMutator.
	 */
	@Test
	void ownerControllerDisallowsIdBinding() {
		OwnerRepository owners = mock(OwnerRepository.class);
		WebDataBinder binder = mock(WebDataBinder.class);

		new OwnerController(owners).setAllowedFields(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	/**
	 * Kỹ thuật: Error Guessing / Mockito Verify Đường đi/Nhánh: BP-VC-01 (Dòng 52–54
	 * trong VisitController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 53 (xóa
	 * dataBinder.setDisallowedFields) Ý đồ: Dùng verify(binder) để đảm bảo
	 * VisitController cấm ghi đè ID thực thể, diệt VoidMethodCallMutator trên lệnh
	 * setDisallowedFields.
	 */
	@Test
	void visitControllerDisallowsIdBinding() {
		OwnerRepository owners = mock(OwnerRepository.class);
		WebDataBinder binder = mock(WebDataBinder.class);

		new VisitController(owners).setAllowedFields(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	/**
	 * Kỹ thuật: Error Guessing / Mockito Verify Đường đi/Nhánh: BP-PC-01 (Dòng 90–92
	 * trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 91 (xóa
	 * dataBinder.setDisallowedFields) Ý đồ: Kiểm tra @InitBinder("owner") thiết lập cấm
	 * bind trường "id", diệt VoidMethodCallMutator nếu phương thức bị làm rỗng.
	 */
	@Test
	void petControllerOwnerBinderDisallowsIdBinding() {
		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
		WebDataBinder binder = mock(WebDataBinder.class);

		controller.initOwnerBinder(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	/**
	 * Kỹ thuật: Error Guessing / Mockito Verify Đường đi/Nhánh: BP-PC-02 (Dòng 95–98
	 * trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 97 (xóa
	 * dataBinder.setDisallowedFields) Ý đồ: Kiểm tra @InitBinder("pet") thiết lập cấm
	 * bind trường "id", diệt VoidMethodCallMutator tại dòng cấu hình disallowed fields.
	 */
	@Test
	void petControllerPetBinderDisallowsIdBinding() {
		PetController controller = new PetController(mock(OwnerRepository.class), mock(PetTypeRepository.class));
		WebDataBinder binder = mock(WebDataBinder.class);

		controller.initPetBinder(binder);

		verify(binder).setDisallowedFields("id", "*.id");
	}

	/**
	 * Kỹ thuật: Boundary Value Analysis / State Assertion Đường đi/Nhánh: BP-VC-02 (Dòng
	 * 84–86 trong VisitController.java) Mutant mục tiêu: NullReturnValsMutator dòng 85
	 * (thay thế return bằng null) Ý đồ: Khẳng định ngày tối thiểu đặt lịch luôn là ngày
	 * mai (LocalDate.now().plusDays(1)), diệt NullReturnValsMutator và đảm bảo tính toàn
	 * vẹn của model attribute minVisitDate.
	 */
	@Test
	void minVisitDateIsTomorrow() {
		VisitController controller = new VisitController(mock(OwnerRepository.class));

		assertThat(controller.minVisitDate()).isEqualTo(LocalDate.now().plusDays(1));
	}

}
