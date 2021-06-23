	<b-modal ref="addFileModal"
		id="file-modal"
		title="Add a new file"
		hide-footer>

		<b-form @submit="onSubmit" @reset="onReset" class="w-100">

			<b-form-group id="form-name-group"
				label="name:"
				label-for="form-name-input">
				<b-form-input id="form-name-input"
						type="file"
						v-model="addFileForm.file"
						required
						placeholder="Enter name">
				</b-form-input>
			</b-form-group>

			<b-button type="submit" variant="primary">Submit</b-button>
			<b-button type="reset" variant="danger">Reset</b-button>
			
		</b-form>

	</b-modal>