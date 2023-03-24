<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="d-flex justify-content-center">
              <img
                id="user-dp-image"
                src=""
                width="180"
                height="180"
                class="rounded-circle bg-white shadow-sm"
              />
            </div>
            <div class="d-flex">
              <h2 class="mx-auto py-2" id="user-name"></h2>
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
              <button class="btn btn-link text-decoration-none">
                <i class="bi bi-people-fill"></i>&nbsp;<span
                  id="follower-count"
                ></span
                >&nbsp;Followers
              </button>
              <button class="btn btn-link text-decoration-none" type="button">
                <i class="bi bi-person-check-fill"></i>&nbsp;<span
                  id="following-count"
                ></span
                >&nbsp;Following
              </button>
              <button class="btn btn-link text-decoration-none" type="button">
                <i class="bi bi-clipboard2-fill"></i>&nbsp;<span
                  id="user-posts"
                ></span
                >&nbsp;Posts
              </button>
              <!-- <button class="btn ms-auto fs-6 fw-bolder">25 Jan 2023</button> -->
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
  mounted() {
    this.FetchProfile();
  },
  data: function () {
    return {
      followed: false,
    };
  },

  methods: {
    toggleFollow() {
      this.followed = !this.followed;
    },
    FetchProfile() {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/1";

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
          var dp = document.getElementById("user-dp-image");
          dp.src = `data:${data.dp_mimetype};charset=utf-8;base64,${data.dp}`;

          var followers = document.getElementById("follower-count");
          followers.textContent = data.followers;

          var following = document.getElementById("following-count");
          following.textContent = data.followed_users.length;

          var name = document.getElementById("user-name");
          name.textContent = data.name;

          var posts = document.getElementById("user-posts");
          posts.textContent = data.posts;
        })
        .catch((error) => {
          console.error(error);
        });
    },
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
