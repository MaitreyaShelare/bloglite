<template>
  <div class="NavBar">
    <nav class="navbar fixed-top bg-white shadow-sm">
      <div class="container">
        <div
          class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
        >
          <div class="container-fluid">
            <a class="navbar-brand h1 text-primary" href="/"> bloglite </a>
          </div>
        </div>
        <div class="text-end">
          <button
            class="btn btn-outline-light text-dark border-white rounded-pill"
            @click="$router.push('/signup')"
          >
            Join now
          </button>
          <button
            class="btn btn-outline-light text-primary border-primary rounded-pill mx-3"
            @click="$router.push('/')"
          >
            Sign in
          </button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-brand {
  padding: 0px;
}
</style>
