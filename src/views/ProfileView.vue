<template>
  <div class="home">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="profile pt-5">
      <ProfileComp />
    </div>
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
      <HelloWorld msg="Welcome to Your Vue.js App" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import ProfileComp from "@/components/ProfileComp.vue";

export default {
  name: "ProfileView",
  components: {
    FeedNav,
    ProfileComp,
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
