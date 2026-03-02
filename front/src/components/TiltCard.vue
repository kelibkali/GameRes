<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref, watch } from "vue";
import VanillaTilt from "vanilla-tilt";
import type { GameFullInfo } from "../types/GameFullInfo.ts";

interface Props {
  width?: string;
  height?: string;
  maxTilt?: number;
  speed?: number;
  scale?: number;
  gyroscope?: boolean;
  startX?: number;
  startY?: number;
  imgScale?: string;
  boxShadow?: string;
  gameDataNow: GameFullInfo;
  gameDataNext: GameFullInfo;
  currentIndex: number;
}

const props = withDefaults(defineProps<Props>(), {
  width: "auto",
  height: "auto",
  maxTilt: 2,
  speed: 500,
  scale: 1.02,
  gyroscope: true,
  startX: 0,
  startY: 0,
  imgScale: "100%",
  boxShadow: "none",
});

const emit = defineEmits<{
  "next": [];
}>();

// 动画时长（需与 CSS 一致）
const ANIMATION_DURATION = 1200;

const isAnimating = ref(false);
const animateNextLayer = ref(false);
const tiltElement = ref<HTMLElement | null>(null);
let tiltInstance: any = null;

// 当前图层 canvas 引用
const canvasRed = ref<HTMLCanvasElement | null>(null);
const canvasGreen = ref<HTMLCanvasElement | null>(null);
const canvasBlue = ref<HTMLCanvasElement | null>(null);

// 下一图层 canvas 引用
const canvasRedNext = ref<HTMLCanvasElement | null>(null);
const canvasGreenNext = ref<HTMLCanvasElement | null>(null);
const canvasBlueNext = ref<HTMLCanvasElement | null>(null);

// 存储已加载的图片对象
const imgNow = ref<HTMLImageElement | null>(null);
const imgNext = ref<HTMLImageElement | null>(null);

// 图片加载状态
const isCurrentLoaded = ref(false);
const isNextLoaded = ref(false);

// ResizeObserver 用于监听容器尺寸变化
let resizeObserver: ResizeObserver | null = null;

// 获取设备像素比
const getPixelRatio = (): number => window.devicePixelRatio || 1;

// 绘制单色通道
const drawSingleChannel = (
    ctx: CanvasRenderingContext2D,
    img: HTMLImageElement,
    width: number,
    height: number,
    channel: "red" | "green" | "blue"
) => {
  ctx.drawImage(img, 0, 0, width, height);
  const imageData = ctx.getImageData(0, 0, width, height);
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    if (channel === "red") {
      data[i + 1] = 0;
      data[i + 2] = 0;
    } else if (channel === "green") {
      data[i] = 0;
      data[i + 2] = 0;
    } else if (channel === "blue") {
      data[i] = 0;
      data[i + 1] = 0;
    }
  }
  ctx.putImageData(imageData, 0, 0);
};

// 初始化一组三个 canvas 为单色图层
const initGlitchLayers = (
    img: HTMLImageElement,
    redCanvas: HTMLCanvasElement,
    greenCanvas: HTMLCanvasElement,
    blueCanvas: HTMLCanvasElement
) => {
  if (!img || !redCanvas || !greenCanvas || !blueCanvas) return;

  const dpr = getPixelRatio();
  const rect = redCanvas.getBoundingClientRect();
  const w = rect.width * dpr;
  const h = rect.height * dpr;

  [redCanvas, greenCanvas, blueCanvas].forEach((canvas) => {
    canvas.width = w;
    canvas.height = h;
  });

  const ctxRed = redCanvas.getContext("2d");
  const ctxGreen = greenCanvas.getContext("2d");
  const ctxBlue = blueCanvas.getContext("2d");

  if (ctxRed && ctxGreen && ctxBlue) {
    ctxRed.imageSmoothingEnabled = true;
    ctxRed.imageSmoothingQuality = "high";
    ctxGreen.imageSmoothingEnabled = true;
    ctxGreen.imageSmoothingQuality = "high";
    ctxBlue.imageSmoothingEnabled = true;
    ctxBlue.imageSmoothingQuality = "high";

    drawSingleChannel(ctxRed, img, w, h, "red");
    drawSingleChannel(ctxGreen, img, w, h, "green");
    drawSingleChannel(ctxBlue, img, w, h, "blue");
  }
};

