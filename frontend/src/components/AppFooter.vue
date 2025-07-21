<script setup lang="ts">
const currentYear = new Date().getFullYear();
</script>

<template>
  <v-footer app class="pa-0" color="primary" elevation="4">
    <v-container>
      <v-row class="py-6">
        <v-col cols="12" class="text-center">
          <span class="text-white">{{ currentYear }} Testupavois</span>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<style scoped>
.v-footer {
  flex: 0 0 64px;
  width: 100%;
  z-index: 100;
}
</style>
