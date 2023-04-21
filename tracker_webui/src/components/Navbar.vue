<script lang="ts">
import { defineComponent } from 'vue'

import { APIs, LOCAL_STORAGE_KEY, URLs } from '@/constants'
import type { IUser } from "@/interfaces/user"

export default defineComponent({
  data() {
    return { user: {} as IUser }
  },
  methods: {
    async performLogout() {
      const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!token) {
        this.$router.push(URLs.ROOT)
        return
      }
      const url: URL = new URL(APIs.ACCOUNT_LOGOUT, import.meta.env.VITE_API_URL)
      const headers: Headers = new Headers([
        ['Content-Type', 'application/json'],
        ['Authorization', `Token ${token}`]
      ])
      const response = await fetch(url.toString(), { method: 'DELETE', headers: headers })
      localStorage.clear()
      this.$router.push(URLs.ROOT)
    }
  },
  async mounted() {
    const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
    if (!token) {
      this.$router.push(URLs.ROOT)
      return
    }
    const url: URL = new URL(APIs.ACCOUNT_DETAIL, import.meta.env.VITE_API_URL)
    const headers: Headers = new Headers([
      ['Content-Type', 'application/json'],
      ['Authorization', `Token ${token}`]
    ])
    const response = await fetch(url.toString(), { method: 'GET', headers: headers })
    if (response.status !== 200) {
      localStorage.clear()
      return
    }
    const data: IUser = await response.json()
    this.user = data;
  }
})
</script>

<template>
  <nav
    class="bg-gray-900 fixed w-full z-20 top-0 left-0 border-b border-gray-200"
  >
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <a href="/todo" class="flex items-center">
        <img src="/favicon-32x32.png" class="h-8 mr-3" alt="Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap text-white"
          >Todo</span
        >
      </a>
      <p
        class="block py-2 pl-3 pr-4 text-white bg-black-700 rounded md:bg-transparent"
        aria-current="page"
      >
        {{ user.first_name }} {{ user.last_name }}
      </p>
      <div class="flex md:order-2">
        <button
          type="button"
          class="text-white bg-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:outline-none focus:ring-yellow-300 font-medium rounded-lg text-sm px-4 py-2 text-center mr-3 md:mr-0 dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800"
          @click="performLogout"
        >
          Log out
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped></style>
