<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="border-bottom mb-3">
              <div class="d-flex align-items-center mb-3">
                <a
                  class="d-block link-dark text-decoration-none"
                  style="cursor: pointer"
                  v-if="blogDetails"
                  @click="
                    $router.push({
                      name: 'profile',
                      params: { userId: blogDetails.blogUserID },
                    })
                  "
                >
                  <!-- @click="$router.push('/profile/' + blogDetails.blogUserID)"
                  :href="'#/profile/' + Blogdata.user.id"
                  @click="$router.push('/profile/1')" -->
                  <img
                    id="dp-image-small"
                    v-if="blogDetails"
                    :src="blogDetails.dpImageSrc"
                    alt="dp"
                    width="35"
                    height="35"
                    class="rounded-circle"
                  />
                </a>
                <div class="flex-1">
                  <a
                    id="blog-author"
                    class="fw-bold fs-6 ms-2 mb-0 text-decoration-none text-black"
                    style="cursor: pointer"
                    v-if="blogDetails"
                    @click="
                      $router.push({
                        name: 'profile',
                        params: { userId: blogDetails.blogUserID },
                      })
                    "
                    >{{ blogDetails.authorName }}</a
                  >
                </div>
                <div class="ms-auto">
                  <a class="btn btn-sm float-end" data-bs-toggle="dropdown">
                    <i class="bi bi-three-dots"></i>
                  </a>
                  <ul class="dropdown-menu">
                    <li>
                      <button
                        class="dropdown-item"
                        v-if="superUser"
                        @click="editBlog"
                      >
                        <i class="bi bi-pen-fill"></i>&nbsp;&nbsp; Edit
                      </button>
                    </li>
                    <li>
                      <button
                        class="dropdown-item"
                        v-if="superUser"
                        @click="toggleHide"
                      >
                        <i
                          :class="{
                            'bi bi-caret-down-square-fill': !hidden,
                            'bi bi-caret-up-square-fill': hidden,
                          }"
                        ></i
                        >&nbsp;&nbsp;
                        {{ hidden ? "Unarchive" : "Archive" }}
                      </button>
                    </li>
                    <li>
                      <button class="dropdown-item" @click="exportBlog">
                        <i class="bi bi-share-fill"></i>&nbsp;&nbsp; Share
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
              <p
                class="text-800"
                id="blog-text"
                v-if="blogDetails"
                v-html="text"
              ></p>
              <div class="row g-1 mb-5">
                <div class="mx-auto">
                  <img
                    id="blog-image"
                    class="rounded h-100 w-100"
                    v-if="blogDetails"
                    :src="blogDetails.blogImageSrc"
                    alt="Blog Image"
                  />
                </div>
              </div>
            </div>
            <div class="d-flex">
              <button
                class="btn btn-link float-start p-0 me-3 fs-6 fw-bolder text-decoration-none"
                type="button"
                @click="toggleLike"
              >
                <i
                  :class="{
                    'bi bi-hand-thumbs-up': !liked,
                    'bi bi-hand-thumbs-up-fill': liked,
                  }"
                ></i
                >&nbsp;{{ liked ? "Liked" : "Like" }}
              </button>
              <button
                class="btn btn-link link-dark p-0 me-3 fs-6 fw-bolder text-decoration-none"
                type="button"
                @click="toggleComments"
              >
                <i
                  :class="{
                    'bi bi-chat': !showComments,
                    'bi bi-chat-fill': showComments,
                  }"
                ></i
                >&nbsp;Comment
              </button>
              <button class="btn ms-auto fs-6 fw-bolder" v-if="blogDetails">
                {{ postDate }}
              </button>
            </div>
          </div>
          <div class="bg-light border-top p-3 p-sm-4" v-if="showComments">
            <CommentComp :blogID="blog_id" :superUser="superUser" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentComp from "@/components/CommentComp.vue";
