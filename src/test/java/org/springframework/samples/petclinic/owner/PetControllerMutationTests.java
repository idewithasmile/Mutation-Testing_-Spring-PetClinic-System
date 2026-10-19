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

	/**
	 * Kỹ thuật: State / Model Assertion Đường đi/Nhánh: BP-PC-04 (Dòng 101–105 trong
	 * PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 103 (xóa
	 * owner.addPet(pet)) Ý đồ: Kiểm tra thuộc tính model "owner" có chứa danh sách thú
	 * cưng gồm 1 pet mới khởi tạo, diệt VoidMethodCallMutator khi lời gọi addPet bị loại
	 * bỏ.
	 */
	/**
	 * Kỹ thuật: State / Model Assertion Đường đi/Nhánh: BP-PC-04 (Dòng 101–105 trong
	 * PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 103 (xóa
	 * owner.addPet(pet)) Ý đồ: Kiểm tra thuộc tính model "owner" có chứa danh sách thú
	 * cưng gồm 1 pet mới khởi tạo, diệt VoidMethodCallMutator khi lời gọi addPet bị loại
	 * bỏ.
	 */
	@Test
	void initCreationFormAddsPetToOwnerModel() throws Exception {
		given(this.owners.findById(TEST_OWNER_ID)).willReturn(Optional.of(new Owner()));

		this.mockMvc.perform(get("/owners/{ownerId}/pets/new", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("owner", hasProperty("pets", hasSize(1))));
	}

	/**
	 * Kỹ thuật: State / Model Assertion Đường đi/Nhánh: BP-PC-03 (Dòng 63–65 trong
	 * PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 64
	 * (populatePetTypes trả về null) Ý đồ: Xác nhận model "types" nhận đúng danh sách
	 * PetType từ repository, diệt NullReturnValsMutator và EmptyObjectReturnValsMutator.
	 */
	/**
	 * Kỹ thuật: State / Model Assertion Đường đi/Nhánh: BP-PC-03 (Dòng 63–65 trong
	 * PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 64
	 * (populatePetTypes trả về null) Ý đồ: Xác nhận model "types" nhận đúng danh sách
	 * PetType từ repository, diệt NullReturnValsMutator và EmptyObjectReturnValsMutator.
	 */
	@Test
	void initCreationFormExposesConfiguredPetTypes() throws Exception {
		this.mockMvc.perform(get("/owners/{ownerId}/pets/new", TEST_OWNER_ID))
			.andExpect(status().isOk())
			.andExpect(model().attribute("types", is(List.of(this.hamster))));
	}

	/**
	 * Kỹ thuật: Basis Path / Error Guessing Đường đi/Nhánh: BP-PC-10, BP-PC-12 (Dòng 116,
	 * 120 trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE
	 * dòng 120 (bỏ qua result.hasErrors) Ý đồ: Gửi form thiếu trường bắt buộc birthDate
	 * để kích hoạt validation error, kiểm tra controller giữ lại view form và không gọi
	 * lưu DB.
	 */
	/**
	 * Kỹ thuật: Basis Path / Error Guessing Đường đi/Nhánh: BP-PC-10, BP-PC-12 (Dòng 116,
	 * 120 trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE
	 * dòng 120 (bỏ qua result.hasErrors) Ý đồ: Gửi form thiếu trường bắt buộc birthDate
	 * để kích hoạt validation error, kiểm tra controller giữ lại view form và không gọi
	 * lưu DB.
	 */
	@Test
	void creationWithNullBirthDateShowsRequiredError() throws Exception {
		this.mockMvc
			.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty").param("type", "hamster"))
			.andExpect(status().isOk())
			.andExpect(model().attributeHasFieldErrors("pet", "birthDate"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "birthDate", "required"))
			.andExpect(view().name("pets/createOrUpdatePetForm"));
	}

	/**
	 * Kỹ thuật: Error Guessing / Exception Rethrow Đường đi/Nhánh: BP-PC-13 (Dòng 128–131
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_IF dòng
	 * 129 (thay !isDuplicate bằng false) Ý đồ: Khi DB ném lỗi ngoại lệ toàn vẹn không
	 * phải trùng tên (FK fail), controller phải ném tiếp ngoại lệ (rethrow) chứ không
	 * được nuốt lỗi hoặc chuyển về form sai bản chất.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Exception Rethrow Đường đi/Nhánh: BP-PC-13 (Dòng 128–131
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_IF dòng
	 * 129 (thay !isDuplicate bằng false) Ý đồ: Khi DB ném lỗi ngoại lệ toàn vẹn không
	 * phải trùng tên (FK fail), controller phải ném tiếp ngoại lệ (rethrow) chứ không
	 * được nuốt lỗi hoặc chuyển về form sai bản chất.
	 */
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

	/**
	 * Kỹ thuật: Error Guessing / Null-Check Đường đi/Nhánh: BP-PC-14, BP-PC-26 (Dòng
	 * 128–131, 203–204 trong PetController.java) Mutant mục tiêu:
	 * RemoveConditionalMutator_EQUAL_ELSE dòng 204 (thay message != null bằng false) Ý
	 * đồ: Bảo vệ khỏi NullPointerException khi ngoại lệ có getMessage() là null, đảm bảo
	 * nhánh kiểm tra null hoạt động chính xác và rethrow ngoại lệ an toàn.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Null-Check Đường đi/Nhánh: BP-PC-14, BP-PC-26 (Dòng
	 * 128–131, 203–204 trong PetController.java) Mutant mục tiêu:
	 * RemoveConditionalMutator_EQUAL_ELSE dòng 204 (thay message != null bằng false) Ý
	 * đồ: Bảo vệ khỏi NullPointerException khi ngoại lệ có getMessage() là null, đảm bảo
	 * nhánh kiểm tra null hoạt động chính xác và rethrow ngoại lệ an toàn.
	 */
	@Test
	void creationRethrowsViolationWithNullMessage() {
		given(this.owners.saveAndFlush(any(Owner.class))).willThrow(new DataIntegrityViolationException((String) null));

		assertThatThrownBy(
				() -> this.mockMvc.perform(post("/owners/{ownerId}/pets/new", TEST_OWNER_ID).param("name", "Betty")
					.param("type", "hamster")
					.param("birthDate", "2015-02-12")))
			.hasRootCauseInstanceOf(DataIntegrityViolationException.class);
	}

	/**
	 * Kỹ thuật: Basis Path / ArgumentCaptor Đường đi/Nhánh: BP-PC-16 (Dòng 124–127,
	 * 135–136 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 125,
	 * 126 (xóa owner.addPet hoặc saveAndFlush) Ý đồ: Dùng ArgumentCaptor bắt đối tượng
	 * Owner được saveAndFlush để khẳng định pet mới ("Betty") đã được thêm vào owner
	 * thành công, diệt VoidMethodCallMutator.
	 */
	/**
	 * Kỹ thuật: Basis Path / ArgumentCaptor Đường đi/Nhánh: BP-PC-16 (Dòng 124–127,
	 * 135–136 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 125,
	 * 126 (xóa owner.addPet hoặc saveAndFlush) Ý đồ: Dùng ArgumentCaptor bắt đối tượng
	 * Owner được saveAndFlush để khẳng định pet mới ("Betty") đã được thêm vào owner
	 * thành công, diệt VoidMethodCallMutator.
	 */
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

	/**
	 * Kỹ thuật: Boundary Value / Basis Path Đường đi/Nhánh: BP-PC-19 (Dòng 159–161 trong
	 * PetController.java) Mutant mục tiêu: ConditionalsBoundaryMutator và
	 * RemoveConditionalMutator_EQUAL_IF dòng 159 Ý đồ: Truyền ngày sinh trong tương lai
	 * (plusMonths(1)) để kiểm tra nhánh rẽ rejectValue birthDate, diệt các mutant đổi
	 * ranh giới isAfter hoặc xóa điều kiện kiểm tra ngày.
	 */
	/**
	 * Kỹ thuật: Boundary Value / Basis Path Đường đi/Nhánh: BP-PC-19 (Dòng 159–161 trong
	 * PetController.java) Mutant mục tiêu: ConditionalsBoundaryMutator và
	 * RemoveConditionalMutator_EQUAL_IF dòng 159 Ý đồ: Truyền ngày sinh trong tương lai
	 * (plusMonths(1)) để kiểm tra nhánh rẽ rejectValue birthDate, diệt các mutant đổi
	 * ranh giới isAfter hoặc xóa điều kiện kiểm tra ngày.
	 */
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

	/**
	 * Kỹ thuật: Error Guessing / Exception Rethrow Đường đi/Nhánh: BP-PC-20 (Dòng 170–173
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_IF dòng
	 * 171 (bỏ qua rethrow ex) Ý đồ: Đảm bảo trong quá trình update, mọi
	 * DataIntegrityViolationException không phải do trùng tên pet đều được rethrow ngay
	 * lập tức, ngăn ngừa lỗi che giấu sự cố hệ thống.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Exception Rethrow Đường đi/Nhánh: BP-PC-20 (Dòng 170–173
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_IF dòng
	 * 171 (bỏ qua rethrow ex) Ý đồ: Đảm bảo trong quá trình update, mọi
	 * DataIntegrityViolationException không phải do trùng tên pet đều được rethrow ngay
	 * lập tức, ngăn ngừa lỗi che giấu sự cố hệ thống.
	 */
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

	/**
	 * Kỹ thuật: State Assertion / MockMvc Đường đi/Nhánh: BP-PC-21, BP-PC-24 (Dòng
	 * 189–195 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 192,
	 * 193, 194 (xóa setName, setBirthDate, setType) Ý đồ: Thao tác qua MockMvc POST edit
	 * form và dùng ArgumentCaptor kiểm tra từng trường dữ liệu của entity trong
	 * repository đã được sao chép giá trị mới, diệt triệt để VoidMethodCallMutator.
	 */
	/**
	 * Kỹ thuật: State Assertion / MockMvc Đường đi/Nhánh: BP-PC-21, BP-PC-24 (Dòng
	 * 189–195 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 192,
	 * 193, 194 (xóa setName, setBirthDate, setType) Ý đồ: Thao tác qua MockMvc POST edit
	 * form và dùng ArgumentCaptor kiểm tra từng trường dữ liệu của entity trong
	 * repository đã được sao chép giá trị mới, diệt triệt để VoidMethodCallMutator.
	 */
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

	/**
	 * Kỹ thuật: Basis Path / Decision Table Đường đi/Nhánh: BP-PC-08 (Dòng 111 trong
	 * PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 111
	 * (thay pet.isNew() bằng true) Ý đồ: Khi một detached pet có id != null (isNew() ==
	 * false) trùng tên với pet đã có, controller không được báo lỗi duplicate, diệt
	 * mutant xóa điều kiện kiểm tra isNew().
	 */
	/**
	 * Kỹ thuật: Basis Path / Decision Table Đường đi/Nhánh: BP-PC-08 (Dòng 111 trong
	 * PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 111
	 * (thay pet.isNew() bằng true) Ý đồ: Khi một detached pet có id != null (isNew() ==
	 * false) trùng tên với pet đã có, controller không được báo lỗi duplicate, diệt
	 * mutant xóa điều kiện kiểm tra isNew().
	 */
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

	/**
	 * Kỹ thuật: Basis Path / Decision Table Đường đi/Nhánh: BP-PC-09 (Dòng 111 trong
	 * PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 111
	 * (thay hasText(name) bằng true) Ý đồ: Tên pet chứa toàn khoảng trắng (" ") làm
	 * StringUtils.hasText() trả về false, bỏ qua kiểm tra trùng tên và bàn giao cho
	 * validation framework, diệt RemoveConditionalMutator.
	 */
	/**
	 * Kỹ thuật: Basis Path / Decision Table Đường đi/Nhánh: BP-PC-09 (Dòng 111 trong
	 * PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng 111
	 * (thay hasText(name) bằng true) Ý đồ: Tên pet chứa toàn khoảng trắng (" ") làm
	 * StringUtils.hasText() trả về false, bỏ qua kiểm tra trùng tên và bàn giao cho
	 * validation framework, diệt RemoveConditionalMutator.
	 */
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

	/**
	 * Kỹ thuật: Basis Path / Fallback Branch Đường đi/Nhánh: BP-PC-22, BP-PC-25 (Dòng
	 * 190, 196–198 trong PetController.java) Mutant mục tiêu:
	 * RemoveConditionalMutator_EQUAL_IF dòng 190 (thay existingPet != null bằng true) Ý
	 * đồ: Khi pet ID không khớp với bất kỳ pet hiện có nào của owner (existingPet ==
	 * null), controller rơi vào nhánh else gọi owner.addPet(pet), diệt
	 * RemoveConditionalMutator.
	 */
	/**
	 * Kỹ thuật: Basis Path / Fallback Branch Đường đi/Nhánh: BP-PC-22, BP-PC-25 (Dòng
	 * 190, 196–198 trong PetController.java) Mutant mục tiêu:
	 * RemoveConditionalMutator_EQUAL_IF dòng 190 (thay existingPet != null bằng true) Ý
	 * đồ: Khi pet ID không khớp với bất kỳ pet hiện có nào của owner (existingPet ==
	 * null), controller rơi vào nhánh else gọi owner.addPet(pet), diệt
	 * RemoveConditionalMutator.
	 */
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

	/**
	 * Kỹ thuật: State Assertion / Direct Method Call Đường đi/Nhánh: BP-PC-21, BP-PC-24
	 * (Dòng 189–195 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng
	 * 192, 193, 194 (xóa setName, setBirthDate, setType) Ý đồ: Gọi trực tiếp
	 * processUpdateForm với detached entity và managed entity có cùng ID nhưng khác nội
	 * dung ("Betty" vs "petty"), assert đối tượng lưu trong repo mang dữ liệu mới của
	 * detached pet.
	 */
	/**
	 * Kỹ thuật: State Assertion / Direct Method Call Đường đi/Nhánh: BP-PC-21, BP-PC-24
	 * (Dòng 189–195 trong PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng
	 * 192, 193, 194 (xóa setName, setBirthDate, setType) Ý đồ: Gọi trực tiếp
	 * processUpdateForm với detached entity và managed entity có cùng ID nhưng khác nội
	 * dung ("Betty" vs "petty"), assert đối tượng lưu trong repo mang dữ liệu mới của
	 * detached pet.
	 */
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

	/**
	 * Kỹ thuật: Basis Path / Short-Circuit Evaluation Đường đi/Nhánh: BP-PC-18 (Dòng 151
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng
	 * 151 (thay hasText bằng true) Ý đồ: Khi tên pet rỗng (" "), biểu thức if
	 * (StringUtils.hasText(petName)) đoản mạch ngay, không tra cứu duplicate trong owner,
	 * diệt RemoveConditionalMutator.
	 */
	/**
	 * Kỹ thuật: Basis Path / Short-Circuit Evaluation Đường đi/Nhánh: BP-PC-18 (Dòng 151
	 * trong PetController.java) Mutant mục tiêu: RemoveConditionalMutator_EQUAL_ELSE dòng
	 * 151 (thay hasText bằng true) Ý đồ: Khi tên pet rỗng (" "), biểu thức if
	 * (StringUtils.hasText(petName)) đoản mạch ngay, không tra cứu duplicate trong owner,
	 * diệt RemoveConditionalMutator.
	 */
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

	/**
	 * Kỹ thuật: Error Guessing / Fail-Fast Guard Đường đi/Nhánh: BP-PC-23 (Dòng 188 trong
	 * PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 188 (xóa
	 * Assert.state(id != null, ...)) Ý đồ: Kiểm tra Assert.state ném
	 * IllegalStateException ngay khi pet.getId() == null trong updatePetDetails, ngăn
	 * chặn cập nhật thực thể vô danh và diệt VoidMethodCallMutator.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Fail-Fast Guard Đường đi/Nhánh: BP-PC-23 (Dòng 188 trong
	 * PetController.java) Mutant mục tiêu: VoidMethodCallMutator dòng 188 (xóa
	 * Assert.state(id != null, ...)) Ý đồ: Kiểm tra Assert.state ném
	 * IllegalStateException ngay khi pet.getId() == null trong updatePetDetails, ngăn
	 * chặn cập nhật thực thể vô danh và diệt VoidMethodCallMutator.
	 */
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

	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-PC-05 (Dòng 68–72
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 70
	 * (orElseThrow lambda cho findOwner) Ý đồ: Truy cập form tạo pet với ownerId=999
	 * không tồn tại, kiểm tra IllegalArgumentException được ném ra với message chính xác,
	 * diệt NullReturnValsMutator.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-PC-05 (Dòng 68–72
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 70
	 * (orElseThrow lambda cho findOwner) Ý đồ: Truy cập form tạo pet với ownerId=999
	 * không tồn tại, kiểm tra IllegalArgumentException được ném ra với message chính xác,
	 * diệt NullReturnValsMutator.
	 */
	@Test
	void creationWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/new", 999)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-PC-05 (Dòng 68–72
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 70
	 * (orElseThrow lambda cho findOwner) Ý đồ: Truy cập form sửa pet với ownerId=999
	 * không tồn tại, kiểm tra IllegalArgumentException được ném ra từ @ModelAttribute
	 * findOwner, diệt NullReturnValsMutator.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Exception Testing Đường đi/Nhánh: BP-PC-05 (Dòng 68–72
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 70
	 * (orElseThrow lambda cho findOwner) Ý đồ: Truy cập form sửa pet với ownerId=999
	 * không tồn tại, kiểm tra IllegalArgumentException được ném ra từ @ModelAttribute
	 * findOwner, diệt NullReturnValsMutator.
	 */
	@Test
	void editWithUnknownOwnerThrowsIllegalArgument() {
		given(this.owners.findById(999)).willReturn(Optional.empty());

		assertThatThrownBy(() -> this.mockMvc.perform(get("/owners/{ownerId}/pets/{petId}/edit", 999, TEST_PET_ID)))
			.hasRootCauseInstanceOf(IllegalArgumentException.class)
			.hasStackTraceContaining("Owner not found with id: 999");
	}

	/**
	 * Kỹ thuật: Basis Path / Mock Sequence Đường đi/Nhánh: BP-PC-06 (Dòng 83–86 trong
	 * PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 84 (orElseThrow
	 * lambda trong findPet) Ý đồ: Mô phỏng lần nạp findOwner thành công nhưng lần gọi
	 * findPet lại thấy owner biến mất, cô lập và diệt chính xác nhánh orElseThrow trong
	 * phương thức findPet.
	 */
	/**
	 * Kỹ thuật: Basis Path / Mock Sequence Đường đi/Nhánh: BP-PC-06 (Dòng 83–86 trong
	 * PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 84 (orElseThrow
	 * lambda trong findPet) Ý đồ: Mô phỏng lần nạp findOwner thành công nhưng lần gọi
	 * findPet lại thấy owner biến mất, cô lập và diệt chính xác nhánh orElseThrow trong
	 * phương thức findPet.
	 */
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

	/**
	 * Kỹ thuật: Error Guessing / Direct Method Call Đường đi/Nhánh: BP-PC-06 (Dòng 83–86
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 84
	 * (orElseThrow lambda trong findPet) Ý đồ: Gọi trực tiếp controller.findPet(999,
	 * petId) độc lập với vòng đời Spring MVC, kiểm chứng deterministic nhánh ném
	 * IllegalArgumentException khi không tìm thấy owner.
	 */
	/**
	 * Kỹ thuật: Error Guessing / Direct Method Call Đường đi/Nhánh: BP-PC-06 (Dòng 83–86
	 * trong PetController.java) Mutant mục tiêu: NullReturnValsMutator dòng 84
	 * (orElseThrow lambda trong findPet) Ý đồ: Gọi trực tiếp controller.findPet(999,
	 * petId) độc lập với vòng đời Spring MVC, kiểm chứng deterministic nhánh ném
	 * IllegalArgumentException khi không tìm thấy owner.
	 */
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
