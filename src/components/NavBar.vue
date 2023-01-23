<template>
  <div class="NavBar">
    <nav class="navbar fixed-top bg-white shadow-sm">
      <div class="container">
        <div
          class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
        >
          <div class="container-fluid">
            <a class="navbar-brand h1 text-primary" href="/">
              <!-- <svg
                xmlns="http://www.w3.org/2000/svg"
                width="30"
                height="30"
                fill="currentColor"
                class="bi bi-alexa"
                viewBox="0 0 16 16"
              >
                <path
                  d="M7.996 0A7.998 7.998 0 0 0 0 8a8 8 0 0 0 6.93 7.93v-1.613a1.06 1.06 0 0 0-.717-1.008A5.602 5.602 0 0 1 2.4 7.865 5.579 5.579 0 0 1 8.054 2.4a5.599 5.599 0 0 1 5.535 5.81l-.002.046a6.116 6.116 0 0 1-.012.192l-.005.061a4.85 4.85 0 0 1-.033.284l-.01.068c-.685 4.516-6.564 7.054-6.596 7.068A7.998 7.998 0 0 0 15.992 8 7.998 7.998 0 0 0 7.996.001Z"
                />
              </svg> -->
              bloglite
            </a>
          </div>
          <!-- <a class="navbar-brand" href="#">
            <img src="@/assets/icon.png" alt="Logo" width="36" height="36" />
          </a>
          <form>
            <input
              class="form-control search-input bg-light border-light fuzzy-search"
              type="search"
              placeholder="Search"
            />
          </form> -->
        </div>
        <div class="text-end">
          <a
            href="/signup"
            class="btn btn-outline-light text-dark border-white rounded-pill"
          >
            Join now
          </a>
          <a
            href="/"
            class="btn btn-outline-light text-primary border-primary rounded-pill mx-3"
          >
            Sign in
          </a>
        </div>
      </div>
    </nav>
    <!-- <nav class="navbar navbar-light bg-light fixed-top p-2 shadow">
      <div class="container py-0">
        <a class="navbar-brand" href="/">
          <i class="bi bi-bootstrap-fill" style="font-size: 36px"></i>
        </a>
      </div>
    </nav> -->
    <!-- <header class="py-2 mb-3 bg-light border-light border-bottom">
      <div
        class="container-fluid d-grid gap-3 align-items-center"
        style="grid-template-columns: 1fr 2fr"
      >
        <div class="dropdown">
          <a
            href="#"
            class="d-flex align-items-center col-lg-4 mb-lg-0 link-dark"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="40"
              height="32"
              fill="currentColor"
              class="bi bi-bootstrap-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M6.375 7.125V4.658h1.78c.973 0 1.542.457 1.542 1.237 0 .802-.604 1.23-1.764 1.23H6.375zm0 3.762h1.898c1.184 0 1.81-.48 1.81-1.377 0-.885-.65-1.348-1.886-1.348H6.375v2.725z"
              />
              <path
                d="M4.002 0a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4h-8zm1.06 12V3.545h3.399c1.587 0 2.543.809 2.543 2.11 0 .884-.65 1.675-1.483 1.816v.1c1.143.117 1.904.931 1.904 2.033 0 1.488-1.084 2.396-2.888 2.396H5.062z"
              />
            </svg>
          </a>
        </div>

        <div class="d-flex align-items-center">
          <form class="w-100 me-3" role="search">
            <input
              type="search"
              class="form-control"
              placeholder="Search..."
              aria-label="Search"
            />
          </form>

          <div class="flex-shrink-0 dropdown">
            <a
              href="#"
              class="d-block link-dark text-decoration-none"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img
                src="https://github.com/mdo.png"
                alt="mdo"
                width="32"
                height="32"
                class="rounded-circle"
              />
            </a>
            <ul class="dropdown-menu text-small shadow">
              <li><a class="dropdown-item" href="#">New project...</a></li>
              <li><a class="dropdown-item" href="#">Settings</a></li>
              <li><a class="dropdown-item" href="#">Profile</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li><a class="dropdown-item" href="#">Sign out</a></li>
            </ul>
          </div>
        </div>
      </div>
    </header> -->
  </div>
</template>

<script>
export default {
  name: "NavBar",
  // props: {
  //   msg: String,
  // },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-brand {
  padding: 0px;
}

/* .container {
  display: flex;
} */
</style>
