<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="d-flex justify-content-center" v-if="profileDetails">
              <form>
                <div class="form-group" id="dp">
                  <span class="btn btn-file">
                    <img
                      id="user-dp-image"
                      :src="profileDetails.dpImageSrc"
                      width="180"
                      height="180"
                      class="rounded-circle bg-white shadow-sm"
                    />
                    <div class="div" v-if="!differentUser">
                      <input
                        type="file"
                        name="dp-image"
                        accept="image/*"
                        @change="changeDp"
                      />
                    </div>
                  </span>
                </div>
              </form>
            </div>
            <div
              class="d-flex mx-auto text-center justify-content-center"
              ref="editable"
              v-if="profileDetails"
              @click="startEditing"
            >
              <div v-if="!isEditing">
                <h2 class="py-2" style="cursor: pointer">
                  {{ userName }}
                </h2>
              </div>
              <div v-else>
                <input
                  type="text"
                  class="h2 py-2 editable"
                  id="editable"
                  v-model="userName"
                  @keyup.enter="endEditing"
                  :style="{
                    textAlign: 'center',
                    fontStyle: isEditing ? 'italic' : 'normal',
                    cursor: isEditing ? 'text' : 'pointer',
                  }"
                />
              </div>
            </div>
            <div class="d-flex" v-if="differentUser">
              <button
                class="btn btn-primary mx-auto rounded-pill lh-1"
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

            <div class="d-flex pt-2 mx-auto text-center justify-content-center">
              <button
                class="btn btn-link text-decoration-none"
                @click="$emit('user-followers')"
                v-if="profileDetails"
              >
                <i class="bi bi-people-fill"></i>&nbsp;
                <!-- {{ profileDetails.userFollowers }}&nbsp;Followers -->
                {{ this.follower_count }}&nbsp;Followers
              </button>
              <button
                class="btn btn-link text-decoration-none"
                @click="$emit('user-following')"
                v-if="profileDetails"
              >
                <i class="bi bi-person-check-fill"></i>&nbsp;
                {{ profileDetails.userFollowing }}&nbsp;Following
              </button>
              <button
                class="btn btn-link text-decoration-none"
                @click="$emit('user-posts')"
                v-if="profileDetails"
              >
                <i class="bi bi-clipboard2-fill"></i>&nbsp;
                {{ profileDetails.userPosts }}&nbsp;Posts
              </button>
              <!-- <button class="btn ms-auto fs-6 fw-bolder">25 Jan 2023</button> -->
              <!-- @click="this.$emit(viewPosts)" -->
            </div>
            <div class="d-flex mx-auto text-center justify-content-center">
              <div class="btn-file">
                <input
                  type="file"
                  style="cursor: pointer"
                  accept=".csv"
                  ref="fileInput"
                  @change="importPosts()"
                />
                <button
                  class="btn btn-link text-decoration-none"
                  v-if="!differentUser"
                  style="cursor: pointer"
                >
                  <i class="bi bi-box-arrow-down-left"></i>&nbsp;&nbsp; Import
                  Blogs
                </button>
              </div>
              <button
                class="btn btn-link text-decoration-none"
                @click="exportPosts()"
                v-if="!differentUser"
              >
                <i class="bi bi-box-arrow-up-right"></i>&nbsp;&nbsp; Export
                Blogs
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
  name: "ProfileComp",

  props: {
    userID: {
      required: true,
    },
  },
  mounted() {
    this.checkUser();
    this.FetchProfile();
  },

  data: function () {
    return {
      followed: null,
      differentUser: false,
      profileData: null,
      follower_count: null,
      dpimage: null,
      user_id: this.userID,
      isEditing: false,
      userName: "",
    };
  },

  methods: {
    exportPosts() {
      var id = this.user_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/export/" + id;

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
          console.log(data);
          var taskID = data.task_id;
          this.checkTaskStatus(taskID);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    checkTaskStatus(taskID) {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/tasks/" + taskID;

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "GET",
        headers: {
          Authorization: auth,
        },
      };

      var pollingInterval = setInterval(() => {
        fetch(url, requestOptions)
          .then((response) => response.blob())
          .then((blob) => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const a = document.createElement("a");
            const timestamp = Date.now();
            const filename = `blogs_${timestamp}.csv`;
            a.href = url;
            a.setAttribute("download", filename);
            a.click();
            clearInterval(pollingInterval);
          });
      }, 1000);
    },

    importPosts() {
      var id = this.user_id;
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/import/" + id;
      // api/profile/import/<int:user_id>
      var file = this.$refs.fileInput.files[0];
      const formData = new FormData();

      formData.append("file", file);

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var requestOptions = {
        method: "POST",
        headers: {
          Authorization: auth,
        },
        body: formData,
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          if (data.msg === "Blogs imported successfully") {
            console.log(data);
          }
          this.$emit("profile-updated");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    startEditing() {
      if (!this.differentUser) {
        this.isEditing = true;
      }
    },
    endEditing() {
      if (!this.differentUser) {
        this.isEditing = false;
        // console.log(this.userName);
        this.changeName();
        // this.$emit("edit", this.editText);
      }
    },
    changeDp(event) {
      var input = event.target;
      if (input.files) {
        this.image = input.files[0];
      }

      if (!this.differentUser) {
        var id = this.user_id;
        var base = this.$store.getters.getBaseURL;
        var url = base + "/api/profile/dp/" + id;
        const formData = new FormData();

        formData.append("image", this.image);

        var token = this.$store.getters.getToken;
        var pureToken = token.replace(/["]+/g, "");
        var auth = `Bearer ${pureToken}`;

        var requestOptions = {
          method: "POST",
          headers: {
            Authorization: auth,
          },
          body: formData,
        };

        fetch(url, requestOptions)
          .then((response) => response.json())
          .then((data) => {
            // console.log(data);
            if (data.msg === "Profile Picture Updated") {
              this.profileData.dp = data.dp;
              this.profileData.dp_mimetype = data.dp_mimetype;
            }
            this.$emit("profile-updated");
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    changeName() {
      if (!this.validName(this.userName)) {
        this.userName = this.profileDetails.userName;
      } else {
        var id = this.user_id;
        var base = this.$store.getters.getBaseURL;
        var url = base + "/api/profile/name/" + id;
        const formData = new FormData();

        formData.append("name", this.userName);

        var token = this.$store.getters.getToken;
        var pureToken = token.replace(/["]+/g, "");
        var auth = `Bearer ${pureToken}`;

        var requestOptions = {
          method: "POST",
          headers: {
            Authorization: auth,
          },
          body: formData,
        };

        fetch(url, requestOptions)
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            this.$emit("profile-updated");
            // if (data.msg === "Name Updated") {

            //   // this.profileData.dp = data.dp;
            //   // this.profileData.dp_mimetype = data.dp_mimetype;
            // }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    validName: function (name) {
      var reg = /^[a-zA-Z ]{2,40}$/;
      // console.log(reg.test(name));
      return reg.test(name);
    },
    toggleFollow() {
      this.followed ? this.UnfollowUser() : this.FollowUser(),
        (this.followed = !this.followed);
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
          this.userName = data.name;
          // console.log(this.userName);
          this.profileData = data;
          // console.log(data);
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
          this.follower_count += 1;
        })
        .catch((error) => {
          console.error(error);
        });
      // this.FetchProfile();
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
          this.follower_count -= 1;
        })
        .catch((error) => {
          console.error(error);
        });
      // this.FetchProfile();
    },
  },

  computed: {
    profileDetails() {
      if (this.profileData) {
        return {
          userName: this.profileData.name,
          dpImageSrc: `data:${this.profileData.dp_mimetype};charset=utf-8;base64,${this.profileData.dp}`,
          userPosts: this.profileData.blog.length,
          // userFollowers: this.profileData.followers_users.length,
          userFollowing: this.profileData.followed_users.length,
          // authorName: this.blogData.user.name,
          // blogUserID: this.blogData.user.id,
        };
      }
      return null;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-height: 300px;
}

.btn-file {
  position: relative;
  overflow: hidden;
}
.btn-file input[type="file"] {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 100%;
  min-height: 100%;
  font-size: 100px;
  text-align: right;
  filter: alpha(opacity=0);
  opacity: 0;
  outline: none;
  cursor: inherit;
  display: block;
}

.editable {
  border: none;
  outline: none;
}
/* .editable :focus {
  outline: none;
  border: none;
} */
/* .editable {
  font-size: 2em;
  border: none;
  font-weight: bold;
  line-height: 1.2;
  margin-top: 1.5em;
  margin-bottom: 0.5em; 

} */

/* .h2-input :focus {
  outline: none;
  border: none;
} */
</style>
