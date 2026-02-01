<script setup lang="ts">
import {computed, onMounted, ref} from "vue";

const props = defineProps({
  fontsize:{
    type: String,
    required:false,
    default:"1.6rem"
  },
  top:{
    type: Number,
    required:false,
    default:50
  },
  text:{
    type: String,
    required:true,
    default:"Hello"
  }
})

const fontStyle = computed(()=>({
  fontSize:`${props.fontsize}`,
  top:`${props.top}%`
}))

const panelClass = computed(()=>({
  'message-panel': true,
  'fade-out': isFadingOut.value,
}))

const isFadingOut = ref(false)

const isVisible = ref(true)

onMounted(()=>{
  setTimeout(()=>{
    isFadingOut.value = true
  },2000)
})

const handleAnimationEnd = ()=>{
  if(isFadingOut.value){
    isVisible.value = false
  }
}

</script>

<template>
  <div v-if="isVisible" :class="panelClass" :style="fontStyle" @animationend="handleAnimationEnd">
  {{text}}
  </div>
</template>

<style scoped>
.message-panel{
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a1a1a;
  opacity: 0.75;

  color: white;
  font-family: "SansMedium",sans-serif;

  position: absolute;

  z-index: 1;
  left: 50%;
  white-space: nowrap;
  transform: translate(-50%, -50%);

  padding: 0.6rem 1.8rem;

  border-radius: 0.4rem;

  user-select: none;

}

.message-panel.fade-out{
  animation: fade-out 0.3s ease-in forwards;
}

@keyframes fade-out {
  from{
    opacity: 0.75;
  }
  to{
    opacity: 0;
  }
}

</style>