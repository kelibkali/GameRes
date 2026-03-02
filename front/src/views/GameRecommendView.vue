<script setup lang="ts">


import {getRecommendGames} from "../services/GameRecommendApi.ts";
import type {GameFullInfo} from "../types/GameFullInfo.ts";
import {onMounted, ref} from "vue";

const gameData = ref<Array<GameFullInfo>>([]);

const initGames = async () => {
  const data = await getRecommendGames();
  if(data.type == "success"){
    gameData.value = Object.values(data.recommend_games);
  }
}

onMounted(async () => {
  await initGames();
})
</script>

<template>
  <el-table :data="gameData"   height="95%">
    <el-table-column max-height="100px" width="500px">
      <template #default="scope">
        <el-link :href="`https://store.steampowered.com/app/${scope.row.steam_appid}/`" target="_blank">
          <el-image
              class="header-image"
              loading="lazy"
              :src="scope.row.header_image"

          />
        </el-link>
      </template>
    </el-table-column>
    <el-table-column prop="name"></el-table-column>
    <el-table-column prop="steam_appid"></el-table-column>
  </el-table>


</template>

<style scoped>

</style>