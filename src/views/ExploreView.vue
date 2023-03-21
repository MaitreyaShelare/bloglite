<template>
  <div class="explore">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="AlluserPosts pt-5">
      <BlogComp />
      <BlogComp />
      <BlogComp />
    </div>
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
        <HelloWorld msg="Welcome to Your Vue.js App" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import BlogComp from "@/components/BlogComp.vue";

export default {
  name: "ExploreView",
  components: {
    FeedNav,
    BlogComp,
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
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
