<template>
  <div class="profile">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="userprofile pt-5">
      <ProfileComp
        :userID="userId"
        :key="userId"
        @user-posts="userPosts()"
        @user-followers="userFollowers()"
        @user-following="userFollowing()"
      />
      <!-- <h2 class="mx-auto py-2">User Profile: {{ this.userId }}</h2> -->
    </div>
    <div class="blogs" v-if="seePosts">
      <div class="userblogs pt-5" v-for="blog in blogs" :key="blog">
        <BlogComp :blogID="blog" />
      </div>
    </div>
    <div class="followers" v-if="seeFollowers">
      <div
        class="userfollowers pt-5"
        v-for="follower in followers"
        :key="follower"
      >
        <SearchUsers :userID="follower" />
      </div>
    </div>
    <div class="following" v-if="seeFollowing">
      <div
        class="userfollowing pt-5"
        v-for="following in following"
        :key="following"
      >
        <SearchUsers :userID="following" />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import FeedNav from "@/components/FeedNav.vue";
import ProfileComp from "@/components/ProfileComp.vue";
import BlogComp from "@/components/BlogComp.vue";
import SearchUsers from "@/components/SearchUsers.vue";

export default {
  name: "ProfileView",
  components: {
    FeedNav,
    ProfileComp,
    BlogComp,
    SearchUsers,
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
      followers: [],
      following: [],
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
      this.seeFollowers = false;
      this.seeFollowing = false;
      this.seePosts = !this.seePosts;
      // console.log(this.seePosts);
      // console.log(this.userId);
    },
    userFollowers() {
      this.FetchFollowers();
      this.seePosts = false;
      this.seeFollowing = false;
      this.seeFollowers = !this.seeFollowers;
    },
    userFollowing() {
      this.FetchFollowing();
      this.seePosts = false;
      this.seeFollowers = false;
      this.seeFollowing = !this.seeFollowing;
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
    FetchFollowers() {
      var id = this.userId;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/followers/" + id;

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
          this.followers = data;
          console.log(this.followers);
        });
    },
    FetchFollowing() {
      var id = this.userId;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/following/" + id;

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
          this.following = data;
          console.log(this.following);
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
