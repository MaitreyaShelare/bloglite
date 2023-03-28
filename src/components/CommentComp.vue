<template>
  <div class="comments">
    <div class="d-flex align-items-start">
      <div class="me-2">
        <img
          src="https://github.com/mdo.png"
          alt="mdo"
          width="32"
          height="32"
          class="rounded-circle"
        />
      </div>
      <div class="flex-1">
        <div class="d-flex">
          <a class="fw-bold mb-0 text-decoration-none text-black" href="#!"
            >John Smith</a
          ><span class="text-600 fw-semi-bold fs--2 ms-2">{{ blog_id }}</span>
          <a
            class="btn btn-sm ms-auto"
            data-bs-toggle="dropdown"
            v-if="superUser"
          >
            <i class="bi bi-three-dots"></i>
          </a>
          <ul class="dropdown-menu">
            <li>
              <button class="dropdown-item" @click="deleteComment">
                <i class="bi bi-trash-fill"></i>&nbsp;&nbsp; Delete
              </button>
            </li>
          </ul>
        </div>
        <p class="mb-0">
          How long did it take to create this? It appears that you quickly
          produced the second one.
        </p>
        <button
          class="btn btn-link p-0 text-900 text-decoration-none fw-bolder mb-2"
          type="button"
        ></button>
      </div>
    </div>
    <div id="add-comment" class="d-flex align-items-center">
      <div class="flex-1 w-100">
        <input
          class="form-control"
          type="text"
          v-model="comment"
          placeholder="Add comment"
        />
      </div>
      &nbsp;&nbsp;&nbsp;<i
        class="bi bi-send-fill"
        style="cursor: pointer"
        @click="checkComment"
      ></i>
    </div>
  </div>
</template>

<script>
export default {
  name: "CommentComp",
  //   props: ["blogId", "superUser"],
  props: {
    superUser: {
      type: Boolean,
      required: true,
    },
    blogID: {
      type: Number,
      required: true,
    },
  },

  data: function () {
    return {
      blog_id: this.blogID,
      comments: [],
      comment: "",
    };
  },
  mounted() {},

  methods: {
    FetchComments() {
      var id = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/comments" + id;

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
          this.comments = data;
        });
    },
    deleteComment() {
      console.log("delete comment");
    },
    checkComment() {
      if (this.comment.length < 1) {
        console.log("comment is empty");
      } else {
        console.log(this.blog_id);
        this.addComment();
        // console.log("comment is not empty");
        // this.comment = "";
      }
    },
    addComment() {
      var blogid = this.blog_id;
      var userid = this.$store.getters.getCurrentUserID;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/comment/" + userid + "/" + blogid;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      const formData = new FormData();
      formData.append("comment", this.comment);

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
          //   this.comments = data;
          console.log(data);
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
