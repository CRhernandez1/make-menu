<template>
  <div class="landing-page">
    <NavBar />
    <HeroSection />
    <FeaturesGrid />
    <HowItWorks />
    <SiteFooter />
  </div>
</template>
<script setup lang="ts">
import HeroSection from '@/components/landing-page/HeroSection.vue';
import NavBar from '../components/landing-page/NavBar.vue';
import FeaturesGrid from '@/components/landing-page/FeaturesGrid.vue';
import HowItWorks from '@/components/landing-page/HowItWorks.vue';
import SiteFooter from '@/components/landing-page/SiteFooter.vue';
</script>
<style scoped></style>
