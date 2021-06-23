<!-- FROM https://serversideup.net/uploading-files-vuejs-axios/ --> 

<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit file to Flask server</button>
    </div>
  </div>
</template>

<script>

import axios from 'axios';


export default {

	data(){
		return {
			file: ''
		}
	},

	methods: {

		handleFileUpload() {
			this.file = this.$refs.file.files[0];
		},

		submitFile() {

			axios.get('http://localhost:8000/upload_file_from_vue', {

					headers: {
						'Access-Control-Allow-Origin': '*',
					},
					proxy: {
						host: 'localhost',
						port: 8000,
						responseType: 'json',
						data: this.file,
						headers: { 'Content-Type': 'multipart/form-data' }
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

	}

}

</script>