<template>
  <div class="home">
    <FeedNav />
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";

export default {
  name: "HomeView",
  components: {
    FeedNav,
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
}
</style>
