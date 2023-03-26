<template>
  <div class="searchview">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-3">
        <div class="form mb-4 d-sm-none d-xl-block">
          <input
            class="form-control"
            type="text"
            placeholder="Find your friends"
            v-model="name"
            :class="{ 'is-invalid': invalidname }"
            @click="invalidname = null"
          />
          <div class="invalid-feedback">Please enter a valid name</div>
        </div>
        <div class="d-flex">
          <button
            class="btn btn-primary mx-auto rounded-pill lh-1"
            type="button"
            @click="checkName"
          >
            <i class="bi bi-search"></i>
            &nbsp;Search
          </button>
        </div>
        <div class="follow pt-5" v-if="noUsers">
          <div class="container">
            <div class="col mx-auto mt-2">
              <div class="card mb-4 overflow-hidden">
                <div class="card-body p-3 p-sm-4">
                  <h3 class="text-center">No Such User Found</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card mt-4 mb-4 overflow-hidden" v-if="showResults">
          <div class="card-body p-3 p-sm-4">
            <div class="users py-1" v-for="user in users" :key="user">
              <SearchUsers :userID="user" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchUsers from "@/components/SearchUsers.vue";
export default {
  name: "SearchComp",
  components: {
    SearchUsers,
  },
  data: function () {
    return {
      users: [],
      showResults: false,
      noUsers: null,
      invalidname: null,
      name: "",
    };
  },
  mounted() {
    if (!this.$store.getters.getAuthentication) {
      this.$router.push("/");
    }
  },

  methods: {
    checkName() {
      this.noUsers = null;
      if (!this.validName(this.name)) {
        this.invalidname = true;
      } else {
        this.userSearch();
      }
    },
    validName: function (name) {
      var reg = /^[a-zA-Z ]{2,40}$/;
      // console.log(reg.test(name));
      return reg.test(name);
    },
    userSearch() {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/profile/search";

      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;

      var form = {
        name: this.name,
      };

      var requestOptions = {
        method: "POST",
        headers: {
          Authorization: auth,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      };

      fetch(url, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          this.users = data;
          console.log(this.users);
          if (this.users.length == 0) {
            this.noUsers = true;
            this.showResults = false;
          } else {
            this.showResults = true;
          }
        });
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
}

.form-control {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  height: 55px;
}

.btn {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
