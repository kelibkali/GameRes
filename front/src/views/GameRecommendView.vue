<script setup lang="ts">


import {getRecommendGames} from "../services/GameRecommendApi.ts";
import type {GameFullInfo} from "../types/GameFullInfo.ts";
import {onActivated, onMounted, ref} from "vue";
import TiltCard from "../components/TiltCard.vue";

const gameData = ref<Array<GameFullInfo>>([]);
const index = ref(0);
const initGames = async () => {
  const data = await getRecommendGames();
  if(data.type == "success"){
    gameData.value = Object.values(data.recommend_games);
  }
}

onMounted(async () => {
  await initGames();
})

onActivated(async () => {
  await initGames();
})
</script>

<template>
  <div style="display: flex;justify-content: center; align-items: center;">
    <div class="game-card-container">
        <TiltCard
            class="game-card"
            width="1012px"
            height="473px"
            box-shadow="1px 4px 8px 0 rgba(0, 0, 0, 0.2), 1px 6px 20px 0 rgba(0, 0, 0, 0.19)"
            @next="index++"
            v-if="gameData[index]"
            :currentIndex="index"
            :gameDataNow="gameData[index]"
            :gameDataNext="gameData[index+1]"
        ></TiltCard>
    </div>
  </div>
</template>

<style scoped>
.game-card-container{
  width: 1200px;
  height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>