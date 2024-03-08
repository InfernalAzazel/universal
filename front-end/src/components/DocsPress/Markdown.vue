<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps<{
  markdown: string;
}>();

const md = new MarkdownIt({
  html: true,
  linkify: true,
  highlight(code, language) {
    const validLang = !!(language && hljs.getLanguage(language))
    if (validLang) {
      const lang = language ?? ''
      return highlightBlock(hljs.highlight(code, { language: lang }).value, lang)
    }
    return highlightBlock(hljs.highlightAuto(code).value, '')
  }
});
const renderedMarkdown = ref('');

function highlightBlock(str: string, lang?: string) {
  return `
<pre class="code-block-wrapper flex flex-col">
  <div class="flex flex-row rounded-t-lg justify-between space-x-2 pl-2 pr-2  bg-[#ffffff] text-gray">
    <span class="code-block-header__lang">${lang}</span>
    <span class="code-block-header__copy cursor-pointer hover:text-[#4b9e5f]">copy</span>
  </div>
  <code class="flex hljs code-block-body  rounded-b-lg overflow-auto mb-4 ${lang}">${str}</code>
</pre>`
}

watchEffect(() => {
  renderedMarkdown.value = md.render(props.markdown);
});

</script>

<template>
  <div v-html="renderedMarkdown" class="markdown-body"></div>
</template>

<style scoped>
</style>