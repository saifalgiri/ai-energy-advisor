// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })

// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// // import tailwindcss from '@tailwindcss/vite'
// import path from 'path'

// export default defineConfig({
//   plugins: [vue()],
//   resolve: {
//     alias: { '@': path.resolve(__dirname, './src') },
//   },
// })


// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import tailwindcss from '@tailwindcss/vite'
// import path from 'path'

// export default defineConfig({
//   plugins: [vue(), tailwindcss()],
//   resolve: { alias: { '@': path.resolve(__dirname, './src') } },
// })

// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import tailwindcss from '@tailwindcss/vite'
// import path from 'path'

// export default defineConfig({
//   plugins: [
//     vue(),
//     tailwindcss(),
//   ],
//   resolve: {
//     alias: { '@': path.resolve(__dirname, './src') },
//   },
// })

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})