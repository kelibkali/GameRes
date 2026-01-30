<script setup lang="ts">
import { CircleCloseFilled } from "@element-plus/icons-vue"
</script>

<template>
    <CircleCloseFilled class="close"></CircleCloseFilled>
</template>

<style scoped>
.close{
  opacity: 0;
  animation: fadeIn 0.5s ease-in-out forwards;
  cursor: pointer;
  transition: opacity 0.5s ease;
}

@keyframes fadeIn {
  from{
    opacity: 0;
  }
  to{
    opacity: 1;
  }
}

</style>