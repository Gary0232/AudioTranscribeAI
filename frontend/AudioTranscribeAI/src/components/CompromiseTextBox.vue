<template>
  <template v-for="(word, index) in words" :key="index">
    <span
      v-if="word.pos !== 'SPACE' && word.pos !== 'PUNCT'"
      @mouseover="hoverWord(index)"
      @mouseleave="leaveWord(index)"
      @click="selectWord(word)"
      :style="wordStyle(index)"
      class="word-span"
    >
      {{ word.text }}
    </span>
    <span v-else :class="{'space': word.pos === 'SPACE', 'punctuation': word.pos === 'PUNCT'}">
      {{ word.text }}
    </span>
  </template>
</template>

<script>
import {ref, watch, toRefs} from 'vue';

export default {
  props: {
    words: Array,
    modelValue: Object,
  },
  emits: ['update:modelValue'],
  setup(props, {emit}) {
    const {words, modelValue} = toRefs(props);
    const hoveredIndex = ref(null);
    const selectedWord = ref(modelValue.value);

    watch(modelValue, (newValue) => {
      selectedWord.value = newValue;
    });

    const hoverWord = (index) => {
      if (words.value[index].pos !== 'SPACE' && words.value[index].pos !== 'PUNCT') {
        hoveredIndex.value = index;
      }
    };

    const leaveWord = (index) => {
      if (hoveredIndex.value === index) {
        hoveredIndex.value = null;
      }
    };

    const selectWord = (word) => {
      if (word.pos !== 'SPACE' && word.pos !== 'PUNCT') {
        selectedWord.value = word;
        emit('update:modelValue', word);
      }
    };

    const wordStyle = (index) => ({
      backgroundColor: hoveredIndex.value === index ? '#ffc069' : 'transparent',
      cursor: 'pointer',
    });

    return {
      words,
      hoveredIndex,
      selectedWord,
      hoverWord,
      leaveWord,
      selectWord,
      wordStyle,
    };
  }
}
</script>

<style scoped>
.text-area {
  border: 1px solid #ccc;
  padding: 10px;
}

.word-span:hover {
  text-decoration: underline;
}

.space, .punctuation {
  pointer-events: none;
}
</style>
