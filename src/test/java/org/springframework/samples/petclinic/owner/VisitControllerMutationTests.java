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
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledInNativeImage;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.aot.DisabledInAotMode;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.web.servlet.mvc.support.RedirectAttributesModelMap;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.hamcrest.Matchers.hasProperty;
import static org.hamcrest.Matchers.hasSize;
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
 * Mutation-killing tests for {@link VisitController}.
 *
 * <p>
 * Targets: the {@code pet == null} guard and the {@code pet.addVisit(visit)} side effect
 * in {@code loadPetWithVisit}, the null-date guard in {@code processNewVisitForm},
 * delegation through {@code owner.addVisit(petId, visit)} and the {@code orElseThrow}
 * lambda for unknown owners.
 */
@WebMvcTest(VisitController.class)
@DisabledInNativeImage
@DisabledInAotMode
class VisitControllerMutationTests {

	private static final int TEST_OWNER_ID = 1;

	private static final int TEST_PET_ID = 1;

	@Autowired
	private MockMvc mockMvc;

	@MockitoBean
	private OwnerRepository owners;

	@BeforeEach
	void init() {
		Owner owner = new Owner();
		Pet pet = new Pet();
		owner.addPet(pet);
		pet.setId(TEST_PET_ID);
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(owner));
	}

	/**
	 * Kỹ thuật: Basis Path / Model Assertion Đường đi/Nhánh: BP-VC-05 (Dòng 76–81 trong
	 * VisitController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 80 (xóa
	 * pet.addVisit(visit)) Ý đồ: Kiểm tra đối tượng pet đưa vào model đã được gắn sẵn
	 * thực thể visit mới khởi tạo (size=1), diệt VoidMethodCallMutator khi lời gọi
	 * addVisit bị loại bỏ.
	 */
	/**
	 * Kỹ thuật: Basis Path / Model Assertion Đường đi/Nhánh: BP-VC-05 (Dòng 76–81 trong
	 * VisitController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 80 (xóa
	 * pet.addVisit(visit)) Ý đồ: Kiểm tra đối tượng pet đưa vào model đã được gắn sẵn
	 * thực thể visit mới khởi tạo (size=1), diệt VoidMethodCallMutator khi lời gọi
	 * addVisit bị loại bỏ.
	 */
	@Test
	void newVisitFormExposesPetWithPendingVisit() throws Exception {
		this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/visits/new", TEST_OWNER_ID, TEST_PET_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("pet", hasProperty("visits", hasSize(1))));
	}

	/**
	 * Kỹ thuật: Error Guessing / Null Guard Đường đi/Nhánh: BP-VC-04 (Dòng 71–74 trong
	 * VisitController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 71
	 * (thay pet == null bằng false) Ý đồ: Kiểm tra nhánh guard pet == null ném
	 * IllegalArgumentException khi truy cập petId=99 không thuộc về ownerId=1, diệt
	 * RemoveConditionalMutator.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Null Guard Đường đi/Nhánh: BP-VC-04 (Dòng 71–74 trong
	 * VisitController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 71
	 * (thay pet == null bằng false) Ý đồ: Kiểm tra nhánh guard pet == null ném
	 * IllegalArgumentException khi truy cập petId=99 không thuộc về ownerId=1, diệt
	 * RemoveConditionalMutator.
	 */
	@Test
	void newVisitFormWithUnknownPetThrowsIllegalArgument() {
		assertThatThrownBy(
				() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/visits/new", TEST_OWNER_ID, 99)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Pet with id 99 not found for owner with id 1");
	}

	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-VC-03 (Dòng 66–69
	 * trong VisitController.java) Mutant mục tiêu: NullReturnValsMutator dòng 68
	 * (orElseThrow lambda cho owners.findById) Ý đồ: Xác nhận khi URL chứa ownerId=999
	 * không tồn tại, phương thức loadPetWithVisit ném IllegalArgumentException với thông
	 * điệp rõ ràng, diệt NullReturnValsMutator.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-VC-03 (Dòng 66–69
	 * trong VisitController.java) Mutant mục tiêu: NullReturnValsMutator dòng 68
	 * (orElseThrow lambda cho owners.findById) Ý đồ: Xác nhận khi URL chứa ownerId=999
	 * không tồn tại, phương thức loadPetWithVisit ném IllegalArgumentException với thông
	 * điệp rõ ràng, diệt NullReturnValsMutator.
	 */
	@Test
	void newVisitFormWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(
				() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/visits/new", 999, TEST_PET_ID)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	/**
	 * Kỹ thuật: Basis Path / ArgumentCaptor Đường đi/Nhánh: BP-VC-08 (Dòng 108–112 trong
	 * VisitController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 108, 109 (xóa
	 * owner.addVisit hoặc save) Ý đồ: Dùng ArgumentCaptor kiểm tra owner được save có
	 * chứa đúng visit mới với ngày hợp lệ và mô tả "Annual checkup", diệt
	 * VoidMethodCallMutator và verify side effect lưu DB.
	 */
	/**
	 * Kỹ thuật: Basis Path / ArgumentCaptor Đường đi/Nhánh: BP-VC-08 (Dòng 108–112 trong
	 * VisitController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 108, 109 (xóa
	 * owner.addVisit hoặc save) Ý đồ: Dùng ArgumentCaptor kiểm tra owner được save có
	 * chứa đúng visit mới với ngày hợp lệ và mô tả "Annual checkup", diệt
	 * VoidMethodCallMutator và verify side effect lưu DB.
	 */
	@Test
	void bookingPersistsVisitThroughOwner() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/visits/new", TEST_OWNER_ID, TEST_PET_ID)
				.param("date", LocalDate.now().plusDays(1).toString())
				.param("description", "Annual checkup"))
			.andExpect(status().is3xxRedirection());

		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(this.owners).save(captor.capture());
		Pet pet = captor.getValue().getPet(TEST_PET_ID);
		assertThat(pet).isNotNull();
		assertThat(pet.getVisits()).hasSize(1);
		assertThat(pet.getVisits().iterator().next().getDescription()).isEqualTo("Annual checkup");
	}

	/**
	 * Kỹ thuật: Basis Path / Null Guard Đường đi/Nhánh: BP-VC-07 (Dòng 100 trong
	 * VisitController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 100
	 * (thay date != null bằng false) Ý đồ: Gọi trực tiếp processNewVisitForm với
	 * visit.getDate() = null để kiểm chứng null-guard tránh NPE tại
	 * visit.getDate().isAfter(), đảm bảo đặt lịch thành công khi ngày để trống.
	 */
	/**
	 * Kỹ thuật: Basis Path / Null Guard Đường đi/Nhánh: BP-VC-07 (Dòng 100 trong
	 * VisitController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 100
	 * (thay date != null bằng false) Ý đồ: Gọi trực tiếp processNewVisitForm với
	 * visit.getDate() = null để kiểm chứng null-guard tránh NPE tại
	 * visit.getDate().isAfter(), đảm bảo đặt lịch thành công khi ngày để trống.
	 */
	@Test
	void processNewVisitFormWithNullDateBooksSuccessfully() {
		OwnerRepository repository = mock(OwnerRepository.class);
		VisitController controller = new VisitController(repository);
		Owner owner = new Owner();
		Pet pet = new Pet();
		pet.setId(TEST_PET_ID);
		owner.addPet(pet);
		Visit visit = new Visit();
		visit.setDate(null);
		visit.setDescription("Annual checkup");
		BeanPropertyBindingResult result = new BeanPropertyBindingResult(visit, "visit");

		String view = controller.processNewVisitForm(owner, TEST_PET_ID, visit, result,
				new RedirectAttributesModelMap());

		assertThat(view).isEqualTo("redirect:/owners/{ownerId}");
		assertThat(result.hasErrors()).isFalse();
		ArgumentCaptor<Owner> captor = ArgumentCaptor.forClass(Owner.class);
		verify(repository).save(captor.capture());
		assertThat(captor.getValue().getPet(TEST_PET_ID).getVisits()).contains(visit);
	}

	/**
	 * Kỹ thuật: Boundary Value / Basis Path Đường đi/Nhánh: BP-VC-06 (Dòng 100–103,
	 * 105–106 trong VisitController.java) Mutant mục tiêu: ConditionalsBoundaryMutator và
	 * RemoveConditionalMutator_EQUAL_IF dòng 100 Ý đồ: Đặt ngày khám là ngày hiện tại
	 * (LocalDate.now()), khẳng định nhánh ranh giới !isAfter(now) kích hoạt rejectValue
	 * "typeMismatch.visitDate" và trả về form, diệt ConditionalsBoundaryMutator.
	 */
	/**
	 * Kỹ thuật: Boundary Value / Basis Path Đường đi/Nhánh: BP-VC-06 (Dòng 100–103,
	 * 105–106 trong VisitController.java) Mutant mục tiêu: ConditionalsBoundaryMutator và
	 * RemoveConditionalMutator_EQUAL_IF dòng 100 Ý đồ: Đặt ngày khám là ngày hiện tại
	 * (LocalDate.now()), khẳng định nhánh ranh giới !isAfter(now) kích hoạt rejectValue
	 * "typeMismatch.visitDate" và trả về form, diệt ConditionalsBoundaryMutator.
	 */
	@Test
	void todayVisitDateIsRejected() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/visits/new", TEST_OWNER_ID, TEST_PET_ID)
				.param("date", LocalDate.now().toString())
				.param("description", "Annual checkup"))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasFieldErrors("visit", "date"))
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

}
