<template>
  <div class="document-uploader">
    <v-card flat>
      <v-card-text>
        <v-file-input
          v-model="files"
          :loading="isUploading"
          accept=".pdf,.docx,.txt"
          label="Upload Document"
          placeholder="Select a document to convert to speech"
          prepend-icon="mdi-file-upload"
          variant="outlined"
          show-size
          counter
          multiple
          chips
          class="mb-4"
          @change="handleFileUpload"
        ></v-file-input>

        <div v-if="isUploading" class="text-center mb-4">
          <v-progress-circular
            indeterminate
            color="primary"
            class="mb-2"
          ></v-progress-circular>
          <div class="text-body-2 text-medium-emphasis">
            Uploading and processing document...
          </div>
        </div>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          closable
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <v-list v-if="uploadedFiles.length > 0" class="bg-grey-lighten-4 rounded-lg">
          <v-list-subheader>Uploaded Documents</v-list-subheader>
          <v-list-item
            v-for="file in uploadedFiles"
            :key="file.id"
            :title="file.name"
            :subtitle="formatFileSize(file.size)"
          >
            <template v-slot:prepend>
              <v-icon
                :color="getFileIconColor(file.type)"
                :icon="getFileIcon(file.type)"
              ></v-icon>
            </template>
            <template v-slot:append>
              <v-btn
                icon="mdi-play"
                variant="text"
                color="primary"
                size="small"
                @click="playFile(file)"
              ></v-btn>
              <v-btn
                icon="mdi-download"
                variant="text"
                color="primary"
                size="small"
                @click="downloadFile(file)"
              ></v-btn>
            </template>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

interface UploadedFile {
  id: string
  name: string
  size: number
  type: string
  url: string
}

const files = ref<File[]>([])
const isUploading = ref(false)
const error = ref('')
const uploadedFiles = ref<UploadedFile[]>([])

const emit = defineEmits(['file-processed'])

const handleFileUpload = async () => {
  if (!files.value.length) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    error.value = ''
    uploadProgress.value = 0

    const response = await axios.post('/api/upload-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = (progressEvent.loaded / progressEvent.total) * 100
      }
    })

    emit('file-uploaded', response.data)
  } catch (err) {
    error.value = 'Error uploading file. Please try again.'
    console.error('Upload error:', err)
  }
}
</script>
