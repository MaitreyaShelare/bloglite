<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="d-flex justify-content-center">
              <img
                src="https://github.com/mdo.png"
                width="180"
                height="180"
                class="rounded-circle bg-white img-thumbnail shadow-sm"
              />
            </div>
            <div class="d-flex">
              <h2 class="mx-auto py-2">Erza Bridgest</h2>
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
                <i class="bi bi-people-fill"></i>&nbsp;50 Followers
              </button>
              <button class="btn btn-link text-decoration-none" type="button">
                <i class="bi bi-person-check-fill"></i>&nbsp;50 Following
              </button>
              <button class="btn btn-link text-decoration-none" type="button">
                <i class="bi bi-clipboard2-fill"></i>&nbsp;50 Posts
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
      var url = base + "/api/blog/1";

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
          // var img = document.getElementById("blog-image");
          // img.src = `data:${data.photo_mimetype};charset=utf-8;base64,${data.photo}`;

          // var dp = document.getElementById("dp-image-small");
          // dp.src = `data:${data.user.dp_mimetype};charset=utf-8;base64,${data.user.dp}`;

          // var text = document.getElementById("single-blog-text");
          // text.textContent = data.text;

          // var author = document.getElementById("blog-author");
          // author.textContent = data.user.name;
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
