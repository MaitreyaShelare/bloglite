<template>
  <div class="searchUser">
    <div class="card-body p-2">
      <div class="mb-3">
        <div class="d-flex align-items-center mb-3">
          <a href="/" class="d-block link-dark text-decoration-none">
            <img
              src="https://github.com/mdo.png"
              alt="mdo"
              width="32"
              height="32"
              class="rounded-circle"
            />
          </a>
          <div class="flex-1">
            <a
              class="fw-bold fs-6 ms-2 mb-0 text-decoration-none text-black"
              href="/"
              >Erza Bridgest</a
            >
          </div>
          <div class="ms-auto">
            <div class="d-flex">
              <button
                class="btn btn-primary mx-auto rounded-pill lh-1"
                type="button"
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
  data: function () {
    return {
      followed: false,
    };
  },

  methods: {
    toggleFollow() {
      this.followed = !this.followed;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
