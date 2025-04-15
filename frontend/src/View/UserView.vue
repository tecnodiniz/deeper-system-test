<script setup>
import { get_user, update_user, delete_user } from "@/services/api";
import { onMounted, ref, shallowRef } from "vue";
import { useRoute, useRouter } from "vue-router";

const snackbar = ref(false);
const text = ref("");
const timeout = ref(2000);
const color = ref("");

const SELECT_INFO = {
  roles: ["admin", "manager", "tester"],
  timezone: ref(Intl.supportedValuesOf("timeZone")),
};

const DEFAULT_RECORD = {
  username: "",
  password: "",
  roles: [],
  active: true,
  preferences: { timezone: "" },
};

const route = useRoute();
const router = useRouter();
const user = ref(DEFAULT_RECORD);
const select_info = ref(SELECT_INFO);
const username = ref();
const dialog = shallowRef(false);

const fetch_user = async (id) => {
  try {
    const response = await get_user(id);
    if (response.data) {
      user.value = response.data;
      username.value = user.value.username;
    }
  } catch (error) {
    console.log(error);
  }
};

async function save() {
  if (user.value.username.trim() !== "") {
    try {
      const { _id, ...payload } = user.value;

      const response = await update_user(_id, payload);
      if (response.data) {
        text.value = response.data.message;
        snackbar.value = true;
        color.value = "green";
        fetch_user(_id);
      }
    } catch (error) {
      console.log(error);
    }
  } else {
    text.value = "Username field is required.";
    snackbar.value = true;
    color.value = "red";
  }
}
async function remove(id) {
  try {
    const response = await delete_user(id);
    if (response.data) {
      router.push("/");
    }
  } catch (error) {
    console.log(error);
  }
}
onMounted(() => {
  fetch_user(route.params.id);
});
</script>

<template>
  <v-card subtitle="User's Information">
    <template v-slot:title>
      <div class="d-flex align-center justify-space-between w-100">
        <span>User {{ username }}</span>
        <v-btn
          icon
          variant="text"
          @click="router.push('/')"
          title="Back to Home"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
    </template>
    <template v-slot:text>
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="user.username"
            label="Username*"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-text-field v-model="user.password" label="Password"></v-text-field>
        </v-col>

        <v-col cols="12" sm="12">
          <v-select
            :items="select_info.timezone"
            v-model="user.preferences.timezone"
            label="Timezone"
          >
          </v-select>
        </v-col>

        <v-col cols="12" sm="6">
          <v-radio-group v-model="user.active" name="active" label="Is Active?">
            <v-radio label="Active" :value="true"></v-radio>
            <v-radio label="Inactive" :value="false"></v-radio>
          </v-radio-group>
        </v-col>

        <v-col cols="12" md="6">
          Roles
          <v-checkbox
            v-for="(role, index) in select_info.roles"
            :key="index"
            v-model="user.roles"
            :value="role"
            :label="role"
            required
            density="compact"
            hide-details
          >
          </v-checkbox>
        </v-col>
      </v-row>
    </template>

    <v-divider></v-divider>

    <v-card-actions class="bg-surface-light">
      <v-btn text="DELETE" variant="plain" @click="dialog = true"></v-btn>

      <v-spacer></v-spacer>

      <v-btn text="Update" @click="save"></v-btn>
    </v-card-actions>
  </v-card>

  <v-dialog v-model="dialog" max-width="500">
    <v-card title="Delete User" text="Are you sure?">
      <v-divider></v-divider>

      <v-card-actions class="bg-surface-light">
        <v-btn text="Cancel" variant="plain" @click="dialog = false"></v-btn>

        <v-spacer></v-spacer>

        <v-btn text="Delete" @click="remove(user._id)"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar
    v-model="snackbar"
    :timeout="timeout"
    location="right"
    :color="color"
  >
    {{ text }}

    <template v-slot:actions>
      <v-btn variant="text" @click="snackbar = false"> Close </v-btn>
    </template>
  </v-snackbar>
</template>
