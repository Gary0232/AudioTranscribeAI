<template>
  <v-footer height="40" app>
    Group Members:&nbsp;
    <v-tooltip
      v-for="item in items"
      location="top"
    >
      <template v-slot:activator="{ props }">
        <a v-bind="props" class="ml-2 social-link" style="cursor: pointer">
          <v-icon color="grey-lighten-1" size="20">
            mdi-account
          </v-icon>
        </a>
      </template>
      <span>{{item.unikey}}</span><br>
      <span>{{item.sid}}</span>
    </v-tooltip>


    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px;"
    >
      May, 2024 — <span class="d-none d-sm-inline-block">COMP4425 Group 3</span>
<!--      —-->
<!--      <a-->
<!--        class="text-decoration-none on-surface"-->
<!--        href="https://vuetifyjs.com/about/licensing/"-->
<!--        rel="noopener noreferrer"-->
<!--        target="_blank"-->
<!--      >-->
<!--        MIT License-->
<!--      </a>-->
    </div>
  </v-footer>
</template>

<script setup>
  const items = [
    {
      unikey: 'lyan3310',
      sid: '490203943'
    },
    {
      unikey: 'zhhu3786',
      sid: '510515492'
    },
    {
      unikey: 'hguo7508',
      sid: '512515492'
    },
    {
      unikey: 'gudu9182',
      sid: '510216876'
    },
  ]
</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)
</style>
