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
                    width="32"
                    height="32"
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
                  <button
                    type="button"
                    class="btn btn-sm float-end"
                    data-bs-toggle="dropdown"
                  >
                    <i class="bi bi-three-dots"></i>
                  </button>
                  <ul class="dropdown-menu">
                    <li><button class="dropdown-item">Edit</button></li>
                    <li>
                      <button class="dropdown-item">Delete</button>
                    </li>
                    <li><button class="dropdown-item">Export</button></li>
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
                >&nbsp;
                <span v-if="!liked">Like</span>
                <span v-else>Liked</span>
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
                <div class="d-flex align-items-center">
                  <a
                    class="fw-bold mb-0 text-decoration-none text-black"
                    href="#!"
                    >Mamur Fechetti</a
                  ><span class="text-600 fw-semi-bold fs--2 ms-2"
                    >35 mins ago</span
                  >
                </div>
                <p class="mb-0">
                  How long did it take to create this? It appears that you
                  quickly produced the second one.
                </p>
                <button
                  class="btn btn-link p-0 text-900 text-decoration-none fw-bolder mb-2"
                  type="button"
                ></button>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="me-2">
                <img
                  src="https://github.com/mdo.png"
                  alt="mdo"
                  width="32"
                  height="32"
                  class="rounded-circle"
                />
              </div>
              <div class="flex-1 w-100">
                <input
                  class="form-control"
                  type="text"
                  placeholder="Add comment"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogComp",
  props: {
    blogID: Number,
  },

  data: function () {
    return {
      showComments: false,
      liked: false,
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
    toggleLike() {
      this.liked = !this.liked;
    },
    // goToProfile() {
    //   this.$router.push({
    //     name: "profile",
    //     params: { userId: this.Blogdata.id },
    //   });
    //   // this.$router.push({ name: "profile" });
    // },
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
          console.log(data);
          this.blogData = data;
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
        return `${minutesDifference} minutes ago`;
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
