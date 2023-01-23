<template>
  <div class="signupHero">
    <div class="container col-xl-10 col-xxl-8 col-l-6 px-3 py-3">
      <div
        class="row flex-lg-row-reverse align-items-center g-lg-2 py-5"
        style="min-height: 90vh"
      >
        <div
          v-if="data"
          class="alert alert-warning alert-dismissible fade show"
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
            Join now to connect with the world
          </h1>
          <div class="col-md-10 mx-auto">
            <form
              id="signup-form"
              novalidate="true"
              class="p-4 p-md-4 rounded-3 needs-validation"
            >
              <div class="form-floating mb-3">
                <input
                  type="text"
                  class="form-control"
                  id="floatingName"
                  placeholder="name"
                  v-model="name"
                  :class="{ 'is-invalid': invalidname }"
                  @click="invalidname = null"
                />
                <label for="floatingName">Name</label>
                <div class="invalid-feedback">Please enter a valid name</div>
              </div>
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  id="floatingInput"
                  placeholder="name@example.com"
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
                  v-model="password"
                  :class="{ 'is-invalid': invalidpassword }"
                  @click="invalidpassword = null"
                />
                <label for="floatingPassword">Password</label>
                <div class="invalid-feedback">
                  Please enter a valid password
                </div>
              </div>
              <button
                type="submit"
                @click="checkForm"
                class="w-100 btn btn-lg btn-primary rounded-pill mb-3"
              >
                Join
              </button>
              <!-- <p>
                Already have an Account?
                <router-link to="/">Sign in</router-link>
              </p> -->
            </form>
            <!-- <p>{{ data.message }}</p> -->
          </div>
        </div>
        <div class="container-fluid col-12 col-sm-8 col-lg-6">
          <img
            src="@/assets/signup.jpg"
            class="d-block mx-auto img-fluid"
            width="700"
            height="700"
            loading="eager"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupHero",
  data: function () {
    return {
      name: "",
      email: "",
      password: "",
      data: false,
      invalidname: null,
      invalidemail: null,
      invalidpassword: null,
    };
  },
  mounted() {
    if (this.$store.getters.getAuthentication) {
      this.$router.push("/home");
    }
  },
  methods: {
    checkForm: function (e) {
      if (!this.validName(this.name)) {
        this.invalidname = true;
      }

      if (!this.validEmail(this.email)) {
        this.invalidemail = true;
      }

      if (!this.validPassword(this.password)) {
        this.invalidpassword = true;
      }

      if (this.invalidname || this.invalidemail || this.invalidpassword) {
        e.preventDefault();
      } else {
        this.submitForm();
        this.resetData();
      }
    },
    validName: function (name) {
      var reg = /^[a-zA-Z ]{2,40}$/;
      return reg.test(name);
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
      this.name = "";
      this.email = "";
      this.password = "";
      this.invalidname = null;
      this.invalidemail = null;
      this.invalidpassword = null;
    },
    submitForm: function () {
      var url = "http://127.0.0.1:5000/api/signup";
      var form = {
        name: this.name,
        email: this.email,
        password: this.password,
      };
      //console.log(form);
      var requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      };
      fetch(url, requestOptions)
        .then((response) => {
          if (response.status == 201) {
            this.$store.commit("loginUser"), this.$router.push("/home");
          }
          return response.json();
        })
        .then((data) => {
          (this.data = data),
            this.$store.commit("setToken", JSON.stringify(data.access_token));
        });
      // .then((v) => console.log(v));
      // fetch(url, requestOptions)
      //   .then((response) => JSON.parse(response))
      //   .then((data) => console.log(data));
      // if (data.message == "User added sucessfully") {
      //   this.$router.push("/about");
      // }
      // if (response.status == 201) {
      //       this.$router.push("/about");
      //     }
    },
  },
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
