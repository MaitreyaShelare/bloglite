<template>
  <div class="comment">
    <a class="btn btn-sm float-end" data-bs-toggle="dropdown" v-if="canDelete">
      <i class="bi bi-three-dots"></i>
    </a>
    <div class="d-flex align-items-start">
      <div class="me-2">
        <img
          v-if="commentImage"
          :src="commentImage.dpImageSrc"
          alt="dp"
          width="35"
          height="35"
          class="rounded-circle"
        />
      </div>
      <div class="flex-1 w-100" v-if="comment">
        <div class="d-flex">
          <a
            class="fw-bold mb-0 text-decoration-none text-black"
            style="cursor: pointer"
            @click="
              $router.push({
                name: 'profile',
                params: { userId: comment.user.id },
              })
            "
            >{{ comment.user.name }}</a
          ><span class="text-600 fw-semi-bold fs--2 ms-2">{{
            commentDate
          }}</span>
          <ul class="dropdown-menu">
            <li>
              <button class="dropdown-item" @click="deleteComment">
                <i class="bi bi-trash-fill"></i>&nbsp;&nbsp; Delete
              </button>
            </li>
          </ul>
        </div>
        <p class="mb-0">
          {{ comment.text }}
        </p>
        <button
          class="btn btn-link p-0 text-900 text-decoration-none fw-bolder mb-2"
          type="button"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SingleComment",
  props: {
    commentID: {
      type: Number,
      required: true,
    },
  },

  data: function () {
    return {
      comment_id: this.commentID,
      canDelete: null,
      comment: null,
    };
  },
  mounted() {
    this.FetchComment();
  },

  methods: {
    FetchComment() {
      var commentid = this.comment_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/comment/" + commentid;

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
          this.comment = data;
          console.log(this.comment);
          this.checkDelete();
        });
    },
    checkDelete() {
      if (this.comment) {
        if (this.comment.user.id == this.$store.getters.getCurrentUserID) {
          this.canDelete = true;
        }
      }
    },
    deleteComment() {
      var commentid = this.comment_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/comment/" + commentid;

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
          this.$emit("comment-updated");
        });
    },
  },
  computed: {
    commentDate() {
      if (!this.comment.timestamp) {
        return null;
      }
      const postTimestamp = new Date(this.comment.timestamp);
      const currentTimestamp = new Date(this.comment.server_time);
      const timeDifference =
        currentTimestamp.getTime() - postTimestamp.getTime();
      const minutesDifference = Math.round(timeDifference / 60000);
      const hoursDifference = Math.floor(minutesDifference / 60);
      if (minutesDifference == 0) {
        return `Just now`;
      }
      if (minutesDifference < 60) {
        // less than an hour
        // return `${minutesDifference} minutes ago`;
        return `A while ago`;
      }
      if (minutesDifference < 120) {
        //  an hour ago
        return `An hour ago`;
      }
      if (minutesDifference < 1440) {
        // less than a day
        return `${hoursDifference} hours ago`;
        // return `${currentTimestamp} current time,${postTimestamp} post time`;
      } else {
        const day = postTimestamp.getDate();
        const month = postTimestamp.toLocaleString("default", {
          month: "short",
        });
        const year = postTimestamp.getFullYear();
        return `${day} ${month} ${year}`;
      }
    },
    commentImage() {
      if (this.comment) {
        return {
          dpImageSrc: `data:${this.comment.user.dp_mimetype};charset=utf-8;base64,${this.comment.user.dp}`,
        };
      }
      return null;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
