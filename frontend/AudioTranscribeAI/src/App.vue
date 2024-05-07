<template>
  <v-app>
    <v-app-bar color="info" density="compact" flat>
      <v-app-bar-title>
        AudioTranscribeAI: Efficient Speech Recognition and Language Model Integration for Enhanced Textual Interaction
      </v-app-bar-title>
    </v-app-bar>
    <v-main style="height: 100vh">
      <router-view />
    </v-main>
    <app-footer></app-footer>
  </v-app>
</template>

<script setup>
import AppFooter from "@/components/AppFooter.vue";
</script>
