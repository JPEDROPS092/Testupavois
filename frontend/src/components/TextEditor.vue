<template>
  <div class="text-editor">
    <v-card flat>
      <v-card-text>
        <v-textarea
          v-model="text"
          label="Enter text to convert to speech"
          placeholder="Type or paste your text here..."
          rows="6"
          auto-grow
          counter
          variant="outlined"
          class="mb-4"
        ></v-textarea>

        <div class="d-flex align-center mb-4">
          <v-slider
            v-model="speed"
            label="Speech Speed"
            min="0.5"
            max="2"
            step="0.1"
            thumb-label
            class="mr-4"
          ></v-slider>

          <v-slider
            v-model="pitch"
            label="Voice Pitch"
            min="-10"
            max="10"
            step="1"
            thumb-label
            class="ml-4"
          ></v-slider>
        </div>

        <div class="text-center">
          <v-btn
            color="primary"
            size="large"
            :loading="isConverting"
            :disabled="!text"
            @click="convertToSpeech"
            class="px-8"
          >
            <v-icon start>mdi-text-to-speech</v-icon>
            Convert to Speech
          </v-btn>
        </div>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mt-4"
        >
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'

const text = ref('')
const speed = ref(1)
const pitch = ref(0)
const isConverting = ref(false)
const error = ref('')

const props = defineProps({
  voiceSettings: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['text-processed', 'audioGenerated'])

const handleTextChange = () => {
  error.value = ''
}

const convertToSpeech = async () => {
  if (!text.value) return
  
  if (!text.value || !props.voiceSettings.modelId) return

  isProcessing.value = true
  error.value = ''

  try {
    const response = await axios.post('/api/tts', {
      text: text.value,
      ...props.voiceSettings
    })

    emit('text-processed', response.data)
  } catch (err) {
    error.value = 'Error processing text. Please try again.'
    console.error('Processing error:', err)
  } finally {
    isProcessing.value = false
  }
}
</script>
