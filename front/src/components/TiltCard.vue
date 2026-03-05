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
  gameDataNow: GameFullInfo;      // 当前显示的游戏
  gameDataNext: GameFullInfo;     // 下一张游戏（用于预加载）
  gameDataPrev: GameFullInfo;     // 上一张游戏（用于预加载）
  currentIndex: number;           // 当前索引（用于标题/评价过渡）
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
  "next": [];  // 通知父组件切换到下一张
  "prev": [];  // 通知父组件切换到上一张
}>();

// 动画时长（需与 CSS 一致）
const ANIMATION_DURATION = 1200;

const descMap = ref({
  "Mostly Positive": "多半好评",
  "Positive": "特别好评",
  "Very Positive": "特别好评",
  "Overwhelmingly Positive": "好评如潮",
});

const isAnimating = ref(false);          // 是否正在播放动画
const direction = ref<"next" | "prev" | null>(null); // 当前动画方向
const animateNextLayer = ref(false);     // 控制下一张图层进入动画
const animatePrevLayer = ref(false);     // 控制上一张图层进入动画
const tiltElement = ref<HTMLElement | null>(null);
let tiltInstance: any = null;

// 当前图层 canvas
const canvasRed = ref<HTMLCanvasElement | null>(null);
const canvasGreen = ref<HTMLCanvasElement | null>(null);
const canvasBlue = ref<HTMLCanvasElement | null>(null);

// 下一图层 canvas
const canvasRedNext = ref<HTMLCanvasElement | null>(null);
const canvasGreenNext = ref<HTMLCanvasElement | null>(null);
const canvasBlueNext = ref<HTMLCanvasElement | null>(null);

// 上一图层 canvas
const canvasRedPrev = ref<HTMLCanvasElement | null>(null);
const canvasGreenPrev = ref<HTMLCanvasElement | null>(null);
const canvasBluePrev = ref<HTMLCanvasElement | null>(null);

// 存储已加载的图片对象
const imgNow = ref<HTMLImageElement | null>(null);
const imgNext = ref<HTMLImageElement | null>(null);
const imgPrev = ref<HTMLImageElement | null>(null);

// 图片加载状态
const isCurrentLoaded = ref(false);
const isNextLoaded = ref(false);
const isPrevLoaded = ref(false);

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

// 加载上一张图片并绘制
const loadPrev = async () => {
  if (!props.gameDataPrev?.header_image) return;
  try {
    const img = await loadImage(props.gameDataPrev.header_image);
    imgPrev.value = img;
    isPrevLoaded.value = true;
    if (canvasRedPrev.value && canvasGreenPrev.value && canvasBluePrev.value) {
      initGlitchLayers(img, canvasRedPrev.value, canvasGreenPrev.value, canvasBluePrev.value);
    }
  } catch (error) {
    console.error(error);
  }
};

// 切换到下一张
const goToNext = async () => {
  if (isAnimating.value || !isNextLoaded.value) return;

  isAnimating.value = true;
  direction.value = "next";
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
    imgNow.value = imgNext.value;
    isCurrentLoaded.value = true;
  }

  // 重置动画状态
  isAnimating.value = false;
  direction.value = null;
  animateNextLayer.value = false;

  // 重新加载下一张（此时父组件应已更新 gameDataNext）
  if (props.gameDataNext?.header_image) {
    await loadNext();
    await loadPrev()
  }



};

// 切换到上一张（通过 expose 暴露给父组件）
const goToPrev = async () => {
  if (isAnimating.value || !isPrevLoaded.value) return;

  isAnimating.value = true;
  direction.value = "prev";
  emit("prev");

  // 触发上一图层进入动画
  animatePrevLayer.value = false;
  await nextTick();
  animatePrevLayer.value = true;

  // 等待动画完成
  await new Promise((resolve) => setTimeout(resolve, ANIMATION_DURATION));

  // 将上一张图片绘制到当前图层
  if (imgPrev.value && canvasRed.value && canvasGreen.value && canvasBlue.value) {
    initGlitchLayers(imgPrev.value, canvasRed.value, canvasGreen.value, canvasBlue.value);
    imgNow.value = imgPrev.value;
    isCurrentLoaded.value = true;
  }

  // 重置动画状态
  isAnimating.value = false;
  direction.value = null;
  animatePrevLayer.value = false;

  // 重新加载上一张（此时父组件应已更新 gameDataPrev）
  if (props.gameDataPrev?.header_image) {
    await loadPrev();
    await loadNext()
  }
};

const goToWeb=()=>{
  window.open(`https://store.steampowered.com/app/${props.gameDataNow.steam_appid}`,"_blank")
}

