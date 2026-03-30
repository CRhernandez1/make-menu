<script setup lang="ts">
import Footer from '@/components/Footer.vue'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <Navbar />
  <main class="min-h-screen">
    <RouterView />
  </main>
  <Footer />
</template>
