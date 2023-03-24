<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="d-flex justify-content-center">
              <img
                id="user-dp-image"
                v-if="profileDetails"
                :src="profileDetails.dpImageSrc"
                width="180"
                height="180"
                class="rounded-circle bg-white shadow-sm"
              />
            </div>
            <div class="d-flex">
              <h2 class="mx-auto py-2" id="user-name" v-if="profileDetails">
                {{ profileDetails.userName }}
              </h2>
              <!-- <h2 class="mx-auto py-2">User Profile: {{ this.user_id }}</h2> -->
            </div>
            <div class="d-flex">
              <button
                class="btn btn-primary mx-auto rounded-pill lh-1"
                type="button"
                @click="toggleFollow"
              >
                <i
                  :class="{
                    'bi bi-person-plus-fill': !followed,
                    'bi bi-person-check-fill': followed,
                  }"
                ></i
                >&nbsp;{{ followed ? "Following" : "Follow" }}
              </button>
            </div>

            <div class="d-flex pt-2 mx-auto text-center justify-content-center">
              <button
                class="btn btn-link text-decoration-none"
                v-if="profileDetails"
              >
                <i class="bi bi-people-fill"></i>&nbsp;
                {{ profileDetails.userFollowers }}&nbsp;Followers
              </button>
              <button
                class="btn btn-link text-decoration-none"
                v-if="profileDetails"
              >
                <i class="bi bi-person-check-fill"></i>&nbsp;
                {{ profileDetails.userFollowing }}&nbsp;Following
              </button>
              <button
                class="btn btn-link text-decoration-none"
                @click="$emit('user-posts')"
                v-if="profileDetails"
              >
                <i class="bi bi-clipboard2-fill"></i>&nbsp;
                {{ profileDetails.userPosts }}&nbsp;Posts
              </button>
              <!-- <button class="btn ms-auto fs-6 fw-bolder">25 Jan 2023</button> -->
              <!-- @click="this.$emit(viewPosts)" -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileComp",

  props: {
    userID: {
      type: Number,
      required: true,
    },
  },
  mounted() {
    this.FetchProfile();
  },
  data: function () {
    return {
      followed: false,
      profileData: null,
      user_id: this.userID,
    };
  },

  methods: {
    toggleFollow() {
      this.followed = !this.followed;
    },
    FetchProfile() {
      var id = this.user_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/" + id;

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
          this.profileData = data;
          // console.log(data);
          // console.log(this.profileData.name);
          // var dp = document.getElementById("user-dp-image");
          // dp.src = `data:${data.dp_mimetype};charset=utf-8;base64,${data.dp}`;

          // var followers = document.getElementById("follower-count");
          // followers.textContent = data.followers;

          // var following = document.getElementById("following-count");
          // following.textContent = data.followed_users.length;

          // var name = document.getElementById("user-name");
          // name.textContent = data.name;

          // var posts = document.getElementById("user-posts");
          // posts.textContent = data.posts;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },

  computed: {
    profileDetails() {
      if (this.profileData) {
        return {
          userName: this.profileData.name,
          dpImageSrc: `data:${this.profileData.dp_mimetype};charset=utf-8;base64,${this.profileData.dp}`,
          userPosts: this.profileData.blog.length,
          userFollowers: this.profileData.followers,
          userFollowing: this.profileData.followed_users.length,
          // authorName: this.blogData.user.name,
          // blogUserID: this.blogData.user.id,
        };
      }
      return null;
    },

    // isFollowing() {
    //   if (this.blogData) {
    //     return this.blogData.user.followed;
    //   }
    //   return false;
    // },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-height: 300px;
}
</style>
