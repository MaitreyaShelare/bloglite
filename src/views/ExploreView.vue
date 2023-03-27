<template>
  <div class="explore">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="blogs pt-5" v-for="blog in blogs" :key="blog">
      <BlogComp
        :blogID="blog"
        @toggleHide="FetchBlogs"
        @editBlog="showEditModal"
      />
    </div>
    <div v-if="showModal">
      <BlogModal
        :blogID="modalBlogID"
        @close="closeModal"
        @updated="closeEditModal"
      />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import BlogComp from "@/components/BlogComp.vue";
import BlogModal from "@/components/BlogModal.vue";

export default {
  name: "ExploreView",
  components: {
    FeedNav,
    BlogComp,
    BlogModal,
  },
  data: function () {
    return {
      blogs: [],
      modalBlogID: null,
      showModal: false,
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
      var url = base + "/api/blogs";

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
          if (data.msg === "Token has expired") {
            this.refreshToken();
          } else {
            this.blogs = data;
            this.blogKey = 0;
          }
        });
    },
    refreshToken() {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/refresh";

      var refreshtoken = this.$store.getters.getRefreshToken;
      var pureToken = refreshtoken.replace(/["]+/g, "");
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
          this.$store.commit("setToken", data.access_token);
          this.FetchBlogs();
        });
    },
    showEditModal(blogID) {
      this.modalBlogID = blogID;
      console.log(this.modalBlogID);
      this.showModal = true;
    },
    closeEditModal() {
      this.showModal = false;
      this.modalBlogID = null;
      this.blogs = [];
    },
    closeModal() {
      this.showModal = false;
      this.modalBlogID = null;
    },
  },
  watch: {
    blogs: function () {
      this.FetchBlogs();
    },
  },
};
</script>

<style>
.explore {
  height: 100vh;
  width: 100%;
  background-color: #eeeeee;
  /* background-color: #e9ebee; */
  overflow-y: auto;
}
</style>
