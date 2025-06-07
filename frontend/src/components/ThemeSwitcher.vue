<template>
  <v-btn
    icon
    @click="toggleTheme"
    :color="isDarkMode ? 'amber' : 'indigo'"
  >
    <v-icon v-if="!isDarkMode">mdi-moon-waxing-crescent</v-icon>
    <v-icon v-else>mdi-white-balance-sunny</v-icon>
  </v-btn>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTheme } from 'vuetify'

const theme = useTheme()
const emit = defineEmits(['theme-changed'])
const isDarkMode = ref(false)

onMounted(() => {
  // Check if theme is already dark from system preference
  if (theme.global.current.value.dark) {
    isDarkMode.value = true
  }
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  theme.global.name.value = isDarkMode.value ? 'dark' : 'light'
  emit('theme-changed', isDarkMode.value ? 'dark' : 'light')
}
</script>
