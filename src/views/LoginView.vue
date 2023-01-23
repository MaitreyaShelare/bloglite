<template>
  <div class="login">
    <NavBar />
    <LoginHero />
    <FootBar />
    <!-- <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Login View" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";
import LoginHero from "@/components/LoginHero.vue";
import FootBar from "@/components/FootBar.vue";
export default {
  name: "LoginView",
  components: {
    NavBar,
    LoginHero,
    FootBar,
  },
};
</script>
<style>
.login {
  height: 100vh;
  width: 100%;
}
</style>
