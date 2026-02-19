<script setup lang="ts">
import {computed, onMounted, ref} from "vue";

interface ColorRange {
  min: number
  max: number | typeof Infinity
  color: string
}

interface Props {
  gameName?: string
  playTime?: number
  playTime2week?: number
  maxValue?: number
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  playTime: 0,
  maxValue: 1000,
  height: '8px',
})

const colorRanges = ref<ColorRange[]>([
  { min: 0, max: 50, color: '#409EFF' },
  { min: 50, max: 100, color: '#90ef4b' },
  { min: 100, max: 500, color: '#9361bf' },
  { min: 500, max: Infinity, color: '#f4c03b' },
])

const currentValue = ref(props.playTime)

// 根据当前值获取对应颜色
const getCurrentColor = (value: number): string => {
  for (const range of colorRanges.value) {
    if (value >= range.min && value < range.max) {
      return range.color
    }
  }
  // 处理最大值边界情况
  const lastRange = colorRanges.value[colorRanges.value.length - 1]
  return lastRange?.color || '#409EFF'
}

const progressPercent = computed(() => {
  let percent = 0
  percent += Math.min((props.playTime / 50) * 40,40)
  percent += Math.min(props.playTime >= 50 ? ((props.playTime - 50) / 50) * 40 : 0 ,40)
  percent += Math.min(props.playTime >= 100 ? ((props.playTime - 100) / 400) * 15 : 0,15)
  percent += Math.min(props.playTime >= 500 ? ((props.playTime - 500) / 100000) : 0,5)
  return Math.min(Math.max(percent, 0), 100)
})

const animatedWidth = ref(0)

const fillStyle = computed(() => ({
  width: `${animatedWidth.value}%`,
  backgroundColor: getCurrentColor(currentValue.value),
  height: props.height
}))

onMounted(()=>{
  setTimeout(()=>{
    animatedWidth.value = progressPercent.value
  })
})

</script>

<template>
  <div class="progress-container">
    <span class="game-name">
      {{props.gameName}}
    </span>
    <div class="time-text">
      <span >
        {{props.playTime}}h
      </span>
      <span class="playtime-2week">
        {{props.playTime2week}}h
      </span>
    </div>
    <div class="progress-bar-bg">
      <div
          class="progress-bar-fill"
          :style="fillStyle"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.progress-container {
  width: 100%;

}

.progress-bar-bg {
  width: 100%;
  background-color: #ebeef5;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  margin-top: 0.2rem;
}

.progress-bar-fill {
  width: 0;
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease, background-color 0.3s ease;
}

.time-text{
  color: #2c2c2c;
  font-family: "SansMedium", sans-serif;
  font-size: 14px;
  margin-bottom: 0.2rem;
  margin-top: 0.6rem;
  display: flex;
  justify-content: space-between;
  .playtime-2week{
    color: #8e8e8e;
    font-size: 12px;
  }
}

.game-name{
  font-weight: bold;
  color: #1a1a1a;
  font-family: "SansMedium", sans-serif;
  font-size: 16px;
}
</style>