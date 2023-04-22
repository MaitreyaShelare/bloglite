<template>
  <div class="search">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="Searchuser pt-5">
      <SearchComp />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import SearchComp from "@/components/SearchComp.vue";

export default {
  name: "SearchView",
  components: {
    FeedNav,
    SearchComp,
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
  },
};
</script>

<style>
.search {
  height: 100vh;
  width: 100%;
  background-color: #eeeeee;
  /* background-color: #e9ebee; */
  overflow-y: auto;
}
</style>
