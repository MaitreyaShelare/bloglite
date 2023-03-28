<template>
  <div class="profile">
    <div class="navbar">
      <FeedNav />
    </div>
    <div class="userprofile pt-5">
      <ProfileComp
        :userID="userId"
        :key="userId + profileKey"
        @profile-updated="UpdateProfile()"
        @user-posts="userPosts()"
        @user-followers="userFollowers()"
        @user-following="userFollowing()"
      />
      <!-- <h2 class="mx-auto py-2">User Profile: {{ this.userId }}</h2> -->
    </div>
    <div class="blogs" v-if="seePosts">
      <div class="userblogs pt-5" v-for="blog in blogs" :key="blog">
        <BlogComp :blogID="blog" @editBlog="showEditModal" />
      </div>
    </div>

    <div class="followers" v-if="!nofollowers">
      <div v-if="seeFollowers">
        <div class="container">
          <div class="col col-md-6 mx-auto mt-2">
            <div class="card mb-4 overflow-hidden">
              <div class="card-body p-3 p-sm-4">
                <div
                  class="userfollowers"
                  v-for="follower in followers"
                  :key="follower"
                >
                  <SearchUsers
                    :userID="follower"
                    @toggle-follow="UpdateProfile()"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="following" v-if="!nofollowing">
      <div v-if="seeFollowing">
        <div class="container">
          <div class="col col-md-6 mx-auto mt-2">
            <div class="card mb-4 overflow-hidden">
              <div class="card-body p-3 p-sm-4">
                <div
                  class="userfollowing"
                  v-for="following in following"
                  :key="following"
                >
                  <SearchUsers
                    :userID="following"
                    @toggle-follow="UpdateProfile()"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
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
import ProfileComp from "@/components/ProfileComp.vue";
import BlogComp from "@/components/BlogComp.vue";
import SearchUsers from "@/components/SearchUsers.vue";
import BlogModal from "@/components/BlogModal.vue";

export default {
  name: "ProfileView",
  components: {
    FeedNav,
    ProfileComp,
    BlogComp,
    SearchUsers,
    BlogModal,
  },
  props: ["userId"],

  data() {
    return {
      seePosts: true,
      seeFollowers: false,
      seeFollowing: false,
      nofollowers: false,
      nofollowing: false,
      showModal: false,
      modalBlogID: null,
      profileKey: 0,
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
    this.FetchFollowers();
    this.FetchFollowing();
  },
  methods: {
    showEditModal(blogID) {
      this.modalBlogID = blogID;
      console.log(this.modalBlogID);
      this.showModal = true;
    },
    closeEditModal() {
      this.showModal = false;
      this.modalBlogID = null;
      this.blogs = [];
      this.FetchBlogs();
    },
    closeModal() {
      this.showModal = false;
      this.modalBlogID = null;
    },
    UpdateProfile() {
      // console.log("changed");
      this.profileKey += 1;
      this.blogs = [];
      this.FetchBlogs();
      // this.seePosts = false;
      // this.seeFollowers = false;
      // this.seeFollowing = false;
    },
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
      this.seePosts = false;
      this.seeFollowing = false;
      // this.seeFollowers = !this.seeFollowers;
      this.FetchFollowers();
      if (this.nofollowers) {
        this.seeFollowers = false;
      } else {
        this.seeFollowers = !this.seeFollowers;
      }
    },
    userFollowing() {
      this.seePosts = false;
      this.seeFollowers = false;
      // this.seeFollowing = !this.seeFollowing;
      this.FetchFollowing();
      if (this.nofollowing) {
        this.seeFollowing = false;
      } else {
        this.seeFollowing = !this.seeFollowing;
      }
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
          if (data.msg === "Token has expired") {
            this.refreshToken();
          } else {
            this.blogs = data;
          }
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
          // console.log(this.followers);
          if (this.followers.length == 0) {
            this.nofollowers = true;
            // console.log(this.nofollowers);
          } else {
            this.nofollowers = false;
          }
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
          // console.log(this.following);
          if (this.following.length == 0) {
            this.nofollowing = true;
          } else {
            this.nofollowing = false;
          }
        });
    },
    resetData() {
      this.seePosts = true;
      this.seeFollowers = false;
      // this.noFollowers = false;
      this.seeFollowing = false;
      // this.noFollowing = false;
      this.profileKey = 0;
      this.blogs = [];
      this.followers = [];
      this.following = [];
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
  },
  watch: {
    userId: function () {
      // this.update = !this.update;
      this.resetData();
      this.FetchBlogs();
      this.FetchFollowers();
      this.FetchFollowing();
      // this.$forceUpdate();
      // this.$forceRefresh();
    },
  },
};
</script>

<style scoped>
.profile {
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
  min-height: fit-content;
}
</style>
