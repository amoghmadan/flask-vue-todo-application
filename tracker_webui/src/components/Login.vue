<script lang="ts">
import { defineComponent } from 'vue'

import { APIs, LOCAL_STORAGE_KEY, URLs } from '@/constants'
import type { IPayload, IToken } from '@/interfaces/login'

export default defineComponent({
  mounted() {
    const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
    if (!token) return
    this.$router.push(URLs.TODO)
  },
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async performLogin() {
      const url: URL = new URL(APIs.ACCOUNT_LOGIN, import.meta.env.VITE_API_URL)
      const payload: IPayload = { email: this.email, password: this.password }
      const headers: Headers = new Headers([['Content-Type', 'application/json']])
      const response: Response = await fetch(url.toString(), {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: headers
      })
      if (response.status !== 201) {
        alert('Invalid credentials.')
        return
      }
      const data: IToken = await response.json()
      localStorage.setItem(LOCAL_STORAGE_KEY, data.token)
      this.$router.push(URLs.TODO)
    }
  }
})
</script>

<template>
  <section class="bg-gray-50 dark:bg-gray-900">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <a
        href="#"
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        <img class="w-8 h-8 mr-2" src="/favicon-32x32.png" alt="logo" />
        Todo
      </a>
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            Sign in to your account
          </h1>
          <form class="space-y-4 md:space-y-6" action="#">
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your email</label
              >
              <input
                type="email"
                name="email"
                id="email"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="name@website.com"
                required="true"
                v-model="email"
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required="true"
                v-model="password"
              />
            </div>
            <button
              type="button"
              class="w-full middle none center rounded-lg bg-blue-500 py-3 px-6 font-sans text-xs font-bold uppercase text-white shadow-md shadow-blue-500/20 transition-all hover:shadow-lg hover:shadow-blue-500/40 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
              @click="performLogin"
            >
              Sign in
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
