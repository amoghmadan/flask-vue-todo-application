<script lang="ts">
import { defineComponent } from 'vue'

import { APIs, LOCAL_STORAGE_KEY, URLs } from '@/constants'
import type { IItem } from '@/interfaces/item'

export default defineComponent({
  data() {
    return {
      text: '' as string
    }
  },
  methods: {
    async createTaskItem() {
      const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!token) {
        this.$router.push(URLs.ROOT)
        return
      }
      const payload: IItem = { text: this.text }
      const url: URL = new URL(APIs.TASK_ITEM, import.meta.env.VITE_API_URL)
      const headers: Headers = new Headers([
        ['Content-Type', 'application/json'],
        ['Authorization', `Token ${token}`]
      ])
      const response: Response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: headers
      })
      if (response.status !== 201) {
        alert('Something went wrong!')
        return
      }
      this.$router.push(URLs.ROOT)
    }
  }
})
</script>

<template>
  <div className="justify-center mt-4 flex">
    <form onSubmit={onSubmit}>
      <div className="flex items-center py-2">
        <input
          type="text"
          id="text"
          placeholder="Text"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          v-model="text"
        />
        <button
          type="button"
          class="middle none center rounded-lg bg-blue-500 py-3 px-6 font-sans text-xs font-bold uppercase text-white shadow-md shadow-blue-500/20 transition-all hover:shadow-lg hover:shadow-blue-500/40 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          @click="createTaskItem"
        >
          Add
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped></style>
