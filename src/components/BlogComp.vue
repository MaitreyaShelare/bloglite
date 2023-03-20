<template>
  <div class="blog">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-2">
        <div class="card mb-4 overflow-hidden">
          <div class="card-body p-3 p-sm-4">
            <div class="border-bottom mb-3">
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
                  <button
                    type="button"
                    class="btn btn-sm float-end"
                    data-bs-toggle="dropdown"
                  >
                    <i class="bi bi-three-dots"></i>
                  </button>
                  <ul class="dropdown-menu">
                    <li><button class="dropdown-item">Edit</button></li>
                    <li>
                      <button class="dropdown-item">Delete</button>
                    </li>
                    <li><button class="dropdown-item">Export</button></li>
                  </ul>
                </div>
              </div>
              <p class="text-800">
                Hello, it's really a pain to be followed. Those who praise,
                however, are spurned by the necessities from which they are to
                assume the comforts of forgiveness, because unless they flee
                less from the consequences, they do not know which one will find
                the pleasure of happiness.
              </p>
              <div class="row g-1 mb-5">
                <div class="mx-auto">
                  <img
                    class="rounded h-100 w-100"
                    src="https://github.com/mdo.png"
                    alt="..."
                  />
                </div>
              </div>
            </div>
            <div class="d-flex">
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
                <!-- <i class="bi bi-hand-thumbs-up"></i>&nbsp;Like -->
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
                <!-- <i class="bi bi-chat"></i>&nbsp;Comment -->
              </button>
              <button class="btn ms-auto fs-6 fw-bolder">25 Jan 2023</button>
            </div>
          </div>
          <div class="bg-light border-top p-3 p-sm-4" v-if="showComments">
            <div class="d-flex align-items-start">
              <div class="me-2">
                <img
                  src="https://github.com/mdo.png"
                  alt="mdo"
                  width="32"
                  height="32"
                  class="rounded-circle"
                />
              </div>
              <div class="flex-1">
                <div class="d-flex align-items-center">
                  <a
                    class="fw-bold mb-0 text-decoration-none text-black"
                    href="#!"
                    >Mamur Fechetti</a
                  ><span class="text-600 fw-semi-bold fs--2 ms-2"
                    >35 mins ago</span
                  >
                </div>
                <p class="mb-0">
                  How long did it take to create this? It appears that you
                  quickly produced the second one.
                </p>
                <button
                  class="btn btn-link p-0 text-900 text-decoration-none fw-bolder mb-2"
                  type="button"
                ></button>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="me-2">
                <img
                  src="https://github.com/mdo.png"
                  alt="mdo"
                  width="32"
                  height="32"
                  class="rounded-circle"
                />
              </div>
              <div class="flex-1 w-100">
                <input
                  class="form-control"
                  type="text"
                  placeholder="Add comment"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogComp",
  data: function () {
    return {
      showComments: false,
      liked: false,
    };
  },

  methods: {
    toggleComments() {
      this.showComments = !this.showComments;
    },
    toggleLike() {
      this.liked = !this.liked;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  min-height: 200px;
}
</style>
