<template>
  <div class="loginHero">
    <div class="container col-xl-10 col-xxl-8 col-l-6 px-3 py-3">
      <div class="row align-items-center g-lg-5 py-5" style="min-height: 94vh">
        <div
          v-if="data"
          class="alert alert-light alert-dismissible fade show"
          role="alert"
        >
          {{ data.message }}
          <button
            type="button"
            class="btn-close"
            @click="data = null"
            data-bs-dismiss="alert"
            aria-label="Close"
          ></button>
        </div>
        <div class="col-lg-6 align-items-center">
          <h1 class="display-5 fw-bold lh-1 mb-1 mt-1 p-4">
            Welcome to <br />
            Bloglite Community
          </h1>
          <form class="p-6 mx-4 p-md-4 rounded-3">
            <div class="form-floating mb-3">
              <input
                type="email"
                class="form-control"
                id="floatingInput"
                placeholder="name@example.com"
                autocomplete="off"
                v-model="email"
                :class="{ 'is-invalid': invalidemail }"
                @click="invalidemail = null"
              />
              <label for="floatingInput">Email address</label>
              <div class="invalid-feedback">Please enter a valid email</div>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="floatingPassword"
                placeholder="Password"
                autocomplete="off"
                v-model="password"
                :class="{ 'is-invalid': invalidpassword }"
                @click="invalidpassword = null"
              />
              <label for="floatingPassword">Password</label>
              <div class="invalid-feedback">Please enter a valid password</div>
            </div>
            <button
              class="w-100 btn btn-lg btn-primary rounded-pill mt-4"
              type="submit"
              @click="checkForm"
            >
              Sign in
            </button>
            <hr class="my-4" />
            <button
              @click="$router.push('/signup')"
              class="w-100 btn btn-outline-dark btn-lg rounded-pill"
            >
              New Here? Sign up
            </button>
          </form>
        </div>
        <div class="container-fluid col-12 col-sm-6 col-lg-6 mt-5">
          <img
            src="@/assets/login.jpg"
            class="d-block mx-auto img-fluid"
            alt=""
            width="600"
            height="600"
            loading="eager"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginHero",
  data: function () {
    return {
      email: "",
      password: "",
      data: false,
      invalidemail: null,
      invalidpassword: null,
    };
  },
  mounted() {
    if (this.$store.getters.getAuthentication) {
      this.$router.push("/feed");
    }
  },
  methods: {
    checkForm: function (e) {
      if (!this.validEmail(this.email)) {
        this.invalidemail = true;
      }

      if (!this.validPassword(this.password)) {
        this.invalidpassword = true;
      }

      if (this.invalidemail || this.invalidpassword) {
        e.preventDefault();
      } else {
        this.submitForm();
        this.resetData();
      }
    },
    validEmail: function (email) {
      var reg =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return reg.test(email);
    },
    validPassword: function (password) {
      var reg = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
      return reg.test(password);
    },
    resetData: function () {
      this.email = "";
      this.password = "";
      this.invalidemail = null;
      this.invalidpassword = null;
    },
    submitForm: function () {
      var base = this.$store.getters.getBaseURL;
      var url = base + "/api/login";
      var form = {
        email: this.email,
        password: this.password,
      };
      // console.log(form);
      var requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      };
      fetch(url, requestOptions)
        .then((response) => {
          if (response.status !== 201) {
            return response.json().then((data) => {
              this.data = data;
            });
          } else {
            return response.json().then((data) => {
              this.data = data;
              this.$store.commit("loginUser");
              this.$store.commit("setCurrentUserID", data.id);
              this.$store.commit("setToken", data.access_token);
              this.$store.commit("setRefreshToken", data.refresh_token);
              this.$router.push("/feed");
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
