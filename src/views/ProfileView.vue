<template>
  <div class="profile">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="userprofile pt-5">
      <ProfileComp :userID="userId" :key="userId" @user-posts="userPosts()" />
      <!-- <h2 class="mx-auto py-2">User Profile: {{ this.userId }}</h2> -->
    </div>
    <div class="blogs" v-if="seePosts">
      <div class="userblogs pt-5" v-for="blog in blogs" :key="blog">
        <BlogComp :blogID="blog" />
      </div>
    </div>

    <!-- <div class="userPosts pt-2">
      <BlogComp />
    </div> -->
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
      <HelloWorld msg="Welcome to Your Vue.js App" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import ProfileComp from "@/components/ProfileComp.vue";
import BlogComp from "@/components/BlogComp.vue";

export default {
  name: "ProfileView",
  components: {
    FeedNav,
    ProfileComp,
    BlogComp,
  },
  // props: ["userId"],
  props: {
    userId: Number,
  },
  data() {
    return {
      seePosts: true,
      seeFollowers: false,
      seeFollowing: false,
      blogs: [],
    };
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
    this.FetchBlogs();
  },
  watch: {
    userId: function () {
      // this.update = !this.update;
      this.FetchBlogs();
      // this.$forceUpdate();
      // this.$forceRefresh();
    },
  },
  methods: {
    userPosts() {
      // console.log("userPosts");
      this.FetchBlogs();
      this.seePosts = !this.seePosts;
      // console.log(this.seePosts);
      // console.log(this.userId);
    },
    FetchBlogs() {
      var id = this.userId;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/blogs/" + id;

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
        });
    },
  },
};
</script>

<style>
.profile {
  height: 100vh;
  width: 100%;
  background-color: #eeeeee;
  /* background-color: #e9ebee; */
  overflow-y: auto;
}
</style>
