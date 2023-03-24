<template>
  <div class="home">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="blogadd pt-5">
      <BlogAdd />
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
// import BlogComp from "@/components/BlogComp.vue";

export default {
  name: "HomeView",
  components: {
    FeedNav,
    BlogAdd,
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
  },
};
</script>

<style>
.home {
  height: 100vh;
  width: 100%;
  background-color: #eeeeee;
  /* background-color: #e9ebee; */
  overflow-y: auto;
}
</style>
