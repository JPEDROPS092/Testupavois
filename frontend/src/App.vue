<template>
  <v-app :theme="theme">
    <!-- App Bar -->
    <v-app-bar
      color="primary"
      app
      elevation="4"
      :height="64"
    >
      <div class="d-flex align-center">
        <v-icon icon="mdi-text-to-speech" size="large" class="mr-2"></v-icon>
        <v-app-bar-title class="text-h5 font-weight-bold">Testupavois</v-app-bar-title>
      </div>
      <v-spacer></v-spacer>
      <v-btn
        variant="text"
        href="https://github.com/k2-fsa/sherpa-onnx"
        target="_blank"
        class="mx-2"
      >
        <v-icon icon="mdi-github" class="mr-2"></v-icon>
        GitHub
      </v-btn>
      <ThemeSwitcher @theme-changed="handleThemeChange" />
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="bg-background">
      <v-container fluid class="fill-height pa-0">
        <!-- Hero Section -->
        <v-row class="hero-section ma-0 pa-0" justify="center">
          <v-col cols="12" class="pa-0">
            <v-sheet
              color="primary"
              class="py-10 px-4"
              rounded="0"
            >
              <v-container>
                <v-row align="center" justify="center">
                  <v-col cols="12" md="6" lg="5" class="text-center text-md-left">
                    <h1 class="text-h2 font-weight-bold text-white mb-4">Transforme Texto em Fala</h1>
                    <p class="text-subtitle-1 text-white mb-6">Utilize nossa tecnologia avançada de síntese de voz para converter texto em áudio natural em diversos idiomas. Agora com suporte para processamento de documentos!</p>
                    <v-btn
                      size="large"
                      color="white"
                      variant="elevated"
                      class="text-primary font-weight-bold"
                      @click="scrollToTTS"
                    >
                      <v-icon icon="mdi-play" class="mr-2"></v-icon>
                      Começar
                    </v-btn>
                  </v-col>
                  <v-col cols="12" md="6" lg="5" class="d-flex justify-center align-center">
                    <v-sheet
                      width="300"
                      height="300"
                      color="transparent"
                      class="d-flex justify-center align-center position-relative"
                    >
                      <div class="pulse-circle"></div>
                      <v-avatar
                        size="200"
                        color="white"
                        class="elevation-10"
                      >
                        <v-icon
                          size="100"
                          color="primary"
                          icon="mdi-waveform"
                        ></v-icon>
                      </v-avatar>
                    </v-sheet>
                  </v-col>
                </v-row>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>

        <!-- Main TTS Section -->
        <v-row class="ma-0 pa-0" justify="center">
          <v-col cols="12" class="pa-0">
            <v-sheet class="py-10">
              <v-container>
                <v-row justify="center">
                  <v-col cols="12" md="10" lg="8">
                    <v-card ref="ttsSection" class="elevation-3 rounded-lg overflow-hidden">
                      <v-card-title class="text-h5 font-weight-bold bg-primary text-white py-4">
                        Conversor de Texto para Fala
                      </v-card-title>
                      
                      <v-row class="ma-0 pa-0">
                        <v-col cols="12" class="pa-0">
                          <v-tabs
                            v-model="activeTab"
                            bg-color="primary"
                            center-active
                            slider-color="white"
                            class="elevation-2"
                          >
                            <v-tab value="tts" class="text-white">
                              <v-icon icon="mdi-text-to-speech" class="mr-2"></v-icon>
                              Texto para Voz
                            </v-tab>
                            <v-tab value="document" class="text-white">
                              <v-icon icon="mdi-file-document-outline" class="mr-2"></v-icon>
                              Processar Documento
                            </v-tab>
                          </v-tabs>
                        </v-col>
                      </v-row>

                      <v-card-text class="pa-6">
                        <v-window v-model="activeTab">
                          <!-- TTS Tab -->
                          <v-window-item value="tts">
                            <v-form @submit.prevent="handleFormSubmit" class="tts-form">
                              <v-row>
                                <v-col cols="12">
                                  <v-alert
                                    type="info"
                                    variant="tonal"
                                    icon="mdi-information-outline"
                                    class="mb-4"
                                  >
                                    Digite ou cole o texto que deseja converter em áudio. Selecione o idioma e o modelo de voz desejados.
                                  </v-alert>
                                </v-col>
                              </v-row>
                              
                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-select
                                    v-model="selectedLanguage"
                                    :items="languages"
                                    label="Idioma"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    prepend-inner-icon="mdi-translate"
                                    required
                                  ></v-select>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-select
                                    v-model="selectedModel"
                                    :items="models"
                                    label="Modelo de Voz"
                                    variant="outlined"
                                    :disabled="isLoading || !selectedLanguage"
                                    prepend-inner-icon="mdi-account-voice"
                                    required
                                  ></v-select>
                                </v-col>
                              </v-row>

                              <v-row>
                                <v-col cols="12">
                                  <v-textarea
                                    v-model="inputText"
                                    label="Texto para Sintetizar"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    rows="5"
                                    counter
                                    placeholder="Digite ou cole aqui o texto que deseja converter em áudio..."
                                    required
                                  ></v-textarea>
                                </v-col>
                              </v-row>

                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-text-field
                                    v-model="speakerId"
                                    label="ID do Locutor (opcional)"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    hint="Deixe vazio para usar o padrão"
                                    prepend-inner-icon="mdi-account"
                                  ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-card class="pa-3" variant="outlined">
                                    <div class="d-flex align-center mb-2">
                                      <v-icon icon="mdi-speedometer" class="mr-2"></v-icon>
                                      <span class="text-subtitle-1">Velocidade: {{ speed.toFixed(1) }}x</span>
                                    </div>
                                    <v-slider
                                      v-model="speed"
                                      :min="0.5"
                                      :max="2.0"
                                      :step="0.1"
                                      :disabled="isLoading"
                                      thumb-label
                                      show-ticks="always"
                                      color="primary"
                                    ></v-slider>
                                  </v-card>
                                </v-col>
                              </v-row>

                              <v-row class="mt-4">
                                <v-col cols="12" class="text-center">
                                  <v-btn
                                    type="submit"
                                    color="primary"
                                    size="large"
                                    :disabled="!canSubmit || isLoading"
                                    :loading="isLoading"
                                    class="px-8"
                                    elevation="2"
                                  >
                                    <v-icon icon="mdi-volume-high" class="mr-2"></v-icon>
                                    Gerar Áudio
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </v-form>
                          </v-window-item>

                          <!-- Document Processing Tab -->
                          <v-window-item value="document">
                            <v-form @submit.prevent="handleDocumentUpload" class="document-form">
                              <v-row>
                                <v-col cols="12">
                                  <v-alert
                                    type="info"
                                    variant="tonal"
                                    icon="mdi-information-outline"
                                    class="mb-4"
                                  >
                                    Faça upload de um documento (PDF, DOCX, PPTX ou TXT) para extrair o texto e convertê-lo em áudio.
                                  </v-alert>
                                </v-col>
                              </v-row>
                              
                              <v-row>
                                <v-col cols="12">
                                  <v-file-input
                                    v-model="documentFile"
                                    label="Selecione um documento"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    accept=".pdf,.docx,.pptx,.txt"
                                    prepend-icon="mdi-file-document-outline"
                                    show-size
                                    truncate-length="30"
                                    required
                                  >
                                    <template v-slot:selection="{ fileNames }">
                                      <v-chip
                                        color="primary"
                                        label
                                        size="small"
                                        class="mr-2"
                                      >
                                        {{ fileNames[0] }}
                                      </v-chip>
                                    </template>
                                  </v-file-input>
                                </v-col>
                              </v-row>

                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-select
                                    v-model="selectedLanguage"
                                    :items="languages"
                                    label="Idioma"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    prepend-inner-icon="mdi-translate"
                                    required
                                  ></v-select>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-select
                                    v-model="selectedModel"
                                    :items="models"
                                    label="Modelo de Voz"
                                    variant="outlined"
                                    :disabled="isLoading || !selectedLanguage"
                                    prepend-inner-icon="mdi-account-voice"
                                    required
                                  ></v-select>
                                </v-col>
                              </v-row>

                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-text-field
                                    v-model="speakerId"
                                    label="ID do Locutor (opcional)"
                                    variant="outlined"
                                    :disabled="isLoading"
                                    hint="Deixe vazio para usar o padrão"
                                    prepend-inner-icon="mdi-account"
                                  ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-card class="pa-3" variant="outlined">
                                    <div class="d-flex align-center mb-2">
                                      <v-icon icon="mdi-speedometer" class="mr-2"></v-icon>
                                      <span class="text-subtitle-1">Velocidade: {{ speed.toFixed(1) }}x</span>
                                    </div>
                                    <v-slider
                                      v-model="speed"
                                      :min="0.5"
                                      :max="2.0"
                                      :step="0.1"
                                      :disabled="isLoading"
                                      thumb-label
                                      show-ticks="always"
                                      color="primary"
                                    ></v-slider>
                                  </v-card>
                                </v-col>
                              </v-row>

                              <v-row class="mt-4">
                                <v-col cols="12" class="text-center">
                                  <v-btn
                                    type="submit"
                                    color="primary"
                                    size="large"
                                    :disabled="!documentFile || isLoading"
                                    :loading="isLoading"
                                    class="px-8"
                                    elevation="2"
                                  >
                                    <v-icon icon="mdi-file-document-outline" class="mr-2"></v-icon>
                                    Processar Documento
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </v-form>
                          </v-window-item>
                        </v-window>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>

        <!-- Results Section -->
        <v-row class="ma-0 pa-0 bg-grey-lighten-5" v-if="audioURL || documentChunks.length > 0">
          <v-col cols="12" class="pa-0">
            <v-sheet class="py-10">
              <v-container>
                <v-row justify="center">
                  <v-col cols="12" md="10" lg="8">
                    <!-- Audio Output Section (for direct text input) -->
                    <v-card v-if="audioURL" class="audio-output mb-8 elevation-3 rounded-lg overflow-hidden">
                      <v-card-title class="text-h5 font-weight-bold bg-primary text-white py-4">
                        <v-icon icon="mdi-volume-high" class="mr-2"></v-icon>
                        Áudio Gerado
                      </v-card-title>
                      <v-card-text class="pa-6">
                        <v-alert
                          type="success"
                          variant="tonal"
                          icon="mdi-check-circle"
                          class="mb-4"
                        >
                          Áudio gerado com sucesso! Você pode ouvir abaixo ou fazer o download.
                        </v-alert>
                        
                        <v-card class="pa-4 mb-4" variant="outlined">
                          <audio 
                            controls 
                            :src="audioURL" 
                            class="w-100"
                          ></audio>
                        </v-card>
                      </v-card-text>
                      <v-card-actions class="pa-4 pt-0">
                        <v-spacer></v-spacer>
                        <v-btn
                          color="primary"
                          prepend-icon="mdi-download"
                          :href="audioURL"
                          download="tts_audio.wav"
                          variant="elevated"
                        >
                          Download do Áudio
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                    
                    <!-- Document Chunks Section -->
                    <v-card v-if="documentChunks.length > 0" class="elevation-3 rounded-lg overflow-hidden">
                      <v-card-title class="text-h5 font-weight-bold bg-primary text-white py-4">
                        <v-icon icon="mdi-file-document-outline" class="mr-2"></v-icon>
                        Documento Processado
                      </v-card-title>
                      <v-card-text class="pa-6">
                        <v-alert
                          type="success"
                          variant="tonal"
                          icon="mdi-check-circle"
                          class="mb-4"
                        >
                          Documento <strong>{{ processedDocument.filename }}</strong> processado com sucesso! 
                          Foram extraídas {{ documentChunks.length }} partes de texto.
                        </v-alert>
                        
                        <v-expansion-panels variant="accordion">
                          <v-expansion-panel
                            v-for="(chunk, index) in documentChunks"
                            :key="index"
                            class="mb-2"
                          >
                            <v-expansion-panel-title>
                              <div class="d-flex align-center">
                                <v-icon icon="mdi-text-box-outline" class="mr-2"></v-icon>
                                <span>Parte {{ index + 1 }}</span>
                                <v-chip
                                  size="small"
                                  color="grey-lighten-1"
                                  class="ml-2"
                                >
                                  {{ chunk.length }} caracteres
                                </v-chip>
                                <v-chip
                                  v-if="chunkAudios[index]"
                                  size="small"
                                  color="success"
                                  class="ml-2"
                                >
                                  Áudio Gerado
                                </v-chip>
                              </div>
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                              <v-card variant="outlined" class="pa-4 mb-4 bg-grey-lighten-5">
                                <p class="text-body-1">{{ chunk }}</p>
                              </v-card>
                              
                              <div v-if="!chunkAudios[index]" class="d-flex justify-center mb-4">
                                <v-btn
                                  color="primary"
                                  @click="generateAudioForChunk(chunk, index)"
                                  :loading="chunkProcessingIndex === index"
                                  :disabled="isLoading"
                                  prepend-icon="mdi-volume-high"
                                  variant="elevated"
                                >
                                  Gerar Áudio para esta Parte
                                </v-btn>
                              </div>
                              
                              <v-card v-if="chunkAudios[index]" class="pa-4" variant="outlined">
                                <div class="d-flex align-center mb-2">
                                  <v-icon icon="mdi-volume-high" color="primary" class="mr-2"></v-icon>
                                  <span class="text-h6">Áudio Gerado</span>
                                </div>
                                <audio 
                                  controls 
                                  :src="chunkAudios[index]" 
                                  class="w-100 mb-2"
                                ></audio>
                                <div class="d-flex justify-end">
                                  <v-btn
                                    color="primary"
                                    variant="text"
                                    :href="chunkAudios[index]"
                                    download="tts_chunk_audio.wav"
                                    prepend-icon="mdi-download"
                                    density="comfortable"
                                  >
                                    Download
                                  </v-btn>
                                </div>
                              </v-card>
                            </v-expansion-panel-text>
                          </v-expansion-panel>
                        </v-expansion-panels>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>

        <!-- Error Alert -->
        <v-row v-if="errorMessage" class="ma-0 pa-0">
          <v-col cols="12" class="pa-0">
            <v-container>
              <v-row justify="center">
                <v-col cols="12" md="10" lg="8" class="pa-4">
                  <v-alert
                    type="error"
                    variant="tonal"
                    closable
                    @click:close="errorMessage = null"
                    class="elevation-2"
                  >
                    <template v-slot:prepend>
                      <v-icon icon="mdi-alert-circle" size="large"></v-icon>
                    </template>
                    <div class="text-subtitle-1 font-weight-medium">Erro</div>
                    <div>{{ errorMessage }}</div>
                  </v-alert>
                </v-col>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
        
        <!-- Features Section -->
        <v-row class="ma-0 pa-0 bg-grey-lighten-4">
          <v-col cols="12" class="pa-0">
            <v-sheet class="py-12">
              <v-container>
                <v-row justify="center" class="mb-8">
                  <v-col cols="12" md="8" class="text-center">
                    <h2 class="text-h3 font-weight-bold text-primary mb-2">Recursos</h2>
                    <p class="text-subtitle-1">Conheça os principais recursos da nossa plataforma de conversão de texto em fala</p>
                  </v-col>
                </v-row>
                
                <v-row justify="center">
                  <v-col cols="12" sm="6" md="4" class="pa-4">
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                        v-bind="props"
                        :elevation="isHovering ? 8 : 2"
                        :class="{ 'on-hover': isHovering }"
                        height="100%"
                        class="transition-swing rounded-lg"
                      >
                        <v-card-text class="text-center pa-6">
                          <v-avatar
                            color="primary"
                            size="80"
                            class="mb-4"
                          >
                            <v-icon size="40" color="white" icon="mdi-translate"></v-icon>
                          </v-avatar>
                          <h3 class="text-h5 font-weight-bold mb-2">Multilíngue</h3>
                          <p class="text-body-1">Suporte a diversos idiomas para atender a um público global. Escolha entre diferentes modelos de voz para cada idioma.</p>
                        </v-card-text>
                      </v-card>
                    </v-hover>
                  </v-col>

                  <v-col cols="12" sm="6" md="4" class="pa-4">
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                        v-bind="props"
                        :elevation="isHovering ? 8 : 2"
                        :class="{ 'on-hover': isHovering }"
                        height="100%"
                        class="transition-swing rounded-lg"
                      >
                        <v-card-text class="text-center pa-6">
                          <v-avatar
                            color="primary"
                            size="80"
                            class="mb-4"
                          >
                            <v-icon size="40" color="white" icon="mdi-file-document-outline"></v-icon>
                          </v-avatar>
                          <h3 class="text-h5 font-weight-bold mb-2">Processamento de Documentos</h3>
                          <p class="text-body-1">Converta documentos PDF, DOCX, PPTX e TXT em áudio. Ideal para transformar artigos, relatórios e livros em conteúdo de áudio.</p>
                        </v-card-text>
                      </v-card>
                    </v-hover>
                  </v-col>

                  <v-col cols="12" sm="6" md="4" class="pa-4">
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                        v-bind="props"
                        :elevation="isHovering ? 8 : 2"
                        :class="{ 'on-hover': isHovering }"
                        height="100%"
                        class="transition-swing rounded-lg"
                      >
                        <v-card-text class="text-center pa-6">
                          <v-avatar
                            color="primary"
                            size="80"
                            class="mb-4"
                          >
                            <v-icon size="40" color="white" icon="mdi-account-voice"></v-icon>
                          </v-avatar>
                          <h3 class="text-h5 font-weight-bold mb-2">Vozes Naturais</h3>
                          <p class="text-body-1">Síntese de voz que soa natural e expressiva. Ajuste a velocidade da fala e escolha entre diferentes locutores para personalizar o resultado.</p>
                        </v-card-text>
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>

        <!-- Footer -->
        <v-footer app class="pa-0" color="primary" elevation="4">
          <v-container>
            <v-row class="py-6">
              <v-col cols="12" md="4" class="text-center text-md-left">
                <div class="d-flex align-center justify-center justify-md-start mb-4">
                  <v-icon icon="mdi-text-to-speech" size="large" color="white" class="mr-2"></v-icon>
                  <span class="text-h5 text-white font-weight-bold">Testupavois</span>
                </div>
                <p class="text-white text-body-2 mb-0">Uma plataforma avançada de conversão de texto em fala utilizando modelos de IA de última geração.</p>
              </v-col>
              
              <v-col cols="12" md="4" class="text-center d-flex flex-column align-center justify-center">
                <div class="text-white text-subtitle-1 font-weight-medium mb-4">Links Rápidos</div>
                <div class="d-flex flex-wrap justify-center">
                  <v-btn variant="text" color="white" class="mx-2 mb-2" @click="scrollToTTS">
                    <v-icon icon="mdi-text-to-speech" size="small" class="mr-1"></v-icon>
                    Texto para Voz
                  </v-btn>
                  <v-btn variant="text" color="white" class="mx-2 mb-2" href="https://github.com/k2-fsa/sherpa-onnx" target="_blank">
                    <v-icon icon="mdi-github" size="small" class="mr-1"></v-icon>
                    GitHub
                  </v-btn>
                </div>
              </v-col>
              
              <v-col cols="12" md="4" class="text-center text-md-right">
                <div class="text-white text-subtitle-1 font-weight-medium mb-4">Tecnologias</div>
                <div class="d-flex flex-wrap justify-center justify-md-end">
                  <v-chip color="white" text-color="primary" class="ma-1">Vue.js</v-chip>
                  <v-chip color="white" text-color="primary" class="ma-1">Vuetify</v-chip>
                  <v-chip color="white" text-color="primary" class="ma-1">FastAPI</v-chip>
                  <v-chip color="white" text-color="primary" class="ma-1">Sherpa-ONNX</v-chip>
                </div>
              </v-col>
            </v-row>
            
            <v-divider color="white" opacity="0.2"></v-divider>
            
            <v-row class="py-3">
              <v-col cols="12" class="text-center text-white text-caption">
                &copy; {{ new Date().getFullYear() }} Testupavois - Text-to-Speech. Todos os direitos reservados.
              </v-col>
            </v-row>
          </v-container>
        </v-footer>
      </v-main>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import ThemeSwitcher from './components/ThemeSwitcher.vue';
