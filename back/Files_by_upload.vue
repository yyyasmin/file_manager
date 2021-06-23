
<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Files</h1>
        <hr><br><br>

        <input class="file" name="file" type="file" @change="send_to_flask"/>

        <label for="file" class="label"></label>

        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">File name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(File, index) in Files" :key="index">
              <td>{{ File.name }}</td>
              <td>
                <div class="btn-group" role="group">

                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeletefile(File)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      Files: [],
    };
  },

  methods: {
        getFiles() {

            // FROM https://github.com/axios/axios/issues/853
            // TO SOLVE CORS PROBLEN

            axios.get('http://localhost:5000/files_by_upload', {

                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
                proxy: {
                    host: 'localhost',
                    port: 5000,
                    responseType: 'json'
                }
                }).then( (response)  => {

                      // console.log('PRINTING response:', response.data.FILES)
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

        removeFile(fileID) {

          let param = new FormData(); //Create form object
          param.set('id', fileID);//Add data to the form object through append
          console.log('In RRR removeFile: --- param.get-id ---', param.get('id')); //FormData private class object, can not be accessed, you can judge whether the value is passed in through get

          axios({
            method: "post",
            url: "http://localhost:5000/del_file",
            data: {
              id: fileID
            },
            processData: false, contentType: false ,
            headers: {
                'Access-Control-Allow-Origin': '*',
            },
              proxy: {
                  host: 'localhost',
                  port: 5000,
                  responseType: 'json',
              },
            })
            .then(() => {
              console.log("RETURNED SUCCESSFULLY FROM DELETE FILE DDD")
                this.getFiles();
                this.message = 'file deleted!';
            })
            .catch((error) => {
              console.log("RETURNED ERROR FROM DELETE FILE DDD")
              // eslint-disable-next-line
              console.log(error);
              this.getFiles();
          });
        },

      onDeletefile(File) {
        console.log("IN onDeletefile FILE file-id", File.id)
        this.removeFile(File.id);
      },

      //FROM FROM https://www.programmersought.com/article/15116850767/

      send_to_flask(e) {

        let file = e.target.files[0];
        let param = new FormData(); //Create form object
        param.append('file', file);//Add data to the form object through append
        console.log('In Update: --- param.get-fle ---', param.get('file')); //FormData private class object, can not be accessed, you can judge whether the value is passed in through get

        axios({
          method: "post",
          url: "http://localhost:5000/add_file",
          data: param,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'multipart/form-data',
            },
            proxy: {
                host: 'localhost',
                port: 5000,
                responseType: 'json',
            },
          })
          .then(() => {
              this.getFiles();
              this.message = 'file uploaded!';
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getFiles();
          });
      },

    initForm() {
    },
	
  },
  created() {
    this.getFiles();
  },

};

</script>