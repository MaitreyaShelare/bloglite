<template>
  <div class="blogadd">
    <div class="container">
      <div class="card col col-md-6 mx-auto mt-2 mb-3">
        <textarea
          class="form-control border-200 rounded border-0 flex-1 fs-0"
          rows="3"
          contenteditable="true"
          placeholder="What's on your mind?"
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
                :disabled="blogtext.length < 2 || !image"
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
          <div class="text-center col-lg-10 mx-3 mx-lg-auto">
            <div class="text-end mt-2">
              <button class="btn-close" @click="clearImage"></button>
            </div>
            <img :src="preview" class="img-thumbnail my-4" />
            <!-- <img :src="item" class="img-fluid mt-4" /> -->
          </div>
          <!-- <p>size: {{ image_list[index].size / 1024 }}KB</p> -->
          <!-- </div> -->
          <!-- <div
            class="container-fluid d-grid col-2 align-items-center text-center py-3"
          >
            
          </div> -->
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
    clearImage: function () {
      this.image = null;
      this.preview = null;
    },
    reset: function () {
      this.image = null;
      this.preview = null;
      this.blogtext = "";
    },
    sanitizeHtml(html) {
      const allowedTags = ["p", "a", "b", "i", "u", "ul", "ol", "li"];
      const allowedAttrs = ["href"];

      return html
        .replace(/<(\/?)(\w+)[^>]*>/g, (match, endTag, tagName) => {
          if (allowedTags.indexOf(tagName.toLowerCase()) !== -1) {
            return `<${endTag}${tagName}>`;
          } else {
            return "";
          }
        })
        .replace(/\b(\w+)="[^"]*"/g, (match, attrName) => {
          if (allowedAttrs.indexOf(attrName.toLowerCase()) !== -1) {
            return `${attrName}="${match.slice(attrName.length + 2, -1)}"`;
          } else {
            return "";
          }
        });
    },
    // sanitizeHtml(html) {
    //   const allowedTags = ["p", "b", "i", "u", "ul", "ol", "li"];
    //   const regex = /<([^>]+)>/gi;

    //   return html
    //     .replace(regex, (tag, name) => {
    //       if (allowedTags.includes(name)) {
    //         return tag;
    //       } else {
    //         return "";
    //       }
    //     })
    //     .replace(/&/g, "&amp;")
    //     .replace(/</g, "&lt;")
    //     .replace(/>/g, "&gt;")
    //     .replace(/"/g, "&quot;")
    //     .replace(/'/g, "&#x27;")
    //     .replace(/\//g, "&#x2F;");
    // },

    // sanitizeHtml(html) {
    //   const allowedTags = ["p", "b", "i", "u", "ul", "ol", "li"];
    //   // const allowedAttrs = ["href"];

    //   return html.replace(/<(\/?)(\w+)[^>]*>/g, (match, endTag, tagName) => {
    //     if (allowedTags.indexOf(tagName.toLowerCase()) !== -1) {
    //       return `<${endTag}${tagName}>`;
    //     } else {
    //       return "";
    //     }
    //   });
    //   // .replace(/\b(\w+)="[^"]*"/g, (match, attrName) => {
    //   //   if (allowedAttrs.indexOf(attrName.toLowerCase()) !== -1) {
    //   //     return `${attrName}="${match.slice(attrName.length + 2, -1)}"`;
    //   //   } else {
    //   //     return "";
    //   //   }
    //   // });
    // },
    PostBlog: function () {
      // console.log(this.image);
      // console.log(this.blogtext);
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog";

      var cleanText = this.sanitizeHtml(this.blogtext);

      const formData = new FormData();
      formData.append("image", this.image);
      formData.append("text", cleanText);

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "POST",
        headers: {
          Authorization: auth,
        },
        body: formData,
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.$emit("BlogCreated");
        })
        .catch((error) => {
          console.log(error);
        });
      this.reset();
    },
    // async postBlog() {
    //   var base = this.$store.getters.getBaseURL;
    //   var url = base + "/api/blog";
    //   var photo = document.getElementById("blog-image").files[0];
    //   console.log(photo);
    //   // const photo = this.$refs.image.files[0];
    //   var form = {
    //     text: this.blogtext,
    //     photo: photo,
    //   };
    //   var token = this.$store.getters.getToken;
    //   var pureToken = token.replace(/["]+/g, "");
    //   var auth = `Bearer ${pureToken}`;
    //   // console.log(auth);
    //   var requestOptions = {
    //     method: "POST",
    //     headers: {
    //       // Authorization: this.$store.getters.getToken,
    //       "Content-Type": "application/json",
    //       Authorization: auth,
    //     },
    //     body: JSON.stringify(form),
    //   };
    //   const response = await fetch(url, requestOptions);
    //   if (response.status == 201) {
    //     this.$emit("BlogCreated");
    //     console.log("Blog Successfully Created");
    //   }
    //   if (response.status == 401) {
    //     console.log("Failure");
    //   }
    //   this.reset();
    // },
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
.card {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
