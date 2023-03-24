<template>
  <div class="explore">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="blogs pt-5" v-for="blog in blogs" :key="blog">
      <BlogComp :blogID="blog" />
    </div>
    <!-- <div class="blogs pt-5">
      <BlogComp />
    </div> -->
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
  data: function () {
    return {
      blogs: [],
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
          this.blogs = data;
          // console.log(this.blogs);
          // console.log(data);
          // console.log(data[1]);
          // console.log(data[0].text);
          //   var img = document.getElementById("blog-image");
          //   img.src = `data:${data.photo_mimetype};charset=utf-8;base64,${data.photo}`;

          //   var dp = document.getElementById("dp-image-small");
          //   dp.src = `data:${data.user.dp_mimetype};charset=utf-8;base64,${data.user.dp}`;

          //   var text = document.getElementById("blog-text");
          //   text.innerHTML = data.text;

          //   var author = document.getElementById("blog-author");
          //   author.textContent = data.user.name;
          // })
          // .catch((error) => {
          //   console.error(error);
        });
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
