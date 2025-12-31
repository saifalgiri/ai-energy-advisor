
<script setup lang="ts" />

<template>
  <header class="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-green-600 via-green-400 to-green-200 text-white shadow-md">
    <!-- Left Section: Logo and Mobile Menu Button -->
    <div class="flex items-center space-x-6">
      <!-- Mobile Sidebar Toggle Button -->


      <!-- Logo and Branding -->
      <div class="ml-4 flex items-center space-x-2">
        <img src="/src/assets/logo.png" alt="Home Energy Advisor Logo" class="w-25 h-10" />
      </div>
    </div>

    <!-- Center Section: Main Navigation Links -->
    <nav class="hidden lg:flex space-x-6">
      <a href="/" class="text-black hover:text-green-100 font-medium">Home</a>
      <a href="/about" class="text-black hover:text-green-100 font-medium">About Us</a>
      <a href="/energy-tips" class="text-black hover:text-green-100 font-medium">Energy Saving Tips</a>
      <a href="/calculator" class="text-black hover:text-green-100 font-medium">Energy Calculator</a>
      <a href="/contact" class="text-black hover:text-green-100 font-medium">Contact</a>
    </nav>

    <!-- Right Section: Login Button -->
    <div class="flex items-center space-x-6">
      <!-- Login Button -->
      <button
        class="px-6 py-2 text-white bg-green-500 hover:bg-green-600 rounded-lg font-medium transition-colors duration-200"
      >
        Login
      </button>
    </div>
  </header>
</template>
