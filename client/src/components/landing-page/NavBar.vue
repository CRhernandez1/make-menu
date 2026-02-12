<template>
  <header class="nav-bar flex flex-row justify-between h-[10vh] items-center px-4">
    <div class="flex flex-row">
      <div class="flex flex-row">
        <CompanyLogo class="position: absolute top-5 left-2" />
        <h1 class="position: relative mr-16 font-bold ml-10">Make Menu</h1>
      </div>
      <nav class="flex flex-row gap-4">
        <a href="#">Nuestro Producto</a>
        <a href="#">Funcionalidades</a>
        <a href="#">Quiénes somos</a>
      </nav>
    </div>
    <a href="#" class="block p-2.5 background bg-emerald-400 rounded-xl">Empezar &rarr;</a>
  </header>
</template>
<script setup lang="ts">
import CompanyLogo from './CompanyLogo.vue';
</script>
<style scoped>
.nav-bar {
  background-color: #fff;
}
</style>
