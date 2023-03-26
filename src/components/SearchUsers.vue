<template>
  <div class="searchUser">
    <div class="card-body p-2">
      <div class="mb-3">
        <div class="d-flex align-items-center mb-3">
          <a class="d-block link-dark text-decoration-none">
            <img
              v-if="profileDetails"
              :src="profileDetails.dpImageSrc"
              width="32"
              height="32"
              class="rounded-circle"
              style="cursor: pointer"
              @click="
                $router.push({
                  name: 'profile',
                  params: { userId: profileData.id },
                })
              "
            />
          </a>
          <div class="flex-1">
            <a
              class="fw-bold fs-6 ms-2 mb-0 text-decoration-none text-black"
              v-if="profileDetails"
              style="cursor: pointer"
              @click="
                $router.push({
                  name: 'profile',
                  params: { userId: profileData.id },
                })
              "
              >{{ profileDetails.userName }}</a
            >
          </div>
          <div class="ms-auto">
            <div class="d-flex">
              <button
                class="btn btn-primary mx-auto rounded-pill lh-1"
                v-if="differentUser"
                @click="toggleFollow"
              >
                <i
                  :class="{
                    'bi bi-person-plus-fill': !followed,
                    'bi bi-person-check-fill': followed,
                  }"
                ></i
                >&nbsp;{{ followed ? "Following" : "Follow" }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchUsers",
  props: {
    userID: {
      type: Number,
      required: true,
    },
  },
  data: function () {
    return {
      user_id: this.userID,
      differentUser: false,
      profileData: null,
      followed: null,
    };
  },
  mounted() {
    this.FetchProfile();
    this.isFollowed();
    this.checkUser();
  },

  methods: {
    toggleFollow() {
      this.followed ? this.UnfollowUser() : this.FollowUser(),
        (this.followed = !this.followed);
      this.$emit("toggle-follow");
    },
    isFollowed() {
      if (this.profileData) {
        this.follower_count = this.profileData.followers_users.length;
        var id = this.$store.getters.getCurrentUserID;
        if (this.profileData.followers_users.includes(id)) {
          this.followed = true;
        } else {
          this.followed = false;
        }
      }
    },
    checkUser() {
      if (this.$store.getters.getCurrentUserID == this.user_id) {
        this.differentUser = false;
      } else {
        this.differentUser = true;
      }
    },
    FetchProfile() {
      var id = this.user_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/" + id;

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
          this.profileData = data;
          console.log(this.profileData);
          this.isFollowed();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    FollowUser() {
      var id = this.user_id;
      var currentid = this.$store.getters.getCurrentUserID;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/follow/" + currentid + "/" + id;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
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
          console.log(data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    UnfollowUser() {
      var id = this.user_id;
      var currentid = this.$store.getters.getCurrentUserID;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/unfollow/" + currentid + "/" + id;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
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
          console.log(data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  computed: {
    profileDetails() {
      if (this.profileData) {
        return {
          userName: this.profileData.name,
          dpImageSrc: `data:${this.profileData.dp_mimetype};charset=utf-8;base64,${this.profileData.dp}`,
        };
      }
      return null;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
