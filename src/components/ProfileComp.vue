<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="d-flex justify-content-center">
              <img
                src="https://github.com/mdo.png"
                width="180"
                height="180"
                class="rounded-circle bg-white img-thumbnail shadow-sm"
              />
            </div>
            <div class="d-flex">
              <h2 class="mx-auto py-2">Erza Bridgest</h2>
            </div>
            <div class="row">
              <button
                class="btn btn-primary mx-auto rounded-pill w-25 lh-1"
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
              <!-- <button
                class="btn mx-auto btn-link p-0 me-3 fs-6 fw-bolder text-decoration-none"
                type="button"
                @click="toggleLike"
              >
                <i
                  :class="{
                    'bi bi-hand-thumbs-up': !liked,
                    'bi bi-hand-thumbs-up-fill': liked,
                  }"
                ></i
                >&nbsp;Like
              </button> -->
            </div>

            <!-- <div class="d-flex">
              <button
                class="btn btn-link float-start p-0 me-3 fs-6 fw-bolder text-decoration-none"
                type="button"
                @click="toggleLike"
              >
                <i
                  :class="{
                    'bi bi-hand-thumbs-up': !liked,
                    'bi bi-hand-thumbs-up-fill': liked,
                  }"
                ></i
                >&nbsp;Like
              </button>
              <button
                class="btn btn-link link-dark p-0 me-3 fs-6 fw-bolder text-decoration-none"
                type="button"
                @click="toggleComments"
              >
                <i
                  :class="{
                    'bi bi-chat': !showComments,
                    'bi bi-chat-fill': showComments,
                  }"
                ></i
                >&nbsp;Comment
              </button>
              <button class="btn ms-auto fs-6 fw-bolder">25 Jan 2023</button>
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileComp",
  data: function () {
    return {
      showComments: false,
      followed: false,
    };
  },

  methods: {
    toggleComments() {
      this.showComments = !this.showComments;
    },
    toggleFollow() {
      this.followed = !this.followed;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  min-height: 300px;
}
</style>
