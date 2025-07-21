<template>
  <v-app :theme="theme">
    <AppHeader @theme-changed="handleThemeChange" />
    
    <v-main class="main-content">
      <router-view></router-view>
    </v-main>

    <AppFooter />
  </v-app>
</template>

<script setup lang="ts">
/**
 * Importação das dependências necessárias:
 * - ref: Para criar variáveis reativas
 * - useTheme: Hook do Vuetify para gerenciar temas
 * - ThemeSwitcher: Componente personalizado para alternar temas
 */
import { ref } from 'vue';
import { useTheme } from 'vuetify';
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';

/**
 * Configuração do tema:
 * - vuetifyTheme: Instance do tema do Vuetify
 * - theme: Variável reativa que controla o tema atual ('light' ou 'dark')
 */
const vuetifyTheme = useTheme();
const theme = ref('light');

/**
 * Handler para mudança de tema
 * @param newTheme - Nova configuração de tema ('light' ou 'dark')
 * Atualiza tanto a variável local quanto o tema global do Vuetify
 */
const handleThemeChange = (newTheme: string) => {
  theme.value = newTheme;
  vuetifyTheme.global.name.value = newTheme;
};
</script>

<style>
/* Reset global */
:root {
  --app-background: rgb(var(--v-theme-background));
}

.v-application {
  background-color: var(--app-background) !important;
}

.v-main {
  background-color: var(--app-background) !important;
}

.v-application__wrap {
  background-color: var(--app-background) !important;
  min-height: 100vh !important;
  display: flex;
  flex-direction: column;
}

/* Layout principal */
.v-main__wrap {
  display: flex;
  width: 100%;
  min-height: calc(100vh - 128px);
  background-color: var(--app-background) !important;
}

/* Containers e grid */
.v-container {
  max-width: none !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}

.v-row {
  margin: 0 !important;
  padding: 0 !important;
}

.v-col {
  padding: 1rem !important;
}
</style>