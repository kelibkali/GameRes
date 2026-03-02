<script setup lang="ts">
import {onBeforeUnmount, onMounted, ref} from "vue";
import Rellax from 'rellax';

interface Props{
  speed?:number
  xsSpeed?:number
}

const props = withDefaults(defineProps<Props>(),{
  speed:-2,
  xsSpeed:undefined,
});

let rellaxInstance:any = null
const rootRef = ref<HTMLElement | null>(null)

onMounted(()=>{
  if(rootRef.value){
    rellaxInstance = new Rellax(".rellax",{
      breakpoints:[576,768,1024]
    });
  }
})

onBeforeUnmount(()=>{
  if(rellaxInstance){
    rellaxInstance.destroy()
    rellaxInstance = null
  }
})

</script>


<template>
  <div class="rellax" :data-rellax-speed="speed" :data-rellax-xs-speed="xsSpeed">
    <slot></slot>
  </div>
</template>

<style scoped>
.rellax {
  will-change: transform;
}
</style>