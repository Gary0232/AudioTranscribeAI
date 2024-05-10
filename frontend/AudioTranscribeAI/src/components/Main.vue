<script setup>
import {ref, watch} from "vue";
import axios from 'axios';
import CompromiseTextBox from "@/components/CompromiseTextBox.vue";
import {debounce} from "lodash";


const apiUrl = 'http://localhost:4000';
// variable to store file upload


// current step
const step = ref(0);


// Step 1
const file_recognition_loading = ref(false);
const fileHash = ref(null);
const recognitionResult = ref("");
const originalText = ref("");
const recognitionTokenizedResult = ref([]);
const files = ref(null);
const selected_language = ref({state: 'English', abbr: 'en'})
const available_language = [
  {state: 'English', abbr: 'en'},
  {state: 'Japanese', abbr: 'ja'},
  {state: 'French', abbr: 'fr'},
  {state: 'German', abbr: 'de'},
  {state: 'Spanish', abbr: 'es'},
  {state: 'Russian', abbr: 'ru'},
]

function submitFile() {
  file_recognition_loading.value = true;
  const formData = new FormData();
  formData.append('file', files.value);
  formData.append('language', selected_language.value.abbr);
  axios.post(apiUrl + '/file_upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    summarizationResult.value = null;
    if (response.data.status === 'success') {
      recognitionResult.value = response.data.recognition_result.text;
      originalText.value = response.data.recognition_result.original_text;
      recognitionTokenizedResult.value = response.data.recognition_result.tokens;
      fileHash.value = response.data.hash;
    }
  }).catch(error => {
    console.error(error);
  }).finally(() => {
    file_recognition_loading.value = false;
  });
}

// step 2
// on watch the selected word
const selectedWord = ref(null);
const wikipediaResult = ref(null);
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

// step 3
const summarizationResult = ref(null);
const hideQADrawer = ref(true);


// QA
const qaList = ref([]);

function generateSummary() {
  axios.post(apiUrl + '/summarize', {
    text: recognitionResult.value,
    hash: fileHash.value
  }).then(response => {
    summarizationResult.value = response.data.summarization_result;
  }).catch(error => {
    console.error(error);
  });
}

const question = ref(null);
const qaLoading = ref(false);
function sendQuestion() {
  const questionData = question.value;
  if (!questionData) {
    return;
  }
  qaLoading.value = true;
  axios.post(apiUrl + '/qa', {
    question: questionData,
    hash: fileHash.value
  }).then(response => {
    qaList.value.push({
      who: 'user',
      text: questionData
    });
    qaList.value.push({
      who: 'model',
      text: response.data.answer
    });
  }).catch(error => {
    console.error(error);
  }).finally(() => {
    question.value = null;
    qaLoading.value = false;
  });
}

</script>

<template>
  <v-container fluid class="fill-height ma-0 pa-0">
    <v-row class="fill-height mx-2">
      <v-col cols="4" class="h-100" v-if="step === 0">
        <v-card class="fill-height">
          <v-card-title>
            Task 1: Automatic Speech Recognition
          </v-card-title>
          <v-card-text>
            <v-file-input
              accept="audio/*, video/mp4"
              label="Upload the audio/video file here"
              placeholder="No file chosen"
              prepend-icon="mdi-multimedia"
              show-size
              v-model="files"
            ></v-file-input>


            <v-select
              v-model="selected_language"
              :hint="`${selected_language.state}, ${selected_language.abbr}`"
              :items="available_language"
              item-title="state"
              item-value="abbr"
              label="Choose the language of the source file"
              persistent-hint
              return-object
              prepend-icon="mdi-translate"
            ></v-select>

            <v-card-actions>
              <v-btn @click="submitFile" variant="flat" color="blue"
                     :disabled="!files || !selected_language || file_recognition_loading" block>
                Submit
              </v-btn>
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
              <v-card v-if="originalText">
                {{ originalText }}
              </v-card>
              <v-card v-if="originalText" class="mt-4">
                <v-card-title>
                  Translated Result
                </v-card-title>
                <v-card-text>
                  {{ recognitionResult }}
                </v-card-text>
              </v-card>
              <div v-else>
                {{ recognitionResult }}
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="step = 1" v-if="step === 0" variant="flat" color="blue">
              Go to Task 2
            </v-btn>
            <v-btn @click="step = 0" v-if="step === 1" variant="flat" color="blue">
              Back to File Upload
            </v-btn>
            <v-btn color="purple" v-if="step === 1" variant="flat" @click="generateSummary">
              Generate Summary
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
          <v-card-text class="flex-grow-1" v-else-if="wikipediaResult !== null">
            {{ wikipediaResult }}
          </v-card-text>
          <v-card-text v-else class="flex-grow-1 d-flex flex-column justify-center align-center">
            <v-progress-circular
              indeterminate
            ></v-progress-circular>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4" v-if="summarizationResult" class="h-100">
        <v-card class="fill-height d-flex flex-column">
          <v-card-title class="d-flex justify-space-between">
            Text Summarization
            <v-btn @click="summarizationResult = null" icon variant="plain">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text style="overflow-y: auto;">
            {{ recognitionResult }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-navigation-drawer
      width="400"
      location="right"
      permanent
      :rail="hideQADrawer"
      v-if="step === 1"
    >
      <v-btn @click="hideQADrawer = !hideQADrawer" variant="text" icon v-if="hideQADrawer">
        <v-icon>{{ hideQADrawer ? 'mdi-chat-question' : 'mdi-chevron-right' }}</v-icon>
      </v-btn>
      <v-list color="transparent" v-if="!hideQADrawer">
        <v-list-item v-for="data in qaList" :key="data.text"
                     class="text-caption"
                     :prepend-icon="data.who === 'model'? 'mdi-view-dashboard' : ''"
                     :append-icon="data.who === 'model'? '' : 'mdi-account'">
          {{ data.text }}
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-textarea :loading="qaLoading" rows="4" v-model="question" placeholder="Ask a question here..."
                    no-resize hide-details rounded="0" v-if="!hideQADrawer"></v-textarea>
        <v-btn rounded="0" v-if="!hideQADrawer" @click="sendQuestion" :disabled="qaLoading" color="primary">
          Send
        </v-btn>
        <v-btn rounded="0" @click="hideQADrawer = !hideQADrawer" v-if="!hideQADrawer">
          Hide
        </v-btn>

      </template>
    </v-navigation-drawer>
  </v-container>
</template>


