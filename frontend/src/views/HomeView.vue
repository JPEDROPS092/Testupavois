<script setup lang="ts">
import { ref } from 'vue'
import VoiceSelector from '../components/VoiceSelector.vue'
import DocumentUploader from '../components/DocumentUploader.vue'
import TextEditor from '../components/TextEditor.vue'
import AudioPlayer from '../components/AudioPlayer.vue'

const voiceSettings = ref({
  language: '',
  modelId: '',
  speed: 1.0,
  speakerId: 0
})

const audioPath = ref('')

const handleTextProcessed = (data: { audio_path: string }) => {
  audioPath.value = data.audio_path
}

const handleFileUploaded = (data: { file_path: string }) => {
  // Handle uploaded file
  console.log('File uploaded:', data.file_path)
}
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <h2 class="text-h4 mb-4">Text to Speech Converter</h2>
        <VoiceSelector
          @update:settings="(settings) => voiceSettings = settings"
          class="mb-4"
        />
        <DocumentUploader
          @file-uploaded="handleFileUploaded"
          class="mb-4"
        />
        <TextEditor
          :voice-settings="voiceSettings"
          @text-processed="handleTextProcessed"
        />
      </v-col>
      
      <v-col cols="12" md="6">
        <AudioPlayer
          :audio-path="audioPath"
          class="mt-4"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
