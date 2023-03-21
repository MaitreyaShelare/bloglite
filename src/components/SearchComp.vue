<template>
  <div class="searchview">
    <div class="container">
      <div class="col col-md-6 mx-auto mt-3">
        <div class="form mb-4 d-sm-none d-xl-block">
          <input
            class="form-control"
            type="text"
            placeholder="Find your friends"
          />
        </div>
        <div class="d-flex">
          <button
            class="btn btn-primary mx-auto rounded-pill lh-1"
            type="button"
            @click="userSearch"
          >
            <i class="bi bi-search"></i>
            &nbsp;Search
          </button>
        </div>
        <div class="card mb-4 mt-4 overflow-hidden">
          <SearchUsers />
          <SearchUsers />
          <SearchUsers />
          <SearchUsers />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchUsers from "@/components/SearchUsers.vue";
export default {
  name: "SearchComp",
  components: {
    SearchUsers,
  },
  data: function () {
    return {
      followed: false,
    };
  },

  methods: {
    toggleFollow() {
      this.followed = !this.followed;
    },
    userSearch() {
      console.log("searching");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.form-control {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.btn {
  border: 1px solid #e5e5e5;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
