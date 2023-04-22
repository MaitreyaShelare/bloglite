<template>
  <div class="foot">
    <div class="container">
      <footer
        class="d-flex flex-wrap justify-content-between align-items-center py-3 mt-3 border-top"
      >
        <div class="col-md-4 d-flex align-items-center">
          <a href="#" class="mb-3 me-2 mb-md-0 lh-1">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-alexa"
              viewBox="0 0 16 16"
            >
              <path
                d="M7.996 0A7.998 7.998 0 0 0 0 8a8 8 0 0 0 6.93 7.93v-1.613a1.06 1.06 0 0 0-.717-1.008A5.602 5.602 0 0 1 2.4 7.865 5.579 5.579 0 0 1 8.054 2.4a5.599 5.599 0 0 1 5.535 5.81l-.002.046a6.116 6.116 0 0 1-.012.192l-.005.061a4.85 4.85 0 0 1-.033.284l-.01.068c-.685 4.516-6.564 7.054-6.596 7.068A7.998 7.998 0 0 0 15.992 8 7.998 7.998 0 0 0 7.996.001Z"
              />
            </svg>
          </a>
        </div>
        <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
          <li class="ms-3">
            <span class="mb-3 mb-md-0 text-muted"
              >&copy; 2023 Bloglite, Inc</span
            >
          </li>
        </ul>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: "FootBar",
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
