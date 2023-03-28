<template>
  <div class="comments">
    <div v-for="comment in comments" :key="comment">
      <SingleComment :commentID="comment" @comment-updated="updateComments" />
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
        :disabled="disabled"
        @click="checkComment"
      ></i>
    </div>
  </div>
</template>

<script>
import SingleComment from "@/components/SingleComment.vue";

export default {
  name: "CommentComp",
  components: {
    SingleComment,
  },
  props: {
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
      disabled: true,
    };
  },
  mounted() {
    this.FetchComments();
  },

  methods: {
    FetchComments() {
      var blogid = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/comments/" + blogid;

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
          console.log(data);
        });
    },
    checkComment() {
      if (this.comment.length < 1) {
        this.disabled = true;
      } else {
        // console.log(this.blog_id);
        this.addComment();
        this.comment = "";
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
          console.log(data);
          this.updateComments();
        });
    },
    updateComments() {
      this.comments = [];
      this.FetchComments();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
