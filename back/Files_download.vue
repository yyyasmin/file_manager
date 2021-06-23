<!-- FROM https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/ -->


<template>
  <div class="container">

    <div class="row">
      <div class="col-sm-10">
        <h1>Files</h1>
        <hr><br><br>
<button type="button" class="btn btn-success btn-sm" v-b-modal.file-modal>Add File</button>        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">File name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(File, index) in Files" :key="index">
              <td>{{ File }}</td>
              <td>
                <span v-if="File.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

        
    <b-modal ref="addFileModal"
            id="file-modal"
            title="Add a new file"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addFileForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addFileForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addFileForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

  </div>
</template>


<script>

  import axios from 'axios';

  export default {
  data() {
      return {
      Files: [],   // SHOUD IT BE REPLACE WITH Files_download ? 
      };
  },

    methods: {
        getFiles() {

            // FROM https://github.com/axios/axios/issues/853
            // TO SOLVE CORS PROBLEN

            axios.get('http://localhost:8000/files_download', {

                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
                proxy: {
                    host: 'localhost',
                    port: 8000,
                    // data: filename,   # FILE TO DOWNLOAD
                    responseType: 'json'
                }
                }).then( (response)  => {

                      console.log('PRINTING response:', response.data.FILES)
                      this.Files = response.data.FILES;

                }).catch(function (error) {
                    if (error.response) {
                        console.log(error.response.headers);
                    } 
                    else if (error.request) {
                        console.log(error.request);
                    } 
                    else {
                    console.log(error.message);
                    }
                console.log(error.config);
            });

        },

        addFile(payload) {
          const path = 'http://localhost:5000/files';
          axios.post(path, payload)
          .then(() => {
            this.getFiles();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getFiles();
          });
        },
        initForm() {
          this.addFileForm.title = '';
          this.addFileForm.author = '';
          this.addFileForm.read = [];
        },
        onSubmit(evt) {
          evt.preventDefault();
          this.$refs.addFileModal.hide();
          let read = false;
          if (this.addFileForm.read[0]) read = true;
          const payload = {
          title: this.addFileForm.title,
          author: this.addFileForm.author,
          read, // property shorthand
          };
          this.addFile(payload);
          this.initForm();
        },
        onReset(evt) {
          evt.preventDefault();
          this.$refs.addFileModal.hide();
          this.initForm();
        },
  	},
    created() {
    this.getFiles();
    }
};


</script>