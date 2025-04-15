<script setup>
import {
  create_user,
  delete_user,
  get_users,
  update_user,
} from "@/services/api";
import { onMounted, ref, shallowRef } from "vue";

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

const users = ref([]);
const search = ref("");
const record = ref(DEFAULT_RECORD);
const select_info = ref(SELECT_INFO);
const dialog = shallowRef(false);
const dialogRemove = shallowRef(false);
const isEditing = shallowRef(false);
const sort = ref();

const headers = [
  { title: "Username", key: "username", align: "start" },
  { title: "Roles", key: "roles" },
  { title: "Timezone", key: "preferences.timezone" },
  { title: "is Active?", key: "active", align: "center" },
  { title: "Last Updated At", key: "updated_ts", align: "center" },
  { title: "Created At", key: "created_ts", align: "center" },

  { title: "Actions", key: "actions", align: "end", sortable: false },
];

const fetch_users = async () => {
  try {
    const response = await get_users();
    if (response.data) {
      users.value = response.data;
    }
  } catch (error) {
    console.log(error);
  }
};

const new_user = async (data) => {
  try {
    const response = await create_user(data);
    if (response.data) {
      console.log(response.data);
      fetch_users();
    }
  } catch (error) {
    console.log(error);
  }
};

const edit_user = async (id, data) => {
  try {
    const response = await update_user(id, data);
    if (response.data) {
      console.log(response.data);
      fetch_users();
    }
  } catch (error) {
    console.log(error);
  }
};

onMounted(() => {
  fetch_users();
});

function add() {
  isEditing.value = false;
  record.value = DEFAULT_RECORD;
  dialog.value = true;
}

function edit(id) {
  isEditing.value = true;

  const found = users.value.find((user) => user._id === id);

  record.value = {
    id: found._id,
    username: found.username,
    password: found.password,
    roles: found.roles,
    active: found.active,
    preferences: { timezone: found.preferences.timezone },
  };

  dialog.value = true;
}

async function remove(id) {
  try {
    const response = await delete_user(id);
    if (response) {
      console.log(response.data);
      fetch_users();
      dialogRemove.value = false;
    }
  } catch (error) {
    console.log(error);
  }
}

function removeUser(id) {
  dialogRemove.value = true;
  record.value = {
    id: id,
  };
}

function save() {
  if (isEditing.value) {
    if (record.value.username.trim() !== "") {
      edit_user(record.value.id, record.value);
      dialog.value = false;
      sort.value = "updated_ts";
    }
  } else {
    if (record.value.username.trim() !== "") {
      new_user(record.value);
      dialog.value = false;
      sort.value = "created_ts";
    }
  }
}
</script>
<template>
  <v-container>
    <v-sheet border rounded>
      <v-data-table
        :headers="headers"
        :hide-default-footer="users.length < 11"
        :items="users"
        :search="search"
        :sort-by="[{ key: sort, order: 'desc' }]"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>
              <v-icon
                color="medium-emphasis"
                icon="mdi-account-box-multiple"
                size="x-small"
                start
              ></v-icon>

              Users List
            </v-toolbar-title>

            <v-text-field
              v-model="search"
              label="Search users"
              hide-details
              clearable
              density="compact"
              prepend-inner-icon="mdi-magnify"
              class="me-2"
              style="max-width: 250px"
            ></v-text-field>

            <v-btn
              class="me-2"
              prepend-icon="mdi-plus"
              rounded="lg"
              text="Add a User"
              border
              @click="add"
            ></v-btn>
          </v-toolbar>
        </template>

        <template v-slot:item.username="{ value, item }">
          <v-chip
            :text="value"
            border="thin opacity-25"
            prepend-icon="mdi-account"
            label
            :to="`/user/${item._id}`"
          >
            <template v-slot:prepend>
              <v-icon color="medium-emphasis"></v-icon>
            </template>
          </v-chip>
        </template>

        <template v-slot:item.roles="{ value }">
          <v-chip
            v-for="role in value"
            :key="role"
            class="me-1"
            size="small"
            color="primary"
            variant="outlined"
          >
            {{ role }}
          </v-chip>
        </template>

        <template v-slot:item.active="{ value }">
          <v-btn variant="plain">
            <v-badge v-if="value" color="success" dot></v-badge>
            <v-badge v-else color="error" dot></v-badge>
          </v-btn>
        </template>

        <template v-slot:item.updated_ts="{ value }">
          <span v-if="value">
            {{ new Date(value * 1000).toLocaleString() }}
          </span>
          <span v-else> - </span>
        </template>

        <template v-slot:item.created_ts="{ value }">
          <span v-if="value">
            {{ new Date(value * 1000).toLocaleString() }}
          </span>
          <span v-else> - </span>
        </template>

        <template v-slot:item.actions="{ item }">
          <div class="d-flex ga-2 justify-end">
            <v-icon
              color="medium-emphasis"
              icon="mdi-pencil"
              size="small"
              @click="edit(item._id)"
            ></v-icon>

            <v-icon
              color="medium-emphasis"
              icon="mdi-delete"
              size="small"
              @click="removeUser(item._id)"
            ></v-icon>
          </div>
        </template>
      </v-data-table>
    </v-sheet>

    <v-dialog v-model="dialog" max-width="500">
      <v-card
        :subtitle="`${
          isEditing ? 'Update' : 'Create'
        } your user to access the system`"
        :title="`${isEditing ? 'Edit' : 'Add'} a User`"
      >
        <template v-slot:text>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="record.username"
                label="Username*"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="record.password"
                label="Password"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12">
              <v-select
                :items="select_info.timezone"
                v-model="record.preferences.timezone"
                label="Timezone"
              >
              </v-select>
            </v-col>

            <v-col cols="12" sm="6">
              <label for="active">Is Active?</label>
              <v-radio-group v-model="record.active" name="active">
                <v-radio label="Active" :value="true"></v-radio>
                <v-radio label="Inactive" :value="false"></v-radio>
              </v-radio-group>
            </v-col>

            <v-col cols="12" md="6">
              <label for="role">Roles</label>
              <v-checkbox
                v-for="(role, index) in select_info.roles"
                :key="index"
                v-model="record.roles"
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
          <v-btn text="Cancel" variant="plain" @click="dialog = false"></v-btn>

          <v-spacer></v-spacer>

          <v-btn text="Save" @click="save"></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogRemove" max-width="500">
      <v-card title="Delete User" text="Are you sure?">
        <v-divider></v-divider>

        <v-card-actions class="bg-surface-light">
          <v-btn
            text="Cancel"
            variant="plain"
            @click="dialogRemove = false"
          ></v-btn>

          <v-spacer></v-spacer>

          <v-btn text="Delete" @click="remove(record.id)"></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