export default {
  name: "BlogComp",
  props: {
    blogID: Number,
  },
  components: {
    CommentComp,
  },
  data: function () {
    return {
      showComments: false,
      superUser: false,
      hidden: false,
      liked: null,
      blogData: null,
      blog_id: this.blogID,
    };
  },

  mounted() {
    this.FetchData();
  },

  methods: {
    toggleComments() {
      this.showComments = !this.showComments;
    },
    editBlog() {
      // console.log("edit blog");
      this.$emit("editBlog", this.blog_id);
    },
    toggleLike() {
      this.liked = !this.liked;
      this.liked ? this.LikeBlog() : this.UnlikeBlog();
    },
    toggleHide() {
      this.hidden = !this.hidden;
      // this.hidden ? this.HideBlog() : this.UnhideBlog();
      // console.log(this.hidden);
      var blogid = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/toggleHide/" + blogid;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "PATCH",
        headers: {
          Authorization: auth,
        },
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          // this.liked = true;
          this.$emit("toggleHide");
        })
        .catch((error) => {
          console.error(error);
        });
    },
    isLiked() {
      if (this.blogData) {
        var id = this.$store.getters.getCurrentUserID;
        if (this.blogData.liked_by.includes(id)) {
          this.liked = true;
        } else {
          this.liked = false;
        }
      }
    },
    isHidden() {
      if (this.blogData) {
        if (this.blogData.hidden) {
          this.hidden = true;
        } else {
          this.hidden = false;
        }
      }
    },
    isSuperUser() {
      if (this.blogData) {
        var id = this.$store.getters.getCurrentUserID;
        if (this.blogData.user.id == id) {
          this.superUser = true;
          // console.log(this.superUser);
        } else {
          this.superUser = false;
          // console.log(this.superUser);
        }
      }
    },
    LikeBlog() {
      var blogid = this.blog_id;
      var userid = this.$store.getters.getCurrentUserID;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/like/" + userid + "/" + blogid;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "POST",
        headers: {
          Authorization: auth,
        },
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.liked = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    UnlikeBlog() {
      var blogid = this.blog_id;
      var userid = this.$store.getters.getCurrentUserID;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/unlike/" + userid + "/" + blogid;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "POST",
        headers: {
          Authorization: auth,
        },
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.liked = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    exportBlog() {
      var blogid = this.blog_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/blog/export/" + blogid;

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
        .then((response) => response.blob())
        .then((blob) => {
          const url = window.URL.createObjectURL(new Blob([blob]));
          const a = document.createElement("a");
          a.href = url;
          const date = new Date().toISOString().split("T")[0];
          const filename = `blog_${blogid}_${date}.csv`;
          a.setAttribute("download", filename);
          a.click();
        })
        .catch((error) => {
          console.error(error);
        });

      // fetch(url, requestOptions)
      //   .then((response) => response.json())
      //   .then((data) => {
      //     console.log(data);
      //   })
      //   .catch((error) => {
      //     console.error(error);
      //   });
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
          // console.log(data);
          this.blogData = data;
          // console.log(this.blogData);
          this.isLiked();
          this.isSuperUser();
          this.isHidden();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },

  computed: {
    blogDetails() {
      if (this.blogData) {
        return {
          blogImageSrc: `data:${this.blogData.photo_mimetype};charset=utf-8;base64,${this.blogData.photo}`,
          dpImageSrc: `data:${this.blogData.user.dp_mimetype};charset=utf-8;base64,${this.blogData.user.dp}`,
          authorName: this.blogData.user.name,
          blogUserID: this.blogData.user.id,
        };
      }
      return null;
    },

    text() {
      if (this.blogData) {
        return this.blogData.text;
      }
      return null;
    },

    postDate() {
      if (!this.blogData.timestamp) {
        return null;
      }
      const postTimestamp = new Date(this.blogData.timestamp);
      const currentTimestamp = new Date(this.blogData.server_time);
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
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  min-height: 200px;
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
