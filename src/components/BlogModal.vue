<template>
  <div class="blogModal">
    <div
      class="modal modal-sheet position-static d-block bg-background py-5"
      tabindex="-1"
      role="dialog"
      id="modalSheet"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content rounded-4 shadow">
          <div class="modal-header border-bottom-0 mx-auto">
            <h1 class="modal-title fs-5">Edit Blog</h1>
          </div>
          <div class="modal-body py-3">
            <form novalidate="true">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control rounded-3"
                  id="floatingInput"
                  placeholder="List Name"
                  v-model="name"
                  :class="{ 'is-invalid': invalidname }"
                  @click="invalidname = null"
                />
                <label for="floatingInput">List Name</label>
                <div class="invalid-feedback">Please enter a valid name</div>
              </div>
            </form>
          </div>
          <div class="modal-footer flex-column border-top-0">
            <button
              type="submit"
              class="btn btn-primary w-100 mx-0 mb-2"
              @click="checkName"
            >
              Add
            </button>
            <button
              class="btn btn-outline-dark bg border-light w-100 mx-0"
              @click="closeModal"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "listModal",
  props: {
    msg: String,
  },
  data: function () {
    return {
      name: "",
      invalidname: null,
    };
  },
  methods: {
    closeModal: function () {
      this.$emit("close");
    },
    checkName: function (e) {
      if (!this.validName(this.name)) {
        this.invalidname = true;
      }
      if (this.invalidname) {
        e.preventDefault();
      } else {
        this.submitForm();
        this.resetData();
      }
    },
    validName: function (name) {
      var reg = /^[a-zA-Z ]{2,20}$/;
      return reg.test(name);
    },
    resetData: function () {
      this.name = "";
      this.invalidname = null;
    },
    //Change submit form
    async submitForm() {
      var url = "http://127.0.0.1:5000/api/list";
      var form = {
        name: this.name,
      };
      var token = this.$store.getters.getToken;
      var pureToken = token.replace(/["]+/g, "");
      var auth = `Bearer ${pureToken}`;
      // console.log(auth);
      var requestOptions = {
        method: "POST",
        headers: {
          // Authorization: this.$store.getters.getToken,
          "Content-Type": "application/json",
          Authorization: auth,
        },
        body: JSON.stringify(form),
      };
      const response = await fetch(url, requestOptions);
      if (response.status == 201) {
        // console.log("Success");
        // this.$store.commit("ListCRUD");
        this.$emit("created");
        this.closeModal();
      }
      if (response.status == 401) {
        console.log("Failure");
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.blogModal {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  background-color: #000000b2;
}

/* .modal {
  min-height: 9rem;
  max-width: 20rem;
} */
</style>
