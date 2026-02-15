<template>
  <div class="flex items-center justify-center mt-20">
    <div class="w-full max-w-xs">
      <h2 class="text-xl font-bold mb-4">Login</h2>
      <input
        v-model="username"
        type="text"
        placeholder="Usuario"
        class="w-full mb-3 p-2 border rounded"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Contraseña"
        class="w-full mb-3 p-2 border rounded"
      />
      <button @click="handleLogin" class="w-full bg-emerald-400 text-white p-2 rounded">
        Entrar
      </button>
      <p v-if="message" class="mt-2 text-sm text-red-500">{{ message }}</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const message = ref('');

const handleLogin = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });
    const data = await res.json();
    console.log(data);
  } catch {
    message.value = 'Error al conectar con el servidor';
  }
};
</script>
