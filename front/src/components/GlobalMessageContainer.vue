<script setup lang="ts">
import MessagePanel from "./MessagePanel.vue";

import {useMessagesStore} from "../stores/messages.ts";

const messagesStore = useMessagesStore();

</script>

<template>
<div>
  <MessagePanel v-for="msg in messagesStore.messages" :text="msg.text" :id="msg.id" ></MessagePanel>
</div>
</template>
<style scoped>

</style>