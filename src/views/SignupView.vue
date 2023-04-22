<template>
  <div class="signup">
    <NavBar />
    <SignupHero />
    <FootBar />
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";
import SignupHero from "@/components/SignupHero.vue";
import FootBar from "@/components/FootBar.vue";

export default {
  name: "SignupView",
  components: {
    NavBar,
    SignupHero,
    FootBar,
  },
};
</script>

<style>
.signup {
  height: 100vh;
  width: 100%;
}
</style>
