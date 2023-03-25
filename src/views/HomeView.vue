<template>
  <div class="home">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="blogadd pt-5">
      <BlogAdd />
    </div>
    <div class="follow pt-5" v-if="noBlogs">
      <div class="container">
        <div class="col col-md-6 mx-auto mt-2">
          <div class="card mb-4 overflow-hidden">
            <div class="card-body p-3 p-sm-4">
              <h3 class="text-center">Follow some users to see their posts</h3>
              <!-- <div class="d-flex py-1">
                <a
                  class="btn btn-primary mx-auto rounded-pill lh-1"
                  href="#/search"
                >
                  <i class="bi bi-search"></i>
                  &nbsp;Search
                </a>
              </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="feed pt-5" v-for="blog in blogs" :key="blog">
      <BlogComp :blogID="blog" />
    </div>
    <!-- <div class="blog_feed">
      <BlogComp />
    </div> -->
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import BlogAdd from "@/components/BlogAdd.vue";
import BlogComp from "@/components/BlogComp.vue";
// import SearchUsers from "@/components/SearchUsers.vue";

export default {
  name: "HomeView",
  components: {
    FeedNav,
    BlogAdd,
    BlogComp,
  },
  data: function () {
    return {
      blogs: [],
      noBlogs: true,
    };
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
    this.FetchBlogs();
  },
  methods: {
    FetchBlogs() {
      var base = this.$store.getters.getBaseURL;
      var id = this.$store.getters.getCurrentUserID;
      var url = base + "/api/feed/" + id;

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
          this.blogs = data;
          if (this.blogs.length > 0) {
            this.noBlogs = false;
          }
        });
    },
  },
};
</script>

<style scoped>
.home {
  height: 100vh;
  width: 100%;
  background-color: #eeeeee;
  /* background-color: #e9ebee; */
  overflow-y: auto;
}

.card {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-height: 100px;
}
</style>
