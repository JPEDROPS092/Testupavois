<template>
  <div class="voice-selector">
    <v-card flat>
      <v-card-text>
        <v-select
          v-model="selectedLanguage"
          :items="languages"
          label="Select Language"
          variant="outlined"
          prepend-icon="mdi-translate"
          class="mb-4"
        ></v-select>

        <v-select
          v-model="selectedModel"
          :items="availableModels"
          label="Select Voice Model"
          variant="outlined"
          :disabled="!selectedLanguage"
          prepend-icon="mdi-account-voice"
          class="mb-4"
        ></v-select>

        <v-select
          v-model="speakerId"
          :items="speakers"
          label="Select Speaker"
          variant="outlined"
          :disabled="!selectedModel"
          prepend-icon="mdi-account"
          class="mb-4"
        ></v-select>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <v-chip
          v-if="selectedLanguage && selectedModel"
          color="primary"
          class="ma-2"
        >
          <v-icon start>mdi-check</v-icon>
          Voice Selected
        </v-chip>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'

const selectedLanguage = ref('')
const selectedModel = ref('')
const selectedSpeaker = ref('')
const speed = ref(1.0)
const speakerId = ref(0)
const maxSpeakerId = ref(0)
const languages = ref([])
const availableModels = ref([])
const speakers = ref([])
const error = ref('')

const emit = defineEmits(['update:settings'])

const fetchLanguages = async () => {
  try {
    const response = await axios.get('/api/languages')
    languages.value = response.data.map((lang: string) => ({
      title: lang,
      value: lang
    }))
  } catch (err) {
    error.value = 'Failed to load languages'
    console.error('Error fetching languages:', err)
  }
}

const fetchModels = async (language: string) => {
  try {
    const response = await axios.get(`/api/models/${language}`)
    availableModels.value = response.data.models.map((model: any) => ({
      title: model.name,
      value: model.id
    }))
  } catch (err) {
    error.value = 'Failed to load voice models'
    console.error('Error fetching models:', err)
  }
}

const fetchSpeakers = async (modelId: string) => {
  try {
    const response = await axios.get(`/api/speakers/${modelId}`)
    speakers.value = response.data.speakers.map((id: number) => ({
      title: `Speaker ${id}`,
      value: id
    }))
  } catch (err) {
    error.value = 'Failed to load speakers'
    console.error('Error fetching speakers:', err)
  }
}

watch(selectedLanguage, async (newLang) => {
  if (newLang) {
    selectedModel.value = ''
    selectedSpeaker.value = ''
    await fetchModels(newLang)
  }
})

watch(selectedModel, async (newModel) => {
  if (newModel) {
    selectedSpeaker.value = ''
    await fetchSpeakers(newModel)
  }
})

watch([selectedLanguage, selectedModel, speed, speakerId], () => {
  emit('update:settings', {
    language: selectedLanguage.value,
    modelId: selectedModel.value,
    speed: speed.value,
    speakerId: speakerId.value
  })
})

// Fetch languages on component mount
fetchLanguages()
</script>
