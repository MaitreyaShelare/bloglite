<template>
  <div class="blogModal">
    <div
      class="modal modal-sheet position-static d-block bg-background py-5"
      tabindex="-1"
      role="dialog"
      id="modalSheet"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content rounded-4 shadow">
          <div class="modal-header border-bottom-0 mx-auto">
            <h1 class="modal-title fs-5">Edit Blog</h1>
          </div>
          <div class="modal-body py-3">
            <!-- {{ blog_id }} -->
            <div class="card mx-auto">
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
                          <path
                            d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"
                          />
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
                </div>
              </div>
              <div pt-2 mt-3 v-if="preview">
                <div class="text-center col-lg-8 mx-3 mx-lg-auto">
                  <div class="text-end mt-2">
                    <button class="btn-close" @click="clearImage"></button>
                  </div>
                  <img :src="preview" class="img-thumbnail my-4" />
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer flex-column border-top-0">
            <button
              type="submit"
              class="btn btn-primary w-100 mx-0 mb-2"
              @click="PostBlog"
              :disabled="blogtext.length < 2"
            >
              Update Blog
            </button>
            <button
              class="btn btn-danger w-100 mx-0 mb-2"
              :disabled="isDisabled"
              @click="handleDeleteClick"
            >
              {{ deleteButtonText }}
            </button>
            <button
              class="btn btn-outline-dark bg border-light w-100 mx-0"
              @click="closeModal"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertModal",
  props: ["blogID"],
  data: function () {
    return {
      blog_id: this.blogID,
      blogData: null,
      preview: null,
      image: null,
      blogtext: "",
      isDisabled: false,
      deleteCounter: 0,
    };
  },
  mounted() {
    this.FetchData();
  },
  methods: {
    closeModal: function () {
      this.$emit("close");
    },
    FetchData() {
      var id = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/" + id;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "GET",
        headers: {
          Authorization: auth,
        },
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          this.blogData = data;
          console.log(this.blogData);
          this.blogtext = this.blogData.text;
          this.preview = `data:${this.blogData.photo_mimetype};charset=utf-8;base64,${this.blogData.photo}`;
          // this.image = this.blogData.photo;
          // console.log(this.image);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    previewImage: function (event) {
      var input = event.target;
      if (input.files) {
        var reader = new FileReader();
        reader.onload = (e) => {
          this.preview = e.target.result;
        };
        this.image = input.files[0];
        // console.log(this.image);
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
      this.deleteCounter = 0;
      this.isDisabled = false;
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
    PostBlog: function () {
      var id = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/" + id;

      var cleanText = this.sanitizeHtml(this.blogtext);

      const formData = new FormData();
      if (this.image) {
        formData.append("image", this.image);
      }
      formData.append("text", cleanText);

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "PATCH",
        headers: {
          Authorization: auth,
        },
        body: formData,
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.$emit("updated");
        })
        .catch((error) => {
          console.log(error);
        });
      this.reset();
    },
    handleDeleteClick() {
      if (this.deleteCounter === 0) {
        this.deleteWarning();
      } else if (this.deleteCounter === 1) {
        this.deleteBlog();
      }
      this.deleteCounter++;
    },
    deleteWarning() {
      // Disable button for 5 seconds
      this.isDisabled = true;
      setTimeout(() => {
        this.isDisabled = false;
      }, 5000);
    },
    deleteBlog: function () {
      var id = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/" + id;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "DELETE",
        headers: {
          Authorization: auth,
        },
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.$emit("updated");
        })
        .catch((error) => {
          console.log(error);
        });
      this.reset();
    },
  },
  computed: {
    deleteDisabled() {
      return this.deleteCounter > 0;
    },
    deleteButtonText() {
      return this.deleteCounter > 0
        ? "This action cannot be undone. Confirm ?"
        : "Delete Blog";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.blogModal {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  background-color: #000000b2;
}

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
