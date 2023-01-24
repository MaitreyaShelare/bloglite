<template>
  <div class="alertModal">
    <div
      class="modal modal-sheet position-static d-block bg-background py-5"
      tabindex="-1"
      role="dialog"
      id="modalSheet"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content rounded-4 shadow">
          <!-- <div class="modal-header border-bottom-0">
                <h1 class="modal-title fs-5">Add a list</h1>
              </div> -->
          <div class="modal-body py-3">
            <strong>Please login again</strong>
          </div>
          <div class="modal-footer flex-column border-top-0">
            <!-- <button
                type="submit"
                class="btn btn-primary w-100 mx-0 mb-2"
                @click="logout"
              >
                Add
              </button> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertModal",
  methods: {
    logout: function () {
      this.$store.commit("logoutUser"), this.$router.push("/");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.alertModal {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  background-color: #000000b2;
}

.modal {
  min-height: 9rem;
  max-width: 20rem;
}
</style>