import { ref, computed, onMounted, watch } from 'vue';
import { useTheme } from 'vuetify';
import { getLanguages, getModelsForLanguage, submitTTSRequest } from './apiService';
import axios from 'axios';

// Vuetify theme
const vuetifyTheme = useTheme();

// Theme state
const theme = ref('light');

// Tab state
const activeTab = ref('tts');

// Refs
const ttsSection = ref(null);

// Form state
const languages = ref<string[]>([]);
const selectedLanguage = ref<string>('');
const models = ref<string[]>([]);
const selectedModel = ref<string>('');
const inputText = ref<string>('');
const speakerId = ref<string>('0');
const speed = ref<number>(1.0);

// Document processing state
const documentFile = ref<File | null>(null);
const documentChunks = ref<string[]>([]);
const processedDocument = ref<{filename: string, file_type: string}>({filename: '', file_type: ''});
const chunkAudios = ref<{[key: number]: string}>({});
const chunkProcessingIndex = ref<number | null>(null);

// UI state
const audioURL = ref<string | null>(null);
const isLoading = ref<boolean>(false);
const errorMessage = ref<string | null>(null);

// Computed properties
const canSubmit = computed(() => {
  return selectedLanguage.value && selectedModel.value && inputText.value.trim().length > 0;
});

/**
 * Load available languages from the API
 */
