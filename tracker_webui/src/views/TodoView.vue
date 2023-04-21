<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import CreateTask from '@/components/CreateTask.vue'
import ListTask from '@/components/ListTask.vue'
</script>

<template>
  <div>
    <Navbar />
    <main>
      <br /><br /><br />
      <CreateTask />
      <ListTask />
    </main>
  </div>
</template>

<style scoped></style>
