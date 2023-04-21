<script lang="ts">
import { defineComponent } from 'vue'

import { APIs, LOCAL_STORAGE_KEY, URLs } from '@/constants'
import type { IItem } from '@/interfaces/item'

export default defineComponent({
  data() {
    return { items: [] as IItem[] }
  },
  methods: {
    async patchItemByID(id: number | undefined) {
      const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!token) {
        this.$router.push(URLs.ROOT)
        return
      }
      const url: URL = new URL(`${APIs.TASK_ITEM}/${id}`, import.meta.env.VITE_API_URL)
      const headers: Headers = new Headers([
        ['Content-Type', 'application/json'],
        ['Authorization', `Token ${token}`]
      ])
      const response: Response = await fetch(url.toString(), {
        method: 'PATCH',
        body: JSON.stringify({ done: true }),
        headers: headers
      })
      if (response.status !== 200) {
        alert('Something went wrong!')
        return
      }
      this.$router.push(URLs.ROOT)
    },
    async destroyItemByID(id: number | undefined) {
      const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!token) {
        this.$router.push(URLs.ROOT)
        return
      }
      const url: URL = new URL(`${APIs.TASK_ITEM}/${id}`, import.meta.env.VITE_API_URL)
      const headers: Headers = new Headers([
        ['Content-Type', 'application/json'],
        ['Authorization', `Token ${token}`]
      ])
      const response: Response = await fetch(url.toString(), {
        method: 'DELETE',
        headers: headers
      })
      if (response.status !== 204) {
        alert('Something went wrong!')
        return
      }
      this.$router.push(URLs.ROOT)
    }
  },
  async mounted() {
    const token: string | null = localStorage.getItem(LOCAL_STORAGE_KEY)
    if (!token) {
      this.$router.push(URLs.ROOT)
      return
    }
    const url: URL = new URL(APIs.TASK_ITEM, import.meta.env.VITE_API_URL)
    const headers: Headers = new Headers([
      ['Content-Type', 'application/json'],
      ['Authorization', `Token ${token}`]
    ])
    const response: Response = await fetch(url.toString(), {
      method: 'GET',
      headers: headers
    })
    if (response.status !== 200) {
      alert('Something went wrong!')
      return
    }
    const data: IItem[] = await response.json()
    this.items = data
  }
})
</script>

<template>
  <div class="flex flex-col">
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <table class="min-w-full text-left text-sm font-light">
            <thead class="border-b font-medium dark:border-neutral-500">
              <tr class="bg-black text-white">
                <th scope="col" class="px-6 py-4">Task</th>
                <th scope="col" class="px-6 py-4">Status</th>
                <th scope="col" class="px-6 py-4">Delete</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b dark:border-neutral-500" v-for="item in items">
                <td class="whitespace-nowrap px-6 py-4">
                  <span v-if="item.done === true"
                    ><s>{{ item.text }}</s></span
                  ><span v-else>{{ item.text }}</span>
                </td>
                <td class="whitespace-nowrap px-6 py-4">
                  <span v-if="item.done === true"> Done </span
                  ><span v-else
                    ><button
                      type="button"
                      class="middle none center rounded-lg bg-blue-500 py-3 px-6 font-sans text-xs font-bold uppercase text-white shadow-md shadow-blue-500/20 transition-all hover:shadow-lg hover:shadow-blue-500/40 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                      @click="patchItemByID(item.id)"
                    >
                      Mark Done
                    </button></span
                  >
                </td>
                <td class="whitespace-nowrap px-6 py-4">
                  <button
                    type="button"
                    class="middle none center rounded-lg bg-red-500 py-3 px-6 font-sans text-xs font-bold uppercase text-white shadow-md shadow-red-500/20 transition-all hover:shadow-lg hover:shadow-red-500/40 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                    @click="destroyItemByID(item.id)"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