const loadLanguages = async () => {
  isLoading.value = true;
  errorMessage.value = null;
  try {
    languages.value = await getLanguages();
    if (languages.value.length > 0) {
      // Auto-select first language for better UX
      selectedLanguage.value = languages.value[0]; 
    }
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Failed to load languages.';
    console.error('Error loading languages:', err);
  } finally {
    isLoading.value = false;
  }
};

/**
 * Load models for the selected language
 */
const loadModels = async () => {
  if (!selectedLanguage.value) {
    models.value = [];
    selectedModel.value = '';
    return;
  }
  
  models.value = []; // Clear previous models
  selectedModel.value = ''; // Reset selected model
  
  try {
    models.value = await getModelsForLanguage(selectedLanguage.value);
    if (models.value.length > 0) {
      // Auto-select first model for better UX
      selectedModel.value = models.value[0];
    }
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Failed to load models.';
    console.error('Error loading models:', err);
  }
};

/**
 * Handle form submission to generate speech
 */
const handleFormSubmit = async () => {
  if (!canSubmit.value) {
    errorMessage.value = 'Por favor, preencha todos os campos obrigatórios: idioma, modelo e texto.';
    return;
  }
  
  isLoading.value = true;
  errorMessage.value = null;
  
  // Clean up previous audio if exists
  if (audioURL.value) {
    URL.revokeObjectURL(audioURL.value);
    audioURL.value = null;
  }

  try {
    const result = await submitTTSRequest(
      selectedLanguage.value,
      selectedModel.value,
      inputText.value,
      speakerId.value,
      speed.value
    );
    
    audioURL.value = URL.createObjectURL(result.audioBlob);
    
    // Scroll to audio player after generation
    setTimeout(() => {
      const audioElement = document.querySelector('.audio-output');
      if (audioElement) {
        audioElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Falha na síntese de voz.';
    console.error('TTS Submit Error:', err);
  } finally {
    isLoading.value = false;
  }
};

/**
 * Handle document upload and processing
 */
const handleDocumentUpload = async () => {
  if (!documentFile.value) {
    errorMessage.value = 'Por favor, selecione um documento para processar.';
    return;
  }
  
  if (!selectedLanguage.value || !selectedModel.value) {
    errorMessage.value = 'Por favor, selecione um idioma e um modelo.';
    return;
  }
  
  isLoading.value = true;
  errorMessage.value = null;
  
  // Reset previous document processing state
  documentChunks.value = [];
  chunkAudios.value = {};
  
  try {
    const formData = new FormData();
    formData.append('file', documentFile.value);
    formData.append('max_chunk_length', '5000');
    
    const response = await axios.post('http://localhost:8000/api/process-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    documentChunks.value = response.data.chunks;
    processedDocument.value = {
      filename: response.data.filename,
      file_type: response.data.file_type
    };
    
    console.log('Document processed successfully:', response.data);
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Falha no processamento do documento.';
    console.error('Document Processing Error:', err);
  } finally {
    isLoading.value = false;
  }
};

/**
 * Generate audio for a specific document chunk
 */
const generateAudioForChunk = async (chunk: string, index: number) => {
  chunkProcessingIndex.value = index;
  
  try {
    const formData = new FormData();
    formData.append('language', selectedLanguage.value);
    formData.append('repo_id', selectedModel.value);
    formData.append('text_chunk', chunk);
    formData.append('sid', speakerId.value);
    formData.append('speed', speed.value.toString());
    
    const response = await axios.post('http://localhost:8000/api/tts-from-chunk', formData, {
      responseType: 'blob'
    });
    
    const audioBlob = new Blob([response.data], { type: 'audio/wav' });
    const audioUrl = URL.createObjectURL(audioBlob);
    
    // Store audio URL for this chunk
    chunkAudios.value = { ...chunkAudios.value, [index]: audioUrl };
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Falha na geração de áudio para o trecho.';
    console.error('Chunk TTS Error:', err);
  } finally {
    chunkProcessingIndex.value = null;
  }
};

// Lifecycle hooks
onMounted(() => {
  loadLanguages();
  
  // Check for system dark mode preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    theme.value = 'dark';
    vuetifyTheme.global.name.value = 'dark';
  }
});

// Watchers
watch(selectedLanguage, () => {
  loadModels();
});

/**
 * Handle theme change from the ThemeSwitcher component
 */
const handleThemeChange = (newTheme: string) => {
  theme.value = newTheme;
  vuetifyTheme.global.name.value = newTheme;
};

/**
 * Scroll to TTS section
 */
const scrollToTTS = () => {
  if (ttsSection.value) {
    ttsSection.value.$el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};
</script>

<style scoped>
/* Custom styles for audio element */
audio {
  width: 100%;
  border-radius: 8px;
}

.w-100 {
  width: 100%;
}

/* Pulse animation for hero section */
.pulse-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  z-index: 0;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 20px rgba(255, 255, 255, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
  }
}

/* Hover effect for feature cards */
.on-hover {
  transform: translateY(-8px);
  transition: all 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .hero-section {
    text-align: center;
  }
}
</style>
