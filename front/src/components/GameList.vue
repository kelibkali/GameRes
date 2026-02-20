<script setup lang="ts">
import {useAuthStore} from "../stores/auth.ts";
import {onMounted, ref, watch} from "vue";

import {getGames} from "../services/SteamApi.ts";
import type {GameInList} from "../types/GameInList.ts";
import GameTimeProgressBar from "./GameTimeProgressBar.vue";
import type {TableInstance} from "element-plus";

const user = ref();
const authStore = useAuthStore();
const tableData = ref<GameInList[]>([])

const tableRef = ref<TableInstance | null>()

const activeSort = ref("playtime_2weeks")

const needHiddenList = ["playtime_2weeks","achievements_total"]

const tableHeaderCellClassName=(data:any)=>{
  const prop = data.column.property
  const name = data.column.id
  const table = tableRef.value!!;

  const { context } = table;
  const tableHeaderEle = context.refs.headerWrapper;
  const bodyWrapperEle = context.refs.bodyWrapper;

  const needHidden = needHiddenList.includes(prop);
  const colgroupHeader = tableHeaderEle.querySelector(`[name="${name}"]`);
  const colgroupBody = bodyWrapperEle.querySelector(`[name="${name}"]`);

  if (needHidden) {
    colgroupHeader?.classList.add("hidden")
    colgroupBody?.classList.add("hidden")
    return "hidden";
  }

  colgroupHeader?.classList.remove("hidden")
  colgroupBody?.classList.remove("hidden")

  return "";
}

const tableCellClassName = (data:any)=>{
  const prop = data.column.property;
  const needHidden = needHiddenList.includes(prop);

  if (needHidden) {
    return "hidden";
  }

  return "";
}

const getGameList = async () => {
  user.value = authStore.user;
  console.log(user.value);
  if (user.value) {
    const data = await getGames(user.value.steamID);
    tableData.value = data.data.games
    console.log(data);
  }
}

const handleClick = (prop: string) => {
  if (activeSort.value === prop) return

  activeSort.value = prop;
  tableRef.value?.sort(activeSort.value, "descending");
}

watch(
    () => authStore.user,
    (newValue) => {
      if (newValue) {
        getGameList()
      }
    },
    {immediate: true}
)

onMounted(() => {
})

</script>

<template>
  <el-table
      ref="tableRef"
      class="game-table"
      :data="tableData"
      :default-sort="{prop: 'playtime_2weeks', order: 'descending'}"
      height="95%"
      :header-cell-class-name="tableHeaderCellClassName"
      :cell-class-name="tableCellClassName"
  >
    <el-table-column max-height="100px" width="150px">
      <template #default="scope">
        <el-image
            class="header-image"
            loading="lazy"
            :src="scope.row.header_image"
        />
      </template>
    </el-table-column>
    <el-table-column prop="playtime_forever">
      <template #header>
        <div class="table-header">
          <div
              class="container"
              :class="{active: activeSort === 'playtime_forever'}"
              @click="handleClick('playtime_forever')"
          >
            <span>总时间</span>
            <div class="triangle-border"></div>
          </div>
          <div
              class="container"
              :class="{active: activeSort === 'playtime_2weeks'}"
              @click="handleClick('playtime_2weeks')"
          >
            <span>两周时间</span>
            <div class="triangle-border"></div>
          </div>
        </div>
      </template>

      <template #default="scope">
        <game-time-progress-bar
            :play-time="Math.round(scope.row.playtime_forever / 6) / 10"
            :play-time2week="Math.round(scope.row.playtime_2weeks / 6) / 10"
            :game-name="scope.row.name"
        >
        </game-time-progress-bar>
      </template>
    </el-table-column>

    <el-table-column
        prop="playtime_2weeks"
    ></el-table-column>

    <el-table-column
        prop="achieved_count"
        width="100px"
    >
      <template #default="scope">
        <span v-if="scope.row.achievements_total !== 0">
          {{scope.row.achieved_count}} / {{ scope.row.achievements_total }}
        </span>
        <span v-else>
          - / -
        </span>
      </template>
    </el-table-column>

    <el-table-column
        prop="achievements_total"
    ></el-table-column>


  </el-table>
</template>

<style scoped>
.header-image {
  border-radius: 6px;
  user-select: none;
}

::v-deep(.el-table__cell .cell) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 15px;
  font-weight: normal;
}

.container {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #7a7a7a;

  &.active {
    color: #1a1a1a;

    .triangle-border {
      border-top-color: #1a1a1a;
    }
  }

  .triangle-border {
    width: 0;
    height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-top: 8px solid #7a7a7a;
    margin-left: 0.5rem;
  }
}

:deep(.hidden){
  display: none;
}
</style>