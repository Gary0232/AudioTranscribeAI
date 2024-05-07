<script setup>
import {ref, watch} from "vue";
import axios from 'axios';
import CompromiseTextBox from "@/components/CompromiseTextBox.vue";
import {debounce} from "lodash";


const apiUrl = 'http://localhost:5000';
// variable to store file upload
const files = ref(null);

// current step
const step = ref(0);


const recognitionResult = ref("");
const recognitionTokenizedResult = ref([]);
const wikipediaResult = ref(null);
const summarizationResult = ref(null);
const selectedWord = ref(null);

// on watch the selected word
watch(selectedWord, (newValue) => {
  fetchWikipedia(newValue);
});

const fetchWikipedia = debounce((word) => {
  if (word) {
    axios.get(apiUrl + '/wikipedia', {
      params: {
        keyword: word.text
      }
    }).then(response => {
      wikipediaResult.value = response.data;
    }).catch(error => {
      console.error(error);
    });
  }
}, 1000);

function submitFile() {
  const formData = new FormData();
  formData.append('file', files.value);

  axios.post(apiUrl + '/file_upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    summarizationResult.value = null;
    if (response.data.status === 'success') {
      recognitionResult.value = response.data.recognition_result.text;
      recognitionTokenizedResult.value = response.data.recognition_result.tokens;
    }
  }).catch(error => {
    console.error(error);
  });
}

function generateSummary() {
  axios.post(apiUrl + '/summarize', {
    text: recognitionResult.value
  }).then(response => {
    summarizationResult.value = response.data.summarization_result;
  }).catch(error => {
    console.error(error);
  });
}

</script>

<template>
  <v-container fluid class="fill-height ma-0 pa-0">
    <v-row class="fill-height">
      <v-col cols="4" class="h-100" v-if="step === 0">
        <v-card class="fill-height">
          <v-card-title>
            Task 1: Automatic Speech Recognition
          </v-card-title>
          <v-card-text>
            <v-file-input
              accept="audio/*, video/*"
              label="Upload the audio/video file here"
              placeholder="No file chosen"
              prepend-icon="mdi-multimedia"
              show-size
              v-model="files"
            ></v-file-input>
            <v-card-actions>
              <v-btn @click="submitFile" variant="flat" color="blue" :disabled="!files" block>Submit</v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col :cols="summarizationResult === null? 8: 4" class="h-100">
        <v-card class="fill-height d-flex flex-column" v-if="recognitionResult">
          <v-card-title>
            {{ step === 0 ? 'Results' : 'Source Text' }}
          </v-card-title>
          <v-card-text class="flex-grow-1" style="overflow-y: auto">
            <compromise-text-box :words="recognitionTokenizedResult" v-model="selectedWord" v-if="step === 1"/>
            <div v-else>
              {{ recognitionResult }}
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="step = 1" v-if="step === 0" variant="flat" color="blue">
              Go to Task 2
            </v-btn>
            <v-btn @click="step = 0" v-if="step === 1" variant="flat" color="blue">
              Back to File Upload
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-card class="fill-height" v-else>
          <v-card-title>
            Results
          </v-card-title>
          <v-card-text>
            No results available
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4" class="h-100" v-if="step === 1">
        <v-card class="fill-height d-flex flex-column">
          <v-card-title>
            Wikipedia
          </v-card-title>
          <v-card-text class="flex-grow-1" v-if="selectedWord == null">
            Select a word to fetch Wikipedia information
          </v-card-text>
          <v-card-text class="flex-grow-1" v-else-if="wikipediaResult !== null" >
            {{ wikipediaResult }}
          </v-card-text>
          <v-card-text v-else class="flex-grow-1 d-flex flex-column justify-center align-center">
            <v-progress-circular
              indeterminate
            ></v-progress-circular>
          </v-card-text>
          <v-card-actions>
            <v-btn block color="purple" variant="flat" @click="generateSummary">
              Generate Summary
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="4" v-if="summarizationResult" class="h-100">
        <v-card class="fill-height d-flex flex-column">
          <v-card-title>
            Text Summarization
          </v-card-title>
          <v-card-text style="overflow-y: auto;">
            {{ recognitionResult }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