// 通用图片加载函数
const loadImage = (src: string): Promise<HTMLImageElement> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to load image: ${src}`));
    img.src = src;
  });
};

// 加载当前图片并绘制
const loadCurrent = async () => {
  if (!props.gameDataNow?.header_image) return;
  try {
    const img = await loadImage(props.gameDataNow.header_image);
    imgNow.value = img;
    isCurrentLoaded.value = true;
    if (canvasRed.value && canvasGreen.value && canvasBlue.value) {
      initGlitchLayers(img, canvasRed.value, canvasGreen.value, canvasBlue.value);
    }
  } catch (error) {
    console.error(error);
    // 可设置占位图处理
  }
};

// 加载下一张图片并绘制
const loadNext = async () => {
  if (!props.gameDataNext?.header_image) return;
  try {
    const img = await loadImage(props.gameDataNext.header_image);
    imgNext.value = img;
    isNextLoaded.value = true;
    if (canvasRedNext.value && canvasGreenNext.value && canvasBlueNext.value) {
      initGlitchLayers(img, canvasRedNext.value, canvasGreenNext.value, canvasBlueNext.value);
    }
  } catch (error) {
    console.error(error);
  }
};

// 处理卡片点击
const handleCardClick = async () => {
  if (isAnimating.value || !isNextLoaded.value) return; // 确保下一张已加载

  isAnimating.value = true;
  emit("next");

  // 触发下一图层进入动画
  animateNextLayer.value = false;
  await nextTick();
  animateNextLayer.value = true;

  // 等待动画完成
  await new Promise((resolve) => setTimeout(resolve, ANIMATION_DURATION));

  // 将下一张图片绘制到当前图层
  if (imgNext.value && canvasRed.value && canvasGreen.value && canvasBlue.value) {
    initGlitchLayers(imgNext.value, canvasRed.value, canvasGreen.value, canvasBlue.value);
    // 更新当前图片引用
    imgNow.value = imgNext.value;
    isCurrentLoaded.value = true;
  }

  // 重置动画状态
  isAnimating.value = false;
  animateNextLayer.value = false;

  // 此时父组件已更新 props，下一图层需要加载新的下下张图片
  // 由 watch 自动触发 loadNext，但为了立即刷新，可手动调用
  if (props.gameDataNext?.header_image) {
    loadNext();
  }
};

// 重新绘制所有图层（用于容器大小变化时）
const redrawAllLayers = () => {
  if (imgNow.value && canvasRed.value && canvasGreen.value && canvasBlue.value) {
    initGlitchLayers(imgNow.value, canvasRed.value, canvasGreen.value, canvasBlue.value);
  }
  if (imgNext.value && canvasRedNext.value && canvasGreenNext.value && canvasBlueNext.value) {
    initGlitchLayers(imgNext.value, canvasRedNext.value, canvasGreenNext.value, canvasBlueNext.value);
  }
};

// 初始化倾斜效果
const initTilt = () => {
  if (tiltElement.value) {
    VanillaTilt.init(tiltElement.value, {
      max: props.maxTilt,
      speed: props.speed,
      scale: props.scale,
      gyroscope: props.gyroscope,
      reset: true,
      // 注意：reset-to-start 和 startX/Y 并非官方选项，可能需要移除或检查插件版本
      // 如果无效可删除
    });
  }
};

const onLeave = (el:Element, done:() => void) => {
  el.getBoundingClientRect()

  setTimeout(()=>{
    done();
  },300)
}

onMounted(() => {
  initTilt();

  // 加载初始图片
  loadCurrent();
  loadNext();

  // 设置 ResizeObserver 监听容器尺寸变化
  const container = document.querySelector(".image-container") as HTMLElement;
  if (container) {
    resizeObserver = new ResizeObserver(() => {
      redrawAllLayers();
    });
    resizeObserver.observe(container);
  }
});

onUnmounted(() => {
  // 销毁倾斜实例
  if (tiltInstance && tiltInstance.element) {
    tiltInstance.destroy();
  }
  // 断开 ResizeObserver
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});

// 监听图片地址变化
watch(
    () => [props.gameDataNow?.header_image, props.gameDataNext?.header_image],
    () => {
      // 非动画状态下重新加载图片
      if (!isAnimating.value) {
        loadCurrent();
        loadNext();
      }
    },
    { immediate: false } // 移除 immediate，避免与 onMounted 重复
);

// 可选：监听尺寸变化（如果通过 props 传递宽高）
watch(() => [props.width, props.height], () => {
  nextTick(() => redrawAllLayers());
});
</script>

<template>
  <div ref="tiltElement" class="tilt-card" @click="handleCardClick">
    <div class="title-container">
      <Transition
        name="title-anim"
        appear
        @leave="onLeave"
      >
        <span
            :key="currentIndex"
            class="tilt-card-title"
        >
          {{ gameDataNow.name }}
        </span>
      </Transition>

    </div>
    <div
        class="image-container"
        :style="{
        width: width,
        height: height,
        scale: scale,
        boxShadow: boxShadow,
        backgroundColor: '#000' // 确保背景为黑色，避免混色异常
      }"
    >
      <!-- 当前图层 -->
      <div class="layer-group current-layer" :class="{ 'is-exiting': isAnimating }">
        <canvas ref="canvasRed" class="tilt-image"></canvas>
        <canvas ref="canvasGreen" class="tilt-image"></canvas>
        <canvas ref="canvasBlue" class="tilt-image"></canvas>
      </div>

      <!-- 下一图层 -->
      <div class="layer-group next-layer" :class="{ 'is-entering': animateNextLayer }">
        <canvas ref="canvasRedNext" class="tilt-image"></canvas>
        <canvas ref="canvasGreenNext" class="tilt-image"></canvas>
        <canvas ref="canvasBlueNext" class="tilt-image"></canvas>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tilt-card {
  user-select: none;
  position: relative;
  transform-style: preserve-3d;

  .title-container {
    position: absolute;
    bottom: 4rem;
    left: 7rem;
    max-width: 65%;
    transform: translateZ(150px);
    display: flex;
    align-items: center;
    justify-content: space-between;

    .tilt-card-title {
      color: #ffffff;
      z-index: 500;
      font-family: "SansMedium", sans-serif;
      font-weight: bold;
      font-size: 1.2rem;
      text-shadow: 2px 2px 4px rgb(0, 0, 0), 1px 1px 4px rgb(0, 0, 0);

      transform: translateX(-50px);
      opacity: 0;
      transition: all 0.3s ease;
    }
  }

  .image-container {
    position: relative;
    border-radius: 6px;
    overflow: hidden;
    background-color: #000; /* 黑色背景保证混色正确 */

    .tilt-image {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      mix-blend-mode: screen;
      pointer-events: none; /* 避免 canvas 拦截点击事件 */
    }
  }
}

.tilt-card:hover {
  .title-container {
    .tilt-card-title {
      opacity: 1;
      transform: translateX(0px);


    }
  }
}

.current-layer {
  opacity: 1;
}

.current-layer.is-exiting {
  opacity: 1;
}

.next-layer {
  opacity: 0;
}

.next-layer.is-entering {
  opacity: 1;
}

.current-layer.is-exiting .tilt-image:nth-child(1) { /* Red */
  animation: mergeRed 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}
.current-layer.is-exiting .tilt-image:nth-child(3) { /* Blue */
  animation: mergeBlue 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}
.current-layer.is-exiting .tilt-image:nth-child(2) { /* Green */
  animation: flickerGreen 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}

@keyframes mergeRed {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(-20px); opacity: 0; }
}
@keyframes mergeBlue {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(-10px); opacity: 0; }
}
@keyframes flickerGreen {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.next-layer.is-entering .tilt-image:nth-child(1) { /* Red */
  animation: mergeRedNext 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}
.next-layer.is-entering .tilt-image:nth-child(3) { /* Blue */
  animation: mergeBlueNext 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}
.next-layer.is-entering .tilt-image:nth-child(2) { /* Green */
  animation: flickerGreenNext 1.2s cubic-bezier(.96,0,.68,.69) forwards;
}

@keyframes mergeRedNext {
  0% { transform: translateX(-20px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes mergeBlueNext {
  0% { transform: translateX(-10px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes flickerGreenNext {
  0% { opacity: 0; }
  100% { opacity: 1; }
}


.title-anim-enter-from {
  opacity: 0 !important;
  transform: translateX(-50px) !important;
}

.title-anim-enter-active {
  transition: all 0.5s ease !important;
}

.title-anim-enter-to {
  opacity: 1 !important;
  transform: translateX(0) !important;
}

.title-anim-leave-from {
  transform: translateX(0);
}

.title-anim-leave-active {
  position: absolute;
  white-space: nowrap;
  word-wrap: normal;
  overflow: visible;
  animation: titleExitAnim 0.3s cubic-bezier(.96,0,.68,.69) forwards;
}

.title-anim-leave-to {
  opacity: 0;
}

@keyframes titleExitAnim {
  0% {
    opacity: 1;
    transform: translateX(0) ;
    filter: blur(0);
  }
  100% {
    opacity: 0;
    transform: translateX(20px);
  }
}

</style>