// 重新绘制所有图层（用于容器大小变化时）
const redrawAllLayers = () => {
  if (imgNow.value && canvasRed.value && canvasGreen.value && canvasBlue.value) {
    initGlitchLayers(imgNow.value, canvasRed.value, canvasGreen.value, canvasBlue.value);
  }
  if (imgNext.value && canvasRedNext.value && canvasGreenNext.value && canvasBlueNext.value) {
    initGlitchLayers(imgNext.value, canvasRedNext.value, canvasGreenNext.value, canvasBlueNext.value);
  }
  if (imgPrev.value && canvasRedPrev.value && canvasGreenPrev.value && canvasBluePrev.value) {
    initGlitchLayers(imgPrev.value, canvasRedPrev.value, canvasGreenPrev.value, canvasBluePrev.value);
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
    });
  }
};

const onLeave = (el: Element, done: () => void) => {
  el.getBoundingClientRect();
  setTimeout(() => {
    done();
  }, 300);
};

// 暴露方法给父组件
defineExpose({ goToPrev, goToNext });

onMounted(() => {
  initTilt();

  // 加载初始图片
  loadCurrent();
  loadNext();
  loadPrev();

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

// 监听图片地址变化（仅在非动画时重新加载）
watch(
    () => [props.gameDataNow?.header_image, props.gameDataNext?.header_image, props.gameDataPrev?.header_image],
    () => {
      if (!isAnimating.value) {
        loadCurrent();
        loadNext();
        loadPrev();
      }
    },
    { immediate: false }
);
</script>

<template>
  <div ref="tiltElement" class="tilt-card">
    <div class="title-container">
      <Transition name="title-anim" appear @leave="onLeave">
        <span :key="currentIndex" class="tilt-card-title">
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
        backgroundColor: '#000'
      }"
    >

      <div class="controller">
        <div class="prev-button" @click="goToPrev">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15 24" class="card-button">
            <path fill="currentColor"  d="m14.759 21.088-2.596 2.597L.478 12 12.163.315l2.596 2.597L5.671 12z">
            </path>
          </svg>
        </div>
        <div class="href-area" @click="goToWeb"></div>
        <div class="next-button" @click="goToNext">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 23" class="card-button">
            <path fill="currentColor" d="m2.536 22.997-2.545-2.555L8.9 11.5-.009 2.558 2.536.003 13.991 11.5z">
            </path>
          </svg>
        </div>
      </div>

      <div class="mask">
      </div>

      <!-- 当前图层 -->
      <div
          class="layer-group current-layer"
          :class="{
          'is-exiting-next': isAnimating && direction === 'next',
          'is-exiting-prev': isAnimating && direction === 'prev'
        }"
      >
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

      <!-- 上一图层 -->
      <div class="layer-group prev-layer" :class="{ 'is-entering': animatePrevLayer }">
        <canvas ref="canvasRedPrev" class="tilt-image"></canvas>
        <canvas ref="canvasGreenPrev" class="tilt-image"></canvas>
        <canvas ref="canvasBluePrev" class="tilt-image"></canvas>
      </div>
    </div>
    <div class="review-container">
      <Transition name="review-anim" appear @leave="onLeave">
        <div :key="currentIndex" class="review-box">
          <span class="tilt-card-review" style="font-size: 1.1rem">
            {{ gameDataNow.app_reviews?.review_score_desc ? descMap[gameDataNow.app_reviews?.review_score_desc as keyof typeof descMap] : gameDataNow.app_reviews?.review_score_desc }}
          </span>
          <br />
          <span class="tilt-card-review" style="font-size: 0.9rem" v-if="gameDataNow.app_reviews">
            {{ `${gameDataNow.app_reviews.total_positive}/${gameDataNow.app_reviews.total_reviews}(${Math.round((gameDataNow.app_reviews.total_positive / gameDataNow.app_reviews.total_reviews) * 100)}%)` }}
          </span>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.tilt-card {
  user-select: none;
  position: relative;
  transform-style: preserve-3d;

  .title-container {
    pointer-events: none;
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

  .review-container {
    pointer-events: none;
    position: absolute;
    bottom: 3.2rem;
    right: 5rem;
    transform: translateZ(150px);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 25%;

    .review-box {
      transform: translateX(50px);
      transition: all 0.3s ease;

      .tilt-card-review {
        color: #ffffff;
        z-index: 500;
        font-family: "SansMedium", sans-serif;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgb(0, 0, 0), 1px 1px 4px rgb(0, 0, 0);
        opacity: 0;
        transition: all 0.3s ease;
      }
    }
  }

  .image-container {
    position: relative;
    border-radius: 6px;
    overflow: hidden;
    background-color: #000000;

    .mask{
      z-index: 100;
      position: absolute;
      bottom: 0;
      background: linear-gradient(to top, rgb(25, 25, 25), transparent);
      width: 100%;
      height: 30%;
      mix-blend-mode: normal;
      pointer-events: none;
      transform: translateY(20%);
      opacity: 0;

      transition: all 0.3s ease;
    }

    .controller{
      z-index: 150;
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transform-style: preserve-3d;
      transform: translateZ(150px);

      .href-area{
        transform-style: preserve-3d;
        transform: translateZ(150px);
        width: 100%;
        height: 100%;
        cursor: pointer;
      }

      .prev-button{
        transform-style: preserve-3d;
        transform: translateZ(150px);
        cursor: pointer;
        z-index:200;
        display: flex;
        align-items: center;
        justify-content: left;
        padding-left: 3rem;
        width: 30%;
        height: 100%;
      }

      .next-button{
        transform-style: preserve-3d;
        transform: translateZ(150px);
        cursor: pointer;
        z-index:200;
        display: flex;
        align-items: center;
        justify-content: right;
        padding-right: 3rem;
        width: 30%;
        height: 100%;
      }

      .card-button{
        transform: translateZ(150px);
        width: 30px;
        color: #ffffff;
        opacity: 0;
        transition: all 0.3s ease;
        filter: drop-shadow(-1px 2px 4px rgba(0, 0, 0, 0.9));
      }

      .prev-button:hover{
        .card-button{
          opacity: 1;
        }
      }

      .next-button:hover{
        .card-button{
          opacity: 1;
        }
      }

    }

    .tilt-image {
      z-index: 20;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      mix-blend-mode: screen;
      pointer-events: none;
    }
  }
}

.tilt-card:hover {

  .image-container{
    .mask{
      transform: rotateY(0);
      opacity: 0.8;
    }
  }
  .title-container .tilt-card-title {
    opacity: 1;
    transform: translateX(0px);
  }

  .review-container .review-box {
    transform: translateX(0px);
    .tilt-card-review {
      opacity: 1;
    }
  }
}

/* 图层默认状态 */
.current-layer {
  opacity: 1;
}
.next-layer,
.prev-layer {
  opacity: 0;
}
.next-layer.is-entering,
.prev-layer.is-entering {
  opacity: 1;
}

/* ---------- 下一张动画（向左移出/移入） ---------- */
.current-layer.is-exiting-next .tilt-image:nth-child(1) {
  animation: mergeRedNextOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.current-layer.is-exiting-next .tilt-image:nth-child(3) {
  animation: mergeBlueNextOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.current-layer.is-exiting-next .tilt-image:nth-child(2) {
  animation: flickerGreenNextOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}

@keyframes mergeRedNextOut {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(-20px); opacity: 0; }
}
@keyframes mergeBlueNextOut {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(-10px); opacity: 0; }
}
@keyframes flickerGreenNextOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.next-layer.is-entering .tilt-image:nth-child(1) {
  animation: mergeRedNextIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.next-layer.is-entering .tilt-image:nth-child(3) {
  animation: mergeBlueNextIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.next-layer.is-entering .tilt-image:nth-child(2) {
  animation: flickerGreenNextIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}

@keyframes mergeRedNextIn {
  0% { transform: translateX(-20px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes mergeBlueNextIn {
  0% { transform: translateX(-10px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes flickerGreenNextIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

/* ---------- 上一张动画（向右移出/移入） ---------- */
.current-layer.is-exiting-prev .tilt-image:nth-child(1) {
  animation: mergeRedPrevOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.current-layer.is-exiting-prev .tilt-image:nth-child(3) {
  animation: mergeBluePrevOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.current-layer.is-exiting-prev .tilt-image:nth-child(2) {
  animation: flickerGreenPrevOut 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}

@keyframes mergeRedPrevOut {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(20px); opacity: 0; }
}
@keyframes mergeBluePrevOut {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(10px); opacity: 0; }
}
@keyframes flickerGreenPrevOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.prev-layer.is-entering .tilt-image:nth-child(1) {
  animation: mergeRedPrevIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.prev-layer.is-entering .tilt-image:nth-child(3) {
  animation: mergeBluePrevIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
.prev-layer.is-entering .tilt-image:nth-child(2) {
  animation: flickerGreenPrevIn 1.2s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}

@keyframes mergeRedPrevIn {
  0% { transform: translateX(20px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes mergeBluePrevIn {
  0% { transform: translateX(10px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
@keyframes flickerGreenPrevIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

/* 标题和评价的过渡动画 */
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
  animation: titleExitAnim 0.3s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
@keyframes titleExitAnim {
  0% {
    opacity: 1;
    transform: translateX(0);
    filter: blur(0);
  }
  100% {
    opacity: 0;
    transform: translateX(20px);
  }
}

.review-anim-enter-from {
  opacity: 0 !important;
  transform: translateX(-50px) !important;
}
.review-anim-enter-active {
  transition: all 0.5s ease !important;
}
.review-anim-enter-to {
  opacity: 1 !important;
  transform: translateX(0) !important;
}
.review-anim-leave-from {
  transform: translateX(0);
}
.review-anim-leave-active {
  position: absolute;
  white-space: nowrap;
  word-wrap: normal;
  overflow: visible;
  animation: titleExitAnim 0.3s cubic-bezier(0.96, 0, 0.68, 0.69) forwards;
}
</style>