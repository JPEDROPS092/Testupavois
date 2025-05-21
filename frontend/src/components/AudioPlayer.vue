<template>
  <v-card class="pa-4" v-if="audioUrl">
    <v-row align="center">
      <v-col cols="12">
        <audio
          ref="audioPlayer"
          :src="audioUrl"
          controls
          class="w-100"
          @ended="handleAudioEnded"
        />
      </v-col>
    </v-row>

          <div class="d-flex align-center justify-space-between w-100 mb-4">
            <v-btn
              :icon="isPlaying ? 'mdi-pause' : 'mdi-play'"
              color="primary"
              @click="togglePlay"
            ></v-btn>

            <v-slider
              v-model="currentTime"
              :max="duration"
              :step="0.1"
              class="mx-4"
              hide-details
              @change="seekAudio"
            ></v-slider>

            <div class="text-body-2 text-medium-emphasis">
              {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
            </div>
          </div>

          <div class="d-flex align-center justify-space-between w-100">
            <v-btn-group variant="outlined" color="primary">
              <v-btn
                prepend-icon="mdi-volume-medium"
                @click="adjustVolume(-0.1)"
              >
                -
              </v-btn>
              <v-btn
                prepend-icon="mdi-volume-high"
                @click="adjustVolume(0.1)"
              >
                +
              </v-btn>
            </v-btn-group>

            <v-btn-group variant="outlined" color="primary">
              <v-btn
                prepend-icon="mdi-speedometer-slow"
                @click="adjustSpeed(-0.1)"
              >
                -
              </v-btn>
              <v-btn
                prepend-icon="mdi-speedometer"
                @click="adjustSpeed(0.1)"
              >
                +
              </v-btn>
            </v-btn-group>

            <v-btn
              color="primary"
              prepend-icon="mdi-download"
              @click="downloadAudio"
            >
              Download
            </v-btn>
          </div>
        </div>

        <div v-else class="text-center pa-4">
          <v-icon
            icon="mdi-music-note-off"
            size="64"
            color="grey-lighten-1"
          ></v-icon>
          <div class="text-body-1 text-medium-emphasis mt-2">
            No audio available
          </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps<{
  audioPath: {
    type: String,
    required: true
  }
}>()

const audioUrl = ref('')
const audioElement = ref<HTMLAudioElement | null>(null)
const visualizer = ref<HTMLCanvasElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1)
const playbackRate = ref(1)

let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let animationFrame: number | null = null

watch(() => props.audioPath, (newPath) => {
  if (newPath) {
    audioUrl.value = `/api/audio/${newPath}`
    setupAudio()
  }
})

onMounted(() => {
  if (props.audioPath) {
    audioUrl.value = `/api/audio/${props.audioPath}`
    setupAudio()
  }
})

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
  if (audioContext) {
    audioContext.close()
  }
})

const setupAudio = () => {
  audioElement.value = new Audio(audioUrl.value)
  audioElement.value.addEventListener('timeupdate', updateTime)
  audioElement.value.addEventListener('loadedmetadata', () => {
    duration.value = audioElement.value?.duration || 0
  })
  audioElement.value.addEventListener('ended', () => {
    isPlaying.value = false
  })

  setupVisualizer()
}

const setupVisualizer = () => {
  if (!audioElement.value || !visualizer.value) return

  audioContext = new AudioContext()
  analyser = audioContext.createAnalyser()
  const source = audioContext.createMediaElementSource(audioElement.value)
  source.connect(analyser)
  analyser.connect(audioContext.destination)

  analyser.fftSize = 256
  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)

  const canvas = visualizer.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const draw = () => {
    if (!analyser || !ctx) return

    animationFrame = requestAnimationFrame(draw)
    analyser.getByteFrequencyData(dataArray)

    ctx.fillStyle = 'rgba(33, 150, 243, 0.2)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const barWidth = (canvas.width / bufferLength) * 2.5
    let barHeight
    let x = 0

    for (let i = 0; i < bufferLength; i++) {
      barHeight = (dataArray[i] / 255) * canvas.height

      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#2196F3')
      gradient.addColorStop(1, '#82B1FF')
      ctx.fillStyle = gradient

      ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
      x += barWidth + 1
    }
  }

  draw()
}

const togglePlay = async () => {
  if (!audioElement.value) return

  if (audioContext?.state === 'suspended') {
    await audioContext.resume()
  }

  if (isPlaying.value) {
    audioElement.value.pause()
  } else {
    audioElement.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const updateTime = () => {
  if (!audioElement.value) return
  currentTime.value = audioElement.value.currentTime
}

const seekAudio = () => {
  if (!audioElement.value) return
  audioElement.value.currentTime = currentTime.value
}

const adjustVolume = (delta: number) => {
  if (!audioElement.value) return
  volume.value = Math.max(0, Math.min(1, volume.value + delta))
  audioElement.value.volume = volume.value
}

const adjustSpeed = (delta: number) => {
  if (!audioElement.value) return
  playbackRate.value = Math.max(0.5, Math.min(2, playbackRate.value + delta))
  audioElement.value.playbackRate = playbackRate.value
}

const formatTime = (time: number): string => {
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
  // Handle audio playback ended
}

const downloadAudio = () => {
  if (audioUrl.value) {
    const link = document.createElement('a')
    link.href = audioUrl.value
    link.download = `tts_audio_${Date.now()}.wav`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}
</script>

<style scoped>
audio {
  width: 100%;
}
</style>
