<script setup lang="ts">
/**
 * Importa o helper `ref` para criar variáveis reativas
 * e os componentes que serão usados nesta view.
 */
import { ref } from 'vue'
import VoiceSelector from '../components/VoiceSelector.vue'
import DocumentUploader from '../components/DocumentUploader.vue'
import TextEditor from '../components/TextEditor.vue'
import AudioPlayer from '../components/AudioPlayer.vue'

/**
 * Objeto reativo que guarda as configurações de voz escolhidas pelo usuário:
 * - language: código do idioma (ex.: "pt-BR")
 * - modelId: identificador do modelo de TTS
 * - speed: velocidade da fala (1.0 = normal)
 * - speakerId: identificador do locutor
 */
const voiceSettings = ref<{ language: string; modelId: string; speed: number; speakerId: number }>({
  language: '',
  modelId: '',
  speed: 1.0,
  speakerId: 0
})

/**
 * Variável reativa que armazenará o caminho do arquivo de áudio
 * gerado após a conversão de texto para fala.
 */
const audioPath = ref<string>('')

/**
 * Handler acionado pelo componente TextEditor quando
 * o texto é processado e o áudio é gerado pelo backend.
 * Atualiza `audioPath` com o caminho retornado.
 */
const handleTextProcessed = (data: { audio_path: string }) => {
  audioPath.value = data.audio_path
}

/**
 * Handler acionado pelo componente DocumentUploader
 * após o upload de um arquivo. Por enquanto apenas loga
 * o caminho do arquivo no console.
 */
const handleFileUploaded = (data: { file_path: string }) => {
  console.log('File uploaded:', data.file_path)
}
</script>

<template>
  <div class="home-view">
    <v-row class="fill-height ma-0">
      <!-- Coluna esquerda com controles -->
      <v-col cols="12" md="6" class="pa-6">
        <v-card elevation="0" class="h-100">
          <v-card-title class="text-h4 mb-6">Text to Speech Converter</v-card-title>
          
          <v-card-text class="pa-0">
            <VoiceSelector
              @update:settings="(settings) => voiceSettings.value = settings"
              class="mb-6"
            />
            
            <DocumentUploader
              @file-uploaded="handleFileUploaded"
              class="mb-6"
            />
            
            <TextEditor
              :voice-settings="voiceSettings"
              @text-processed="handleTextProcessed"
              class="flex-grow-1"
            />
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Coluna direita com player de áudio -->
      <v-col cols="12" md="6" class="pa-6">
        <v-card elevation="0" class="h-100">
          <AudioPlayer
            :audio-path="audioPath"
            class="flex-grow-1"
          />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.home-view {
  width: 100%;
  height: 100%;
  display: flex;
  background: rgb(var(--v-theme-background));
}

.v-row {
  width: 100%;
  margin: 0 !important;
}

.v-col {
  display: flex;
  padding: 1rem !important;
  background: rgb(var(--v-theme-background));
}

.v-card {
  width: 100%;
  background: transparent !important;
  border: none !important;
}

.v-card-title {
  padding: 1rem;
}

.v-card-text {
  padding: 1rem !important;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.text-editor,
.audio-player {
  flex: 1;
  min-height: 400px;
  background: rgb(var(--v-theme-surface));
  border-radius: 8px;
}

:deep(.v-sheet) {
  background: transparent !important;
}

:deep(.v-card-text > *) {
  margin-bottom: 1rem;
}

:deep(.v-input) {
  background: rgb(var(--v-theme-surface));
  border-radius: 8px;
  padding: 0.5rem;
}
</style>
