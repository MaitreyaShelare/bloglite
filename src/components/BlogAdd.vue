<template>
  <div class="blogadd">
    <div class="container">
      <div class="card col col-md-6 mx-auto mt-2 mb-5">
        <textarea
          class="form-control border-200 rounded border-0 flex-1 fs-0"
          rows="3"
          placeholder="What do you want to talk about?"
          v-model="blogtext"
          id="blog-text"
        ></textarea>
        <div class="card-footer p-2">
          <div class="d-flex justify-content-between align-items-center">
            <form>
              <div class="form-group" id="image">
                <span class="btn btn-file">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    class="bi bi-card-image"
                    viewBox="0 0 16 16"
                  >
                    <path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z" />
                    <path
                      d="M1.5 2A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-13zm13 1a.5.5 0 0 1 .5.5v6l-3.775-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12v.54A.505.505 0 0 1 1 12.5v-9a.5.5 0 0 1 .5-.5h13z"
                    />
                  </svg>
                  <input
                    type="file"
                    accept="image/*"
                    @change="previewImage"
                    id="blog-image"
                  />
                </span>
              </div>
            </form>
            <div class="d-grid col-2 align-items-center">
              <button
                class="btn btn-primary btn-sm rounded-pill mx-2"
                type="submit"
                @click="PostBlog"
              >
                Post
              </button>
            </div>
          </div>
        </div>
        <div pt-2 mt-3 v-if="preview">
          <!-- <div v-for="(item, index) in preview_list" :key="index"> -->
          <!-- <p class="text-center">{{ image_list[index].name }}</p> -->
          <div class="text-center col-lg-6 mx-auto">
            <img :src="preview" class="img-fluid my-4" />
            <!-- <img :src="item" class="img-fluid mt-4" /> -->
          </div>
          <!-- <p>size: {{ image_list[index].size / 1024 }}KB</p> -->
          <!-- </div> -->
          <div
            class="container-fluid d-grid col-2 align-items-center text-center py-3"
          >
            <button class="btn btn-primary btn-sm rounded-pill" @click="reset">
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogAdd",
  data: function () {
    return {
      preview: null,
      image: null,
      blogtext: "",
    };
  },
  methods: {
    previewImage: function (event) {
      var input = event.target;
      if (input.files) {
        var reader = new FileReader();
        reader.onload = (e) => {
          this.preview = e.target.result;
        };
        this.image = input.files[0];
        reader.readAsDataURL(input.files[0]);
      }
    },
    reset: function () {
      this.image = null;
      this.preview = null;
      this.blogtext = "";
    },
    async PostBlog() {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog";
      const photo = document.getElementById("blog-image").files[0];
      // console.log(photo);
      // const photo = this.$refs.image.files[0];
      var form = {
        text: this.blogtext,
        photo: photo,
      };
      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;
      // console.log(auth);
      var requestOptions = {
        method: "POST",
        headers: {
          // Authorization: this.$store.getters.getToken,
          "Content-Type": "application/json",
          Authorization: auth,
        },
        body: JSON.stringify(form),
      };
      const response = await fetch(url, requestOptions);
      if (response.status == 201) {
        this.$emit("BlogCreated");
        console.log("Blog Successfully Created");
      }
      if (response.status == 401) {
        console.log("Failure");
      }
      this.reset();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.btn-file {
  position: relative;
  overflow: hidden;
}
.btn-file input[type="file"] {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 100%;
  min-height: 100%;
  font-size: 100px;
  text-align: right;
  filter: alpha(opacity=0);
  opacity: 0;
  outline: none;
  cursor: inherit;
  display: block;
}
.container {
  display: flex;
}
</style>
