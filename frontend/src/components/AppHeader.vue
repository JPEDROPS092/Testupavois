<script setup lang="ts">
import ThemeSwitcher from './ThemeSwitcher.vue';

const emit = defineEmits<{
  (e: 'theme-changed', theme: string): void
}>();

const handleThemeChange = (newTheme: string) => {
  emit('theme-changed', newTheme);
};
</script>

<template>
  <v-app-bar
    color="primary"
    app
    elevation="4"
    :height="64"
  >
    <!-- Logo e título da aplicação -->
    <div class="d-flex align-center">
      <v-icon icon="mdi-text-to-speech" size="large" class="mr-2"></v-icon>
      <v-app-bar-title class="text-h5 font-weight-bold">Testupavois</v-app-bar-title>
    </div>

    <v-spacer></v-spacer>

    <!-- Botão de link para o GitHub -->
    <v-btn
      variant="text"
      href="https://github.com/jpedrops092/testupavois"
      target="_blank"
      class="mx-2"
    >
      <v-icon icon="mdi-github" class="mr-2"></v-icon>
      GitHub
    </v-btn>

    <!-- Componente para alternar entre temas claro/escuro -->
    <ThemeSwitcher @theme-changed="handleThemeChange" />
  </v-app-bar>
</template>

<style scoped>
.v-app-bar {
  flex: 0 0 64px;
  width: 100%;
  z-index: 100;
}
</style>